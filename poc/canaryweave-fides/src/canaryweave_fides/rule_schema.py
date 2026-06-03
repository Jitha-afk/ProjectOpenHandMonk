from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any


class RuleValidationError(ValueError):
    pass


_ALLOWED_SEVERITIES = {"low", "medium", "high", "critical"}
_ALLOWED_ACTIONS = {"allow", "audit", "quarantine", "block_and_audit"}
_REQUIRED_FIELDS = {
    "id", "name", "version", "category", "severity", "scope", "description",
    "signals", "condition", "recommended_action", "fixtures", "safety_notes",
}
_BOOLEAN_WORDS = {"and", "or", "not", "true", "false"}
_IDENTIFIER_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")


@dataclass(frozen=True)
class SignalDefinition:
    name: str
    type: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RuleDefinition:
    id: str
    name: str
    version: str
    category: str
    severity: str
    scope: str
    description: str
    signals: tuple[SignalDefinition, ...]
    condition: str
    recommended_action: str
    fixtures: dict[str, list[str]]
    safety_notes: str


def _condition_identifiers(condition: str) -> set[str]:
    return {token for token in _IDENTIFIER_RE.findall(condition) if token.lower() not in _BOOLEAN_WORDS}


def validate_rule(data: dict[str, Any]) -> RuleDefinition:
    missing = sorted(_REQUIRED_FIELDS - set(data))
    if missing:
        raise RuleValidationError(f"Missing required rule fields: {missing}")
    severity = str(data["severity"])
    if severity not in _ALLOWED_SEVERITIES:
        raise RuleValidationError(f"Invalid severity: {severity}")
    action = str(data["recommended_action"])
    if action not in _ALLOWED_ACTIONS:
        raise RuleValidationError(f"Invalid recommended_action: {action}")
    raw_signals = data["signals"]
    if not isinstance(raw_signals, list) or not raw_signals:
        raise RuleValidationError("signals must be a non-empty list")
    signals: list[SignalDefinition] = []
    seen: set[str] = set()
    for raw in raw_signals:
        if not isinstance(raw, dict) or "name" not in raw or "type" not in raw:
            raise RuleValidationError("every signal needs name and type")
        name = str(raw["name"])
        if name in seen:
            raise RuleValidationError(f"Duplicate signal name: {name}")
        seen.add(name)
        params = {k: v for k, v in raw.items() if k not in {"name", "type"}}
        signals.append(SignalDefinition(name=name, type=str(raw["type"]), params=params))
    referenced = _condition_identifiers(str(data["condition"]))
    unknown = sorted(referenced - seen)
    if unknown:
        raise RuleValidationError(f"Condition references unknown signals: {', '.join(unknown)}")
    safety_notes = str(data["safety_notes"])
    if not safety_notes.strip():
        raise RuleValidationError("safety_notes is required")
    fixtures = data.get("fixtures") or {}
    return RuleDefinition(
        id=str(data["id"]),
        name=str(data["name"]),
        version=str(data["version"]),
        category=str(data["category"]),
        severity=severity,
        scope=str(data["scope"]),
        description=str(data["description"]),
        signals=tuple(signals),
        condition=str(data["condition"]),
        recommended_action=action,
        fixtures={"positive": list(fixtures.get("positive", [])), "negative": list(fixtures.get("negative", []))},
        safety_notes=safety_notes,
    )
