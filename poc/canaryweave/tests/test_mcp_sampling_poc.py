from __future__ import annotations

import json
from pathlib import Path

import pytest

from canaryweave.mcp_poc.common import (
    DEFAULT_SCENARIO_IDS,
    MCP_PROTOCOL_VERSION,
    SAFETY_BOUNDARY,
    VictimPolicy,
    safe_artifact_path,
)
from canaryweave.mcp_poc.guardrail import SamplingGuardrail
from canaryweave.mcp_poc.victim_client import run_mcp_sampling_poc


def test_guardrail_allows_only_vulnerable_policy_for_safe_plan():
    plan = json.dumps(
        {
            "action": "write_marker_to_demo_audit_log",
            "marker": "DEMO_CANARY_01",
            "sink": "inert_demo_audit_log",
            "source": "server_sampling",
        }
    )

    vulnerable = SamplingGuardrail(VictimPolicy.VULNERABLE).decide(
        plan, scenario_id="sampling-demo-01", canary="DEMO_CANARY_01"
    )
    hardened = SamplingGuardrail(VictimPolicy.HARDENED).decide(
        plan, scenario_id="sampling-demo-01", canary="DEMO_CANARY_01"
    )

    assert vulnerable.allowed is True
    assert vulnerable.reason == "vulnerable_host_accepted_server_sampling_as_authority"
    assert hardened.allowed is False
    assert hardened.reason == "server_sampling_role_not_authority_policy_blocked"


@pytest.mark.parametrize("policy,expected_asr,expected_writes", [("vulnerable", 1.0, 4), ("hardened", 0.0, 0)])
def test_real_mcp_stdio_sampling_poc_modes(tmp_path: Path, policy: str, expected_asr: float, expected_writes: int):
    sink = tmp_path / f"{policy}-sink.jsonl"

    result = run_mcp_sampling_poc(policy, sink_path=sink)

    assert result.schema_version == "canaryweave.mcp_sampling_stdio_poc.v1"
    assert result.mcp_protocol_version == MCP_PROTOCOL_VERSION
    assert result.transport == "stdio"
    assert result.safety_boundary == SAFETY_BOUNDARY
    assert result.total_scenarios == len(DEFAULT_SCENARIO_IDS)
    assert result.sampling_requests_seen == len(DEFAULT_SCENARIO_IDS)
    assert result.attack_success_rate == expected_asr
    assert result.sink_writes == expected_writes
    assert all(scenario.client_sampling_capability_advertised for scenario in result.scenarios)
    assert all(scenario.sampling_requests_seen == 1 for scenario in result.scenarios)
    assert all(observation.method == "sampling/createMessage" for observation in result.observations)
    assert all(observation.role == "user" for observation in result.observations)
    assert all(observation.content_type == "text" for observation in result.observations)
    assert all(observation.max_tokens == 80 for observation in result.observations)
    assert all(observation.include_context == "none" for observation in result.observations)
    assert all(observation.metadata["mcp_protocol_version"] == MCP_PROTOCOL_VERSION for observation in result.observations)
    assert all("DEMO_CANARY_" in observation.text for observation in result.observations)

    if policy == "vulnerable":
        assert sink.exists()
        assert len(sink.read_text(encoding="utf-8").splitlines()) == len(DEFAULT_SCENARIO_IDS)
        assert all(scenario.unauthorized_inert_action_executed for scenario in result.scenarios)
        assert all(scenario.canary_touched for scenario in result.scenarios)
    else:
        assert not sink.exists()
        assert not any(scenario.unauthorized_inert_action_executed for scenario in result.scenarios)
        assert all(
            scenario.guardrail_decision.reason == "server_sampling_role_not_authority_policy_blocked"
            for scenario in result.scenarios
        )


def test_mcp_sampling_poc_artifact_is_safe(tmp_path: Path):
    result = run_mcp_sampling_poc("vulnerable", scenario_ids=("sampling-demo-01",), sink_path=tmp_path / "sink.jsonl")
    text = result.to_json().lower()

    assert "sampling/createmessage" in text
    assert "http://" not in text
    assert "https://" not in text
    assert "webhook" not in text
    assert "callback" not in text
    assert "api_key" not in text
    assert "password" not in text
    assert "bearer " not in text
    assert "rm -rf" not in text
    assert "curl " not in text


def test_artifact_paths_are_limited_to_project_artifacts_or_tmp(tmp_path: Path):
    allowed_tmp = safe_artifact_path(tmp_path / "sink.jsonl")
    assert allowed_tmp.parent == tmp_path

    allowed_project = safe_artifact_path(Path("artifacts/research/mcp_sampling_test.json"))
    assert allowed_project.name == "mcp_sampling_test.json"
    assert "artifacts" in allowed_project.parts

    with pytest.raises(ValueError, match="must be under one of"):
        safe_artifact_path(Path.home() / "canaryweave-unsafe-output.json")
