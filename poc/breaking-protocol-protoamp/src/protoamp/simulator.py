from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .attest import sign_capability, verify_capability
from .events import Event, JsonRpcEventLogger
from .policies import Policy
from .safety import validate_scenario
from .scenario import ActionKind, Mode, Scenario, ToolAction

DEFAULT_SECRET = b"protoamp-test-secret"


@dataclass(frozen=True)
class ActionResult:
    action: ToolAction
    executed: bool
    reason: str
    canary_touched: bool


@dataclass(frozen=True)
class ScenarioResult:
    scenario_id: str
    mode: Mode
    action_results: tuple[ActionResult, ...]

    @property
    def unauthorized_executed(self) -> bool:
        return any(
            result.executed and result.action.kind is ActionKind.UNAUTHORIZED
            for result in self.action_results
        )

    @property
    def canary_touched(self) -> bool:
        return any(result.executed and result.canary_touched for result in self.action_results)


def _action_touches_canary(action: ToolAction, scenario: Scenario) -> bool:
    values = "\n".join(str(value) for value in action.args.values())
    return any(canary in values for canary in scenario.canaries)


class HostSimulator:
    """Pure-Python toy host for baseline, MCP-policy, and attest modes."""

    def __init__(
        self,
        mode: Mode,
        secret: bytes = DEFAULT_SECRET,
        logger: JsonRpcEventLogger | None = None,
    ):
        self.mode = Mode(mode)
        self.secret = secret
        self.logger = logger

    def run(self, scenario: Scenario) -> ScenarioResult:
        validate_scenario(scenario)
        policy = Policy(allowed_capabilities=scenario.allowed_capabilities)
        results: list[ActionResult] = []
        for sequence, action in enumerate(scenario.actions, start=1):
            executed, reason = self._decide(policy, scenario, action)
            canary_touched = executed and _action_touches_canary(action, scenario)
            result = ActionResult(action, executed, reason, canary_touched)
            results.append(result)
            if self.logger is not None:
                self.logger.log(
                    Event(
                        event_type="decision",
                        scenario_id=scenario.id,
                        mode=self.mode.value,
                        action=action.name,
                        capability=action.capability,
                        allowed=executed,
                        reason=reason,
                        canary_touched=canary_touched,
                        sequence=sequence,
                    )
                )
        return ScenarioResult(scenario.id, self.mode, tuple(results))

    def _decide(self, policy: Policy, scenario: Scenario, action: ToolAction) -> tuple[bool, str]:
        decision = policy.decide(action)

        if self.mode is Mode.BASELINE:
            # Direct function-call baseline: only the semantic action required by
            # the user task is available. Protocol-specific candidate actions are
            # not exposed, so they cannot execute.
            return decision.allowed, f"baseline_{decision.reason}"

        if self.mode is Mode.MCP:
            # Unprotected MCP-style condition: all server-proposed JSON-RPC-shaped
            # candidate actions are accepted. This intentionally models absence
            # of message-level capability attestation/origin enforcement.
            return True, "mcp_unprotected_allows_server_action"

        if self.mode is Mode.ATTEST:
            if not decision.allowed:
                return False, "denied_policy_before_attestation"
            nonce = f"nonce-{scenario.id}-{action.name}"
            attestation = sign_capability(
                self.secret, scenario.id, action.name, action.capability, nonce
            )
            if verify_capability(self.secret, attestation):
                return True, "attestation_valid"
            return False, "denied_missing_or_invalid_attestation"

        raise ValueError(f"unsupported mode: {self.mode}")


def run_suite(
    scenarios: Sequence[Scenario],
    mode: Mode,
    logger: JsonRpcEventLogger | None = None,
) -> list[ScenarioResult]:
    simulator = HostSimulator(mode=mode, logger=logger)
    return [simulator.run(scenario) for scenario in scenarios]
