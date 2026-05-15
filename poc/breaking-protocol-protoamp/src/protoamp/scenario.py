from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Mapping, Tuple, Any


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


class AttackType(str, Enum):
    """Safe, protocol-level ASR scenario classes."""

    SAMPLING_ABUSE = "sampling_abuse"
    CAPABILITY_ATTESTATION_ABSENCE = "capability_attestation_absence"
    IMPLICIT_TRUST_PROPAGATION = "implicit_trust_propagation"


class SourceFamily(str, Enum):
    """Where scenario structure came from, without raw payloads."""

    SYNTHETIC_SAFE = "synthetic_safe"
    AGENTDOJO_STRUCTURAL = "agentdojo_structural"
    INJECAGENT_STRUCTURAL = "injecagent_structural"


_DIGEST_RE = re.compile(r"^(synthetic:[a-z0-9_.-]+|sha256:[0-9a-f]{64})$")


@dataclass(frozen=True)
class ScenarioMetadata:
    """Typed metadata for payload-free scenario provenance and taxonomy."""

    scenario_family: str
    attack_type: AttackType
    source_family: SourceFamily
    source_adapter: str
    source_digest: str
    source_record_count: int
    abuse_axis: str
    trust_failure: str
    notes: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "attack_type", AttackType(self.attack_type))
        object.__setattr__(self, "source_family", SourceFamily(self.source_family))
        if self.source_record_count < 0:
            raise ValueError("source_record_count must be non-negative")
        if not _DIGEST_RE.match(self.source_digest):
            raise ValueError("source_digest must be sha256:<64 hex> or synthetic:<label>")
        object.__setattr__(self, "notes", MappingProxyType(dict(self.notes)))


@dataclass(frozen=True)
class ToolAction:
    """A symbolic, inert tool action in a synthetic scenario."""

    name: str
    capability: str
    args: Mapping[str, str]
    kind: ActionKind

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", ActionKind(self.kind))
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
    metadata: ScenarioMetadata | Mapping[str, Any] = field(default_factory=lambda: {"family": "legacy_safe"})

    def __post_init__(self) -> None:
        object.__setattr__(self, "allowed_capabilities", tuple(self.allowed_capabilities))
        object.__setattr__(self, "canaries", tuple(self.canaries))
        object.__setattr__(self, "actions", tuple(self.actions))
        object.__setattr__(self, "expected_unauthorized", tuple(self.expected_unauthorized))
        if not isinstance(self.metadata, ScenarioMetadata):
            legacy_metadata = self.metadata
            # Backward-compatible adapter for old fixtures/callers.
            metadata = ScenarioMetadata(
                scenario_family=str(legacy_metadata.get("family", "legacy_safe")),
                attack_type=AttackType.SAMPLING_ABUSE,
                source_family=SourceFamily.SYNTHETIC_SAFE,
                source_adapter=str(legacy_metadata.get("source", "synthetic_static")),
                source_digest="synthetic:legacy-safe",
                source_record_count=0,
                abuse_axis="legacy_axis",
                trust_failure="legacy_policy_boundary",
                notes={str(k): str(v) for k, v in legacy_metadata.items()},
            )
            object.__setattr__(self, "metadata", metadata)

    @property
    def typed_metadata(self) -> ScenarioMetadata:
        if not isinstance(self.metadata, ScenarioMetadata):
            raise TypeError("scenario metadata was not normalized")
        return self.metadata
