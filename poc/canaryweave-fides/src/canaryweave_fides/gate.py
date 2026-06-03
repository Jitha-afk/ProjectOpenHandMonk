from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence

from .cases import AttackCase
from .decisions import BlockedBy, Decision, FidesVerdict, GateDecision, StackName
from .facts import NormalizedFacts
from .models import PolicyContext, TraceEvent
from .rule_engine import RuleEngine
from .rule_loader import load_rules


class _StringEnum(str, Enum):
    @classmethod
    def coerce(cls, value: Any) -> Any:
        if isinstance(value, cls):
            return value
        return cls(str(value))


class FidesJudgeMode(_StringEnum):
    """Explicit runtime modes for the FIDES LLM-as-judge boundary."""

    DISABLED = "disabled"
    TEST_DOUBLE = "test_double"
    PROVIDER_PLACEHOLDER = "provider_placeholder"


@dataclass(frozen=True)
class FidesJudgeResult:
    verdict: FidesVerdict | str
    confidence: float = 0.0
    reason_codes: tuple[str, ...] = ()
    recommended_decision: Decision | str | None = None
    latency_ms: float | None = None
    provider_calls: int = 0
    judge_transcript: str | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        verdict = FidesVerdict.coerce(self.verdict)
        if verdict == FidesVerdict.NOT_CALLED:
            raise ValueError("FidesJudgeResult verdict cannot be not_called")
        object.__setattr__(self, "verdict", verdict)

        confidence = float(self.confidence)
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        object.__setattr__(self, "confidence", confidence)

        object.__setattr__(self, "reason_codes", tuple(str(code) for code in self.reason_codes))
        if self.recommended_decision is None:
            recommended = _recommended_decision_for_verdict(verdict)
        else:
            recommended = Decision.coerce(self.recommended_decision)
        object.__setattr__(self, "recommended_decision", recommended)

        if self.latency_ms is not None:
            latency_ms = float(self.latency_ms)
            if latency_ms < 0:
                raise ValueError("latency_ms must be non-negative")
            object.__setattr__(self, "latency_ms", latency_ms)

        provider_calls = int(self.provider_calls)
        if provider_calls < 0:
            raise ValueError("provider_calls must be non-negative")
        object.__setattr__(self, "provider_calls", provider_calls)

        if self.judge_transcript is not None:
            object.__setattr__(self, "judge_transcript", str(self.judge_transcript))

    def to_dict(self) -> dict[str, Any]:
        """Public-safe judge result export; no raw transcript is included."""
        verdict = FidesVerdict.coerce(self.verdict)
        recommended = Decision.coerce(self.recommended_decision)
        return {
            "verdict": verdict.value,
            "confidence": self.confidence,
            "reason_codes": list(self.reason_codes),
            "recommended_decision": recommended.value,
            "latency_ms": self.latency_ms,
            "provider_calls": self.provider_calls,
            "transcript_included": False,
        }

    def to_private_dict(self) -> dict[str, Any]:
        data = self.to_dict()
        data["judge_transcript"] = self.judge_transcript
        return data


class FidesJudge(Protocol):
    mode: FidesJudgeMode

    def judge(self, facts: NormalizedFacts) -> FidesJudgeResult:
        ...


class DisabledFidesJudge:
    """FIDES mode for default/public runs: no provider, no transcript."""

    mode = FidesJudgeMode.DISABLED

    def __init__(self) -> None:
        self.calls = 0

    def judge(self, facts: NormalizedFacts) -> FidesJudgeResult:
        self.calls += 1
        return FidesJudgeResult(
            verdict=FidesVerdict.DISABLED,
            confidence=0.0,
            reason_codes=("fides.disabled",),
            recommended_decision=Decision.ALLOW,
            provider_calls=0,
        )


