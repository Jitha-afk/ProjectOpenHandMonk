from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from .models import PolicyContext, RuleDecision, RuleHit, TraceEvent
from .normalization import has_hidden_unicode_structure, has_untrusted_instruction_shape
from .rule_schema import RuleDefinition, SignalDefinition


class RuleEngineError(ValueError):
    pass


class RuleEngine:
    def __init__(self, rules: Iterable[RuleDefinition]):
        self.rules = tuple(rules)

    def evaluate(self, trace: Iterable[TraceEvent], policy: PolicyContext | None = None) -> RuleDecision:
        events = tuple(trace)
        ctx = policy or PolicyContext()
        hits: list[RuleHit] = []
        for rule in self.rules:
            signal_values = {signal.name: self._eval_signal(signal, events, ctx) for signal in rule.signals}
            if self._eval_condition(rule.condition, signal_values):
                matched = tuple(name for name, value in signal_values.items() if value)
                hits.append(RuleHit(
                    rule_id=rule.id,
                    rule_name=rule.name,
                    category=rule.category,
                    severity=rule.severity,
                    action=rule.recommended_action,
                    matched_signals=matched,
                    evidence={"scope": rule.scope},
                ))
        final_action = self._final_action(hits)
        return RuleDecision(hits=tuple(hits), final_action=final_action)

    def _eval_signal(self, signal: SignalDefinition, events: tuple[TraceEvent, ...], policy: PolicyContext) -> bool:
        params = signal.params
        if signal.type == "event_field_equals":
            field = str(params["field"])
            value = params["value"]
            return any(event.field_value(field) == value for event in events)
        if signal.type == "event_field_in":
            field = str(params["field"])
            values = set(params.get("values", []))
            return any(event.field_value(field) in values for event in events)
        if signal.type == "schema_shape":
            shape = params.get("shape")
            return any(event.schema_shape == shape for event in events)
        if signal.type == "capability_policy":
            relation = params.get("relation")
            if relation != "not_in_allowed_capabilities":
                raise RuleEngineError(f"Unsupported capability relation: {relation}")
            return any(
                event.capability is not None and event.capability not in policy.allowed_capabilities
                for event in events
            )
        if signal.type == "canary_flow":
            relation = params.get("relation")
            if relation != "outside_allowed_sink":
                raise RuleEngineError(f"Unsupported canary relation: {relation}")
            return any(
                event.canary_present and event.sink not in policy.allowed_canary_sinks
                for event in events
            )
        if signal.type == "text_structure":
            feature = params.get("feature")
            if feature == "hidden_unicode":
                return any(has_hidden_unicode_structure(event.text) for event in events)
            if feature == "untrusted_instruction_shape":
                return any(has_untrusted_instruction_shape(event.text) for event in events)
            raise RuleEngineError(f"Unsupported text feature: {feature}")
        raise RuleEngineError(f"Unsupported signal type: {signal.type}")

    def _eval_condition(self, condition: str, values: dict[str, bool]) -> bool:
        def replace(match: re.Match[str]) -> str:
            token = match.group(0)
            lower = token.lower()
            if lower in {"and", "or", "not", "true", "false"}:
                return lower.title() if lower in {"true", "false"} else lower
            if token not in values:
                raise RuleEngineError(f"Unknown condition token: {token}")
            return "True" if values[token] else "False"

        expr = re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*\b", replace, condition)
        if not re.fullmatch(r"[TrueFalsandornt ()]+", expr):
            raise RuleEngineError(f"Unsafe condition expression: {condition}")
        return bool(eval(expr, {"__builtins__": {}}, {}))

    def _final_action(self, hits: list[RuleHit]) -> str:
        if any(hit.action == "block_and_audit" or hit.severity == "critical" for hit in hits):
            return "block"
        if any(hit.action == "quarantine" for hit in hits):
            return "quarantine"
        return "allow"
