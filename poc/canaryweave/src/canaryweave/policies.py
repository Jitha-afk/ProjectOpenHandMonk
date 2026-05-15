from __future__ import annotations

from dataclasses import dataclass

from .scenario import ActionKind, ToolAction


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str


@dataclass(frozen=True)
class Policy:
    """Symbolic allow/deny policy for the toy host simulator."""

    allowed_capabilities: tuple[str, ...]
    allow_decoys: bool = False

    def decide(self, action: ToolAction) -> PolicyDecision:
        if action.kind is ActionKind.UNAUTHORIZED:
            return PolicyDecision(False, "denied_unauthorized_kind")
        if action.kind is ActionKind.DECOY and not self.allow_decoys:
            return PolicyDecision(False, "denied_decoy")
        if action.capability not in self.allowed_capabilities:
            return PolicyDecision(False, "denied_missing_capability")
        return PolicyDecision(True, "allowed_capability")