class StaticFidesJudge:
    """Deterministic local FIDES test double.

    This is only a CI/test harness for the FIDES interface. The deterministic
    policy engine is WARDEN; FIDES itself remains the LLM-as-judge layer in the
    research architecture.
    """

    mode = FidesJudgeMode.TEST_DOUBLE

    def __init__(self, results: Mapping[str, FidesJudgeResult | Mapping[str, object]] | None = None):
        self.results = dict(results or {})
        self.calls = 0

    def judge(self, facts: NormalizedFacts) -> FidesJudgeResult:
        self.calls += 1
        result = self.results.get(facts.case_id)
        if isinstance(result, FidesJudgeResult):
            return result
        if isinstance(result, Mapping):
            raw_verdict = result.get("verdict", FidesVerdict.SAFE)
            verdict = FidesVerdict.coerce(raw_verdict)
            raw_confidence = result.get("confidence")
            confidence = float(str(raw_confidence)) if raw_confidence is not None else (1.0 if verdict == FidesVerdict.SAFE else 0.0)
            raw_recommended = result.get("recommended_decision")
            recommended_decision = None if raw_recommended is None else str(raw_recommended)
            raw_transcript = result.get("judge_transcript")
            judge_transcript = None if raw_transcript is None else str(raw_transcript)
            return FidesJudgeResult(
                verdict=verdict,
                confidence=confidence,
                reason_codes=tuple(str(code) for code in result.get("reason_codes", ())),
                recommended_decision=recommended_decision,
                latency_ms=result.get("latency_ms"),
                provider_calls=int(result.get("provider_calls", 0)),
                judge_transcript=judge_transcript,
            )
        return FidesJudgeResult(
            verdict=FidesVerdict.SAFE,
            confidence=1.0,
            reason_codes=("fides.test_double_default_safe",),
            recommended_decision=Decision.ALLOW,
            provider_calls=0,
        )


class ProviderPlaceholderFidesJudge:
    """Non-network placeholder for future provider wiring.

    This class marks the provider boundary explicitly but intentionally raises
    instead of making calls. The POC must not perform real provider calls.
    """

    mode = FidesJudgeMode.PROVIDER_PLACEHOLDER

    def judge(self, facts: NormalizedFacts) -> FidesJudgeResult:
        raise NotImplementedError(
            "FIDES provider_placeholder mode is contract-only in this POC; no real provider calls are implemented."
        )


def build_fides_judge(
    mode: FidesJudgeMode | str = FidesJudgeMode.DISABLED,
    *,
    results: Mapping[str, FidesJudgeResult | Mapping[str, object]] | None = None,
) -> FidesJudge:
    judge_mode = FidesJudgeMode.coerce(mode)
    if judge_mode == FidesJudgeMode.DISABLED:
        return DisabledFidesJudge()
    if judge_mode == FidesJudgeMode.TEST_DOUBLE:
        return StaticFidesJudge(results)
    if judge_mode == FidesJudgeMode.PROVIDER_PLACEHOLDER:
        return ProviderPlaceholderFidesJudge()
    raise ValueError(f"unsupported FIDES judge mode: {mode}")


def _recommended_decision_for_verdict(verdict: FidesVerdict) -> Decision:
    if verdict == FidesVerdict.UNSAFE:
        return Decision.BLOCK
    if verdict == FidesVerdict.UNCERTAIN:
        return Decision.QUARANTINE
    return Decision.ALLOW


def _is_untrusted(facts: NormalizedFacts) -> bool:
    return "untrusted" in facts.trust_labels or any(origin not in facts.policy.get("trusted_origins", ()) for origin in facts.origin_labels)


def _requested_capability_allowed(facts: NormalizedFacts) -> bool | None:
    allowed = facts.capability.get("capability_allowed")
    if allowed is not None:
        return bool(allowed)
    requested = facts.requested.get("capability") or facts.requested.get("tool")
    if requested is None:
        return None
    allowed_caps = tuple(facts.policy.get("allowed_capabilities", ())) or tuple(facts.policy.get("allowed_tools", ()))
    return str(requested) in allowed_caps


