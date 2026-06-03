from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class _StringEnum(str, Enum):
    @classmethod
    def coerce(cls, value: Any) -> Any:
        if isinstance(value, cls):
            return value
        return cls(str(value))


class CaseKind(_StringEnum):
    ATTACK = "attack"
    BENIGN = "benign"


class ExpectedBehavior(_StringEnum):
    ALLOW = "allow"
    QUARANTINE = "quarantine"
    BLOCK = "block"


_PRIVATE_KEYS = {"raw_ref", "private_data"}


def _as_mapping(value: Mapping[str, Any] | Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return dict(value)
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        converted = to_dict()
        if isinstance(converted, Mapping):
            return dict(converted)
    return dict(value)


def _public_safe(value: Any) -> Any:
    """Return a JSON-safe value with private adapter fields removed."""
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {
            str(key): _public_safe(item)
            for key, item in value.items()
            if str(key) not in _PRIVATE_KEYS and not str(key).startswith("_")
        }
    if isinstance(value, (tuple, list, set, frozenset)):
        return [_public_safe(item) for item in value]
    return value


@dataclass(frozen=True)
class AttackCase:
    """Dataset-neutral case envelope.

    raw_ref and private_data are intentionally available for local adapters and
    intentionally absent from to_dict(), the public artifact representation.
    """

    case_id: str
    dataset_id: str
    split: str
    case_kind: CaseKind | str
    attack_category: str
    surface: str
    safe_features: Mapping[str, Any] = field(default_factory=dict)
    policy_context: Mapping[str, Any] = field(default_factory=dict)
    expected_behavior: ExpectedBehavior | str = ExpectedBehavior.ALLOW
    iteration_seed: int | None = None
    raw_ref: str | None = field(default=None, repr=False, compare=False)
    private_data: Mapping[str, Any] = field(default_factory=dict, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "case_id", str(self.case_id))
        object.__setattr__(self, "dataset_id", str(self.dataset_id))
        object.__setattr__(self, "split", str(self.split))
        object.__setattr__(self, "case_kind", CaseKind.coerce(self.case_kind))
        object.__setattr__(self, "attack_category", str(self.attack_category))
        object.__setattr__(self, "surface", str(self.surface))
        object.__setattr__(self, "expected_behavior", ExpectedBehavior.coerce(self.expected_behavior))
        object.__setattr__(self, "safe_features", _as_mapping(self.safe_features))
        object.__setattr__(self, "policy_context", _as_mapping(self.policy_context))
        object.__setattr__(self, "private_data", _as_mapping(self.private_data))
        if self.iteration_seed is not None:
            object.__setattr__(self, "iteration_seed", int(self.iteration_seed))
        if self.raw_ref is not None:
            object.__setattr__(self, "raw_ref", str(self.raw_ref))

    def to_dict(self) -> dict[str, Any]:
        """Public, JSON-safe export. Private raw custody fields are excluded."""
        case_kind = CaseKind.coerce(self.case_kind)
        expected_behavior = ExpectedBehavior.coerce(self.expected_behavior)
        return {
            "case_id": self.case_id,
            "dataset_id": self.dataset_id,
            "split": self.split,
            "case_kind": case_kind.value,
            "attack_category": self.attack_category,
            "surface": self.surface,
            "iteration_seed": self.iteration_seed,
            "safe_features": _public_safe(self.safe_features),
            "policy_context": _public_safe(self.policy_context),
            "expected_behavior": expected_behavior.value,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AttackCase":
        required = (
            "case_id",
            "dataset_id",
            "split",
            "case_kind",
            "attack_category",
            "surface",
            "expected_behavior",
        )
        missing = [key for key in required if key not in data]
        if missing:
            raise ValueError(f"AttackCase missing required fields: {', '.join(missing)}")
        return cls(
            case_id=str(data["case_id"]),
            dataset_id=str(data["dataset_id"]),
            split=str(data["split"]),
            case_kind=data["case_kind"],
            attack_category=str(data["attack_category"]),
            surface=str(data["surface"]),
            iteration_seed=data.get("iteration_seed"),
            safe_features=_as_mapping(data.get("safe_features", {})),
            policy_context=_as_mapping(data.get("policy_context", {})),
            expected_behavior=data["expected_behavior"],
            raw_ref=data.get("raw_ref"),
            private_data=_as_mapping(data.get("private_data", {})),
        )
