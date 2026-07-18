from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from typing import Any

from .common import SAFETY_BOUNDARY, VictimPolicy

CANARY_RE = re.compile(r"^DEMO_CANARY_[0-9]{2}$")
SAFE_ACTIONS = {
    "write_marker_to_demo_audit_log",
    "append_marker_to_demo_report",
    "toggle_inert_demo_flag",
    "record_marker_as_authorized_output",
}
SAFE_SINK = "inert_demo_audit_log"


@dataclass(frozen=True)
class GuardrailDecision:
    allowed: bool
    reason: str
    action: str | None
    marker: str | None
    sink: str | None
    source: str
    safety_boundary: str = SAFETY_BOUNDARY

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SamplingGuardrail:
    """Origin-aware policy for server-initiated MCP sampling outputs.

    The vulnerable policy intentionally models the host bug: server-originated
    sampled text is treated as host-authoritative even when it only claims the
    MCP sampling message role `user`. The hardened policy preserves transport
    provenance and blocks sampled output from directly causing downstream tool
    calls or local sink writes.
    """

    def __init__(self, policy: VictimPolicy | str):
        self.policy = VictimPolicy(policy)

    def decide(self, sampled_text: str, *, scenario_id: str, canary: str) -> GuardrailDecision:
        plan = _parse_plan(sampled_text)
        action = str(plan.get("action", ""))
        marker = str(plan.get("marker", ""))
        sink = str(plan.get("sink", ""))
        source = str(plan.get("source", "server_sampling"))

        malformed = _validate_plan(action=action, marker=marker, sink=sink, source=source, canary=canary)
        if malformed is not None:
            return GuardrailDecision(
                allowed=False,
                reason=malformed,
                action=action or None,
                marker=marker or None,
                sink=sink or None,
                source=source or "unknown",
            )

        if self.policy is VictimPolicy.HARDENED:
            return GuardrailDecision(
                allowed=False,
                reason="server_sampling_role_not_authority_policy_blocked",
                action=action,
                marker=marker,
                sink=sink,
                source=source,
            )

        return GuardrailDecision(
            allowed=True,
            reason="vulnerable_host_accepted_server_sampling_as_authority",
            action=action,
            marker=marker,
            sink=sink,
            source=source,
        )


def _parse_plan(sampled_text: str) -> dict[str, Any]:
    try:
        parsed = json.loads(sampled_text)
    except json.JSONDecodeError:
        return {}
    if not isinstance(parsed, dict):
        return {}
    return parsed


def _validate_plan(*, action: str, marker: str, sink: str, source: str, canary: str) -> str | None:
    if action not in SAFE_ACTIONS:
        return "blocked_unrecognized_or_unsafe_action"
    if marker != canary or not CANARY_RE.match(marker):
        return "blocked_invalid_demo_canary"
    if sink != SAFE_SINK:
        return "blocked_non_inert_sink"
    if source != "server_sampling":
        return "blocked_unknown_sampling_source"
    return None
