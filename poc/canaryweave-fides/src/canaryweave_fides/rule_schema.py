from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any


class RuleValidationError(ValueError):
    pass


_ALLOWED_SEVERITIES = {"low", "medium", "high", "critical"}
_ALLOWED_ACTIONS = {"allow", "audit", "quarantine", "block_and_audit"}
_ALLOWED_NAMESPACES = {"signals", "keywords", "semantics", "fides"}
_REQUIRED_FIELDS = {
    "id", "name", "version", "category", "severity", "scope", "description",
    "signals", "condition", "recommended_action", "fixtures", "safety_notes",
}
_BOOLEAN_WORDS = {"and", "or", "not", "true", "false"}
_NAMESPACED_REF_RE = re.compile(r"\b(signals|keywords|semantics|fides)\.([A-Za-z_][A-Za-z0-9_]*)\b")
_IDENTIFIER_RE = re.compile(r"(?<!\.)\b[A-Za-z_][A-Za-z0-9_]*\b")


@dataclass(frozen=True)
class SignalDefinition:
    name: str
    type: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KeywordPattern:
    name: str
    type: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SemanticPattern:
    name: str
    description: str
    threshold: float
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FidesCheck:
    name: str
    prompt: str
    threshold: float
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
    meta: dict[str, Any] = field(default_factory=dict)
    keywords: tuple[KeywordPattern, ...] = ()
    semantics: tuple[SemanticPattern, ...] = ()
    fides_checks: tuple[FidesCheck, ...] = ()


def _threshold(value: Any, section: str, name: str) -> float:
    try:
        threshold = float(value)
    except (TypeError, ValueError) as exc:
        raise RuleValidationError(f"{section}.{name} threshold must be numeric") from exc
    if not 0.0 <= threshold <= 1.0:
        raise RuleValidationError(f"{section}.{name} threshold must be between 0.0 and 1.0")
    return threshold


def _parse_signals(raw_signals: Any) -> tuple[SignalDefinition, ...]:
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
    return tuple(signals)


def _parse_keywords(raw_keywords: Any) -> tuple[KeywordPattern, ...]:
    if raw_keywords is None:
        return ()
    if not isinstance(raw_keywords, list):
        raise RuleValidationError("keywords must be a list")
    patterns: list[KeywordPattern] = []
    seen: set[str] = set()
    for raw in raw_keywords:
        if not isinstance(raw, dict) or "name" not in raw or "type" not in raw:
            raise RuleValidationError("every keyword needs name and type")
        name = str(raw["name"])
        if name in seen:
            raise RuleValidationError(f"Duplicate keyword name: {name}")
        seen.add(name)
        kind = str(raw["type"])
        if kind not in {"exact", "regex", "feature"}:
            raise RuleValidationError(f"Unsupported keyword type: {kind}")
        params = {k: v for k, v in raw.items() if k not in {"name", "type"}}
        if kind in {"exact", "regex"} and not ("pattern" in params or "value" in params):
            raise RuleValidationError(f"keyword {name} requires pattern or value")
        patterns.append(KeywordPattern(name=name, type=kind, params=params))
    return tuple(patterns)


def _parse_semantics(raw_semantics: Any) -> tuple[SemanticPattern, ...]:
    if raw_semantics is None:
        return ()
    if not isinstance(raw_semantics, list):
        raise RuleValidationError("semantics must be a list")
    patterns: list[SemanticPattern] = []
    seen: set[str] = set()
    for raw in raw_semantics:
        if not isinstance(raw, dict) or "name" not in raw or "description" not in raw:
            raise RuleValidationError("every semantic pattern needs name and description")
        name = str(raw["name"])
        if name in seen:
            raise RuleValidationError(f"Duplicate semantic name: {name}")
        seen.add(name)
        threshold = _threshold(raw.get("threshold", 0.5), "semantics", name)
        params = {k: v for k, v in raw.items() if k not in {"name", "description", "threshold"}}
        patterns.append(SemanticPattern(name=name, description=str(raw["description"]), threshold=threshold, params=params))
    return tuple(patterns)


def _parse_fides(raw_fides: Any) -> tuple[FidesCheck, ...]:
    if raw_fides is None:
        return ()
    if not isinstance(raw_fides, list):
        raise RuleValidationError("fides must be a list")
    checks: list[FidesCheck] = []
    seen: set[str] = set()
    for raw in raw_fides:
        if not isinstance(raw, dict) or "name" not in raw or "prompt" not in raw:
            raise RuleValidationError("every fides check needs name and prompt")
        name = str(raw["name"])
        if name in seen:
            raise RuleValidationError(f"Duplicate fides check name: {name}")
        seen.add(name)
        threshold = _threshold(raw.get("threshold", 0.5), "fides", name)
        params = {k: v for k, v in raw.items() if k not in {"name", "prompt", "threshold"}}
        checks.append(FidesCheck(name=name, prompt=str(raw["prompt"]), threshold=threshold, params=params))
    return tuple(checks)


def _condition_references(condition: str) -> set[str]:
    refs = {f"{namespace}.{name}" for namespace, name in _NAMESPACED_REF_RE.findall(condition)}
    stripped = _NAMESPACED_REF_RE.sub(" ", condition)
    refs.update(
        token for token in _IDENTIFIER_RE.findall(stripped)
        if token.lower() not in _BOOLEAN_WORDS and token not in _ALLOWED_NAMESPACES
    )
    return refs


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

    signals = _parse_signals(data["signals"])
    keywords = _parse_keywords(data.get("keywords"))
    semantics = _parse_semantics(data.get("semantics"))
    fides_checks = _parse_fides(data.get("fides"))

    names_by_namespace = {
        "signals": {item.name for item in signals},
        "keywords": {item.name for item in keywords},
        "semantics": {item.name for item in semantics},
        "fides": {item.name for item in fides_checks},
    }
    valid_refs = set(names_by_namespace["signals"])
    for namespace, names in names_by_namespace.items():
        valid_refs.update(f"{namespace}.{name}" for name in names)

    referenced = _condition_references(str(data["condition"]))
    unknown = sorted(referenced - valid_refs)
    if unknown:
        raise RuleValidationError(f"Condition references unknown rule terms: {', '.join(unknown)}")

    safety_notes = str(data["safety_notes"])
    if not safety_notes.strip():
        raise RuleValidationError("safety_notes is required")
    fixtures = data.get("fixtures") or {}
    meta = data.get("meta") or {}
    if not isinstance(meta, dict):
        raise RuleValidationError("meta must be a mapping when provided")

    return RuleDefinition(
        id=str(data["id"]),
        name=str(data["name"]),
        version=str(data["version"]),
        category=str(data["category"]),
        severity=severity,
        scope=str(data["scope"]),
        description=str(data["description"]),
        signals=signals,
        condition=str(data["condition"]),
        recommended_action=action,
        fixtures={"positive": list(fixtures.get("positive", [])), "negative": list(fixtures.get("negative", []))},
        safety_notes=safety_notes,
        meta=dict(meta),
        keywords=keywords,
        semantics=semantics,
        fides_checks=fides_checks,
    )
