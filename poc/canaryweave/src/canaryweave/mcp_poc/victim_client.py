from __future__ import annotations

import asyncio
import json
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from mcp import types
from mcp.client import session as client_session_module
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from .common import (
    CLIENT_NAME,
    DEFAULT_SCENARIO_IDS,
    MCP_PROTOCOL_VERSION,
    SAFETY_BOUNDARY,
    SERVER_NAME,
    SamplingObservation,
    SinkWrite,
    VictimPolicy,
    safe_artifact_path,
    scenario_config,
)
from .deterministic_sampler import deterministic_sampling_result, extract_text_content
from .guardrail import GuardrailDecision, SamplingGuardrail


@dataclass(frozen=True)
class ScenarioRunResult:
    scenario_id: str
    policy: str
    client_sampling_capability_advertised: bool
    sampling_requests_seen: int
    unauthorized_inert_action_executed: bool
    canary_touched: bool
    guardrail_decision: GuardrailDecision
    sink_writes: tuple[SinkWrite, ...]
    tool_result: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["guardrail_decision"] = self.guardrail_decision.to_dict()
        data["sink_writes"] = [write.to_dict() for write in self.sink_writes]
        return data


@dataclass(frozen=True)
class McpSamplingPocResult:
    schema_version: str
    mcp_protocol_version: str
    transport: str
    policy: str
    safety_boundary: str
    total_scenarios: int
    successes: int
    attack_success_rate: float
    sampling_requests_seen: int
    sink_writes: int
    observations: tuple[SamplingObservation, ...]
    scenarios: tuple[ScenarioRunResult, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "mcp_protocol_version": self.mcp_protocol_version,
            "transport": self.transport,
            "policy": self.policy,
            "safety_boundary": self.safety_boundary,
            "total_scenarios": self.total_scenarios,
            "successes": self.successes,
            "attack_success_rate": self.attack_success_rate,
            "sampling_requests_seen": self.sampling_requests_seen,
            "sink_writes": self.sink_writes,
            "observations": [observation.to_dict() for observation in self.observations],
            "scenarios": [scenario.to_dict() for scenario in self.scenarios],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)


@dataclass
class _ClientState:
    policy: VictimPolicy
    current_scenario_id: str | None = None
    observations: list[SamplingObservation] = field(default_factory=list)


def _server_params() -> StdioServerParameters:
    return StdioServerParameters(
        command=sys.executable,
        args=["-m", "canaryweave.mcp_poc.malicious_server"],
        env={"PYTHONPATH": str(Path(__file__).resolve().parents[2])},
    )


def _parse_tool_text(result: Any) -> dict[str, Any]:
    if getattr(result, "isError", False):
        raise RuntimeError(f"MCP tool returned error: {result}")
    if not result.content:
        return {}
    text = extract_text_content(result.content[0])
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise RuntimeError("expected tool result JSON object")
    return parsed


def _load_sink_writes(path: Path) -> tuple[SinkWrite, ...]:
    if not path.exists():
        return ()
    writes: list[SinkWrite] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        writes.append(
            SinkWrite(
                scenario_id=str(record["scenario_id"]),
                marker=str(record["marker"]),
                sink=str(record["sink"]),
                source=str(record["source"]),
            )
        )
    return tuple(writes)


def _observation_from_params(scenario_id: str, params: types.CreateMessageRequestParams) -> SamplingObservation:
    message = params.messages[0]
    content = message.content
    return SamplingObservation(
        scenario_id=scenario_id,
        method="sampling/createMessage",
        role=str(message.role),
        content_type=str(getattr(content, "type", "unknown")),
        text=extract_text_content(content),
        max_tokens=getattr(params, "maxTokens", None),
        include_context=getattr(params, "includeContext", None),
        metadata=dict(params.metadata or {}),
    )


