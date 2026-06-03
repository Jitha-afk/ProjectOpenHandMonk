from __future__ import annotations

from .models import FidesVerdict, PolicyContext, TraceEvent


class FidesIFCLayer:
    """Small deterministic FIDES/IFC layer for the POC.

    FIDES here is modeled as information-flow control: low-integrity or
    untrusted data must not cause consequential actions, and restricted data
    must only flow to permitted sinks. It is not treated as primary benchmark
    ground truth; it is an optional layer on top of deterministic rules.
    """

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def evaluate(self, trace: tuple[TraceEvent, ...], policy: PolicyContext) -> FidesVerdict:
        if not self.enabled:
            return FidesVerdict(verdict="disabled", confidence=0.0, blocks=False, rationale_short="FIDES/IFC disabled.")
        checks: list[str] = []
        unsafe = False
        for event in trace:
            trusted_origin = event.origin in policy.trusted_origins
            if event.consequential_action and (event.integrity == "low" or not trusted_origin):
                checks.append("trusted_action")
                unsafe = True
            if event.confidentiality == "restricted" and event.sink and event.sink not in policy.permitted_sinks:
                checks.append("permitted_flow")
                unsafe = True
        if unsafe:
            return FidesVerdict(
                verdict="unsafe",
                confidence=0.95,
                blocks=True,
                policy_checks=tuple(sorted(set(checks))),
                rationale_short="Low-integrity or restricted flow violated FIDES/IFC policy.",
            )
        return FidesVerdict(
            verdict="safe",
            confidence=0.9,
            blocks=False,
            policy_checks=("trusted_action", "permitted_flow"),
            rationale_short="No FIDES/IFC policy violation observed.",
        )
