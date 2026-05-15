from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Mapping, Tuple


class Mode(str, Enum):
    """Supported benchmark execution conditions."""

    BASELINE = "baseline"
    MCP = "mcp"
    ATTEST = "attest"


class ActionKind(str, Enum):
    """Semantic labels used by the deterministic evaluator."""

    ALLOWED = "allowed"
    UNAUTHORIZED = "unauthorized"
    DECOY = "decoy"


@dataclass(frozen=True)
class ToolAction:
    """A symbolic, inert tool action in a synthetic scenario."""

    name: str
    capability: str
    args: Mapping[str, str]
    kind: ActionKind

    def __post_init__(self) -> None:
        object.__setattr__(self, "args", MappingProxyType(dict(self.args)))


@dataclass(frozen=True)
class Scenario:
    """A deterministic, synthetic protocol-confusion test case."""

    id: str
    seed: int
    user_goal: str
    context: str
    allowed_capabilities: Tuple[str, ...]
    canaries: Tuple[str, ...]
    actions: Tuple[ToolAction, ...]
    expected_unauthorized: Tuple[str, ...]
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "allowed_capabilities", tuple(self.allowed_capabilities))
        object.__setattr__(self, "canaries", tuple(self.canaries))
        object.__setattr__(self, "actions", tuple(self.actions))
        object.__setattr__(self, "expected_unauthorized", tuple(self.expected_unauthorized))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