def _sink_allowed(facts: NormalizedFacts) -> bool | None:
    allowed = facts.flow.get("sink_allowed")
    if allowed is not None:
        return bool(allowed)
    sink = facts.requested.get("sink")
    if sink is None:
        return None
    return str(sink) in tuple(facts.policy.get("allowed_sinks", ()))


@lru_cache(maxsize=1)
def _default_rule_engine() -> RuleEngine:
    rules_root = Path(__file__).resolve().parents[2] / "rules"
    return RuleEngine(load_rules(rules_root))


def _facts_to_trace_and_policy(facts: NormalizedFacts) -> tuple[tuple[TraceEvent, ...], PolicyContext]:
    schema_shape = facts.features.get("schema_shape")
    if schema_shape in {"tool_plan_like", "tool_plan"}:
        schema_shape = "tool_plan_like_json"
    if schema_shape is None and bool(facts.features.get("tool_plan_shape")):
        schema_shape = "tool_plan_like_json"
    origin = facts.origin_labels[0] if facts.origin_labels else "unknown"
    text_parts: list[str] = []
    if facts.redacted_text:
        text_parts.append(facts.redacted_text)
    if bool(facts.features.get("instruction_shape")):
        text_parts.append("policy boundary directive structure")
    if bool(facts.features.get("obfuscated")):
        text_parts.append("hidden" + "\u200b" + "structure")
    if bool(facts.features.get("canary_present")):
        text_parts.append("[CANARY]")
    text = " ".join(text_parts)
    requested_capability = facts.requested.get("capability") or facts.requested.get("tool")
    requested_sink = facts.requested.get("sink")
    event = TraceEvent(
        event_id=facts.case_id,
        origin=origin,
        surface=facts.surface,
        text=text,
        schema_shape=str(schema_shape) if schema_shape is not None else None,
        capability=str(requested_capability) if requested_capability is not None else None,
        sink=str(requested_sink) if requested_sink is not None else None,
        canary_present=bool(facts.features.get("canary_present")),
        integrity="low" if "untrusted" in facts.trust_labels else "high",
        consequential_action=bool(facts.features.get("tool_plan_shape")) or bool(facts.requested.get("action")),
    )
    policy = PolicyContext(
        allowed_capabilities=tuple(str(item) for item in facts.policy.get("allowed_capabilities", ())),
        allowed_canary_sinks=tuple(str(item) for item in facts.policy.get("allowed_sinks", ())),
        trusted_origins=tuple(str(item) for item in facts.policy.get("trusted_origins", ())),
        permitted_sinks=tuple(str(item) for item in facts.policy.get("allowed_sinks", ())),
    )
    return (event,), policy


def evaluate_regex_baseline(facts: NormalizedFacts) -> GateDecision:
    reason_codes: list[str] = []
    if bool(facts.features.get("canary_present")):
        reason_codes.append("regex.canary_marker")
    if bool(facts.features.get("obfuscated")):
        reason_codes.append("regex.obfuscated_structure")
    redacted = (facts.redacted_text or "").lower()
    if "[canary]" in redacted:
        reason_codes.append("regex.redacted_canary")

    if reason_codes:
        return GateDecision(
            stack=StackName.REGEX_BASELINE,
            decision=Decision.BLOCK,
            blocked_by=BlockedBy.REGEX,
            rule_ids=tuple(reason_codes),
            reason_codes=tuple(reason_codes),
        )
    return GateDecision(stack=StackName.REGEX_BASELINE, decision=Decision.ALLOW)