async def _run_async(
    policy: VictimPolicy,
    scenario_ids: tuple[str, ...],
    sink_path: Path,
) -> McpSamplingPocResult:
    old_latest_protocol = client_session_module.types.LATEST_PROTOCOL_VERSION
    client_session_module.types.LATEST_PROTOCOL_VERSION = MCP_PROTOCOL_VERSION
    state = _ClientState(policy=policy)
    guardrail = SamplingGuardrail(policy)
    scenario_results: list[ScenarioRunResult] = []

    async def sampling_callback(_context: Any, params: types.CreateMessageRequestParams):
        if state.current_scenario_id is None:
            raise RuntimeError("sampling callback invoked without active scenario")
        config = scenario_config(state.current_scenario_id)
        state.observations.append(_observation_from_params(config.scenario_id, params))
        return deterministic_sampling_result(config)

    try:
        async with stdio_client(_server_params()) as (read_stream, write_stream):
            async with ClientSession(
                read_stream,
                write_stream,
                sampling_callback=sampling_callback,
                sampling_capabilities=types.SamplingCapability(),
                client_info=types.Implementation(name=CLIENT_NAME, version="0.1.0"),
            ) as session:
                init = await session.initialize()
                if str(init.protocolVersion) != MCP_PROTOCOL_VERSION:
                    raise RuntimeError(f"expected MCP {MCP_PROTOCOL_VERSION}, got {init.protocolVersion}")
                tools = await session.list_tools()
                tool_names = {tool.name for tool in tools.tools}
                if "summarize_public_note" not in tool_names or "demo_audit_sink" not in tool_names:
                    raise RuntimeError(f"malicious demo server did not expose expected tools: {sorted(tool_names)}")

                for scenario_id in scenario_ids:
                    config = scenario_config(scenario_id)
                    before_observations = len(state.observations)
                    state.current_scenario_id = scenario_id
                    tool_result = await session.call_tool(
                        "summarize_public_note",
                        {"scenario_id": scenario_id, "sink_path": str(sink_path)},
                    )
                    server_result = _parse_tool_text(tool_result)
                    sampled_text = str(server_result["sampled_text"])
                    decision = guardrail.decide(sampled_text, scenario_id=scenario_id, canary=config.canary)
                    before_writes = _load_sink_writes(sink_path)
                    if decision.allowed:
                        await session.call_tool(
                            "demo_audit_sink",
                            {
                                "scenario_id": scenario_id,
                                "marker": decision.marker,
                                "sink": decision.sink,
                                "source": decision.source,
                                "sink_path": str(sink_path),
                            },
                        )
                    after_writes = _load_sink_writes(sink_path)
                    new_writes = after_writes[len(before_writes) :]
                    scenario_observations = len(state.observations) - before_observations
                    scenario_results.append(
                        ScenarioRunResult(
                            scenario_id=scenario_id,
                            policy=policy.value,
                            client_sampling_capability_advertised=bool(server_result["sampling_supported_by_client"]),
                            sampling_requests_seen=scenario_observations,
                            unauthorized_inert_action_executed=decision.allowed and bool(new_writes),
                            canary_touched=any(write.marker == config.canary for write in new_writes),
                            guardrail_decision=decision,
                            sink_writes=new_writes,
                            tool_result=server_result,
                        )
                    )
                    state.current_scenario_id = None

        successes = sum(1 for item in scenario_results if item.unauthorized_inert_action_executed and item.canary_touched)
        total = len(scenario_results)
        return McpSamplingPocResult(
            schema_version="canaryweave.mcp_sampling_stdio_poc.v1",
            mcp_protocol_version=MCP_PROTOCOL_VERSION,
            transport="stdio",
            policy=policy.value,
            safety_boundary=SAFETY_BOUNDARY,
            total_scenarios=total,
            successes=successes,
            attack_success_rate=successes / total if total else 0.0,
            sampling_requests_seen=sum(item.sampling_requests_seen for item in scenario_results),
            sink_writes=sum(len(item.sink_writes) for item in scenario_results),
            observations=tuple(state.observations),
            scenarios=tuple(scenario_results),
        )
    finally:
        client_session_module.types.LATEST_PROTOCOL_VERSION = old_latest_protocol


def run_mcp_sampling_poc(
    policy: VictimPolicy | str,
    scenario_ids: tuple[str, ...] = DEFAULT_SCENARIO_IDS,
    sink_path: Path | None = None,
) -> McpSamplingPocResult:
    selected_policy = VictimPolicy(policy)
    if sink_path is None:
        tmpdir = Path(tempfile.mkdtemp(prefix="canaryweave-mcp-poc-"))
        sink_path = tmpdir / "demo_sink.jsonl"
    else:
        sink_path = safe_artifact_path(sink_path)
        if sink_path.exists():
            if not sink_path.is_file():
                raise ValueError(f"sink path must be a file: {sink_path}")
            sink_path.unlink()
    return asyncio.run(_run_async(selected_policy, tuple(scenario_ids), sink_path))