def evaluate_warden(
    facts: NormalizedFacts,
    stack: StackName | str = StackName.YARA_RULES,
    rule_engine: RuleEngine | None = None,
) -> GateDecision:
    stack_name = StackName.coerce(stack)
    engine = rule_engine or _default_rule_engine()
    trace, policy = _facts_to_trace_and_policy(facts)
    rule_decision = engine.evaluate(trace, policy)
    if not rule_decision.hits:
        return GateDecision(stack=stack_name, decision=Decision.ALLOW)
    rule_ids = tuple(hit.rule_id for hit in rule_decision.hits)
    reason_codes = tuple(signal for hit in rule_decision.hits for signal in hit.matched_signals)
    return GateDecision(
        stack=stack_name,
        decision=rule_decision.final_action,
        blocked_by=BlockedBy.YARA_RULE,
        rule_ids=rule_ids,
        reason_codes=reason_codes,
    )


def evaluate_stack(
    facts: NormalizedFacts,
    stack: StackName | str,
    fides_judge: FidesJudge | None = None,
    rule_engine: RuleEngine | None = None,
) -> GateDecision:
    stack_name = StackName.coerce(stack)
    if stack_name == StackName.NO_GUARD:
        return GateDecision(stack=stack_name, decision=Decision.ALLOW)
    if stack_name == StackName.REGEX_BASELINE:
        return evaluate_regex_baseline(facts)
    if stack_name == StackName.YARA_RULES:
        return evaluate_warden(facts, StackName.YARA_RULES, rule_engine=rule_engine)
    if stack_name == StackName.RULES_PLUS_FIDES:
        warden = evaluate_warden(facts, StackName.RULES_PLUS_FIDES, rule_engine=rule_engine)
        if warden.decision != Decision.ALLOW:
            return GateDecision(
                stack=StackName.RULES_PLUS_FIDES,
                decision=warden.decision,
                blocked_by=warden.blocked_by,
                rule_ids=warden.rule_ids,
                fides_verdict=FidesVerdict.NOT_CALLED,
                reason_codes=warden.reason_codes,
                latency_ms=warden.latency_ms,
                provider_calls=0,
            )
        judge = fides_judge or DisabledFidesJudge()
        verdict = judge.judge(facts)
        if verdict.verdict == FidesVerdict.UNSAFE:
            return GateDecision(
                stack=StackName.RULES_PLUS_FIDES,
                decision=Decision.BLOCK,
                blocked_by=BlockedBy.FIDES_JUDGE,
                fides_verdict=FidesVerdict.UNSAFE,
                reason_codes=verdict.reason_codes,
                latency_ms=verdict.latency_ms,
                provider_calls=verdict.provider_calls,
            )
        if verdict.verdict == FidesVerdict.UNCERTAIN:
            return GateDecision(
                stack=StackName.RULES_PLUS_FIDES,
                decision=Decision.QUARANTINE,
                blocked_by=BlockedBy.FIDES_JUDGE,
                fides_verdict=FidesVerdict.UNCERTAIN,
                reason_codes=verdict.reason_codes,
                latency_ms=verdict.latency_ms,
                provider_calls=verdict.provider_calls,
            )
        return GateDecision(
            stack=StackName.RULES_PLUS_FIDES,
            decision=Decision.ALLOW,
            fides_verdict=verdict.verdict,
            reason_codes=verdict.reason_codes,
            latency_ms=verdict.latency_ms,
            provider_calls=verdict.provider_calls,
        )
    raise ValueError(f"unsupported stack: {stack}")


def evaluate_case(
    case: AttackCase,
    stacks: Sequence[StackName | str] = (
        StackName.NO_GUARD,
        StackName.REGEX_BASELINE,
        StackName.YARA_RULES,
        StackName.RULES_PLUS_FIDES,
    ),
    fides_judge: FidesJudge | None = None,
    rule_engine: RuleEngine | None = None,
) -> tuple[GateDecision, ...]:
    facts = NormalizedFacts.from_attack_case(case)
    return tuple(evaluate_stack(facts, stack, fides_judge=fides_judge, rule_engine=rule_engine) for stack in stacks)
