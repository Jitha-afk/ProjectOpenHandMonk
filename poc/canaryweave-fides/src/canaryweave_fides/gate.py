from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol, Sequence

from .cases import AttackCase
from .decisions import BlockedBy, Decision, FidesVerdict, GateDecision, StackName
from .facts import NormalizedFacts


@dataclass(frozen=True)
class FidesJudgeResult:
    verdict: FidesVerdict | str
    reason_codes: tuple[str, ...] = ()
    latency_ms: float | None = None
    provider_calls: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "verdict", FidesVerdict.coerce(self.verdict))
        object.__setattr__(self, "reason_codes", tuple(str(code) for code in self.reason_codes))
        if self.latency_ms is not None:
            object.__setattr__(self, "latency_ms", float(self.latency_ms))
        object.__setattr__(self, "provider_calls", int(self.provider_calls))


class FidesJudge(Protocol):
    def judge(self, facts: NormalizedFacts) -> FidesJudgeResult:
        ...


class StaticFidesJudge:
    """Deterministic local FIDES test double.

    This is only a CI/test harness for the FIDES interface. The deterministic
    policy engine is WARDEN; FIDES itself remains the LLM-as-judge layer in the
    research architecture.
    """

    def __init__(self, results: Mapping[str, FidesJudgeResult | Mapping[str, object]] | None = None):
        self.results = dict(results or {})
        self.calls = 0

    def judge(self, facts: NormalizedFacts) -> FidesJudgeResult:
        self.calls += 1
        result = self.results.get(facts.case_id)
        if isinstance(result, FidesJudgeResult):
            return result
        if isinstance(result, Mapping):
            return FidesJudgeResult(
                verdict=result.get("verdict", FidesVerdict.SAFE),
                reason_codes=tuple(str(code) for code in result.get("reason_codes", ())),
                latency_ms=result.get("latency_ms"),
                provider_calls=int(result.get("provider_calls", 0)),
            )
        return FidesJudgeResult(verdict=FidesVerdict.SAFE, reason_codes=("fides_default_safe",), provider_calls=0)


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


def evaluate_warden(facts: NormalizedFacts, stack: StackName | str = StackName.YARA_RULES) -> GateDecision:
    stack_name = StackName.coerce(stack)
    rule_ids: list[str] = []
    reason_codes: list[str] = []

    if bool(facts.features.get("tool_plan_shape")) and _is_untrusted(facts):
        rule_ids.append("warden.untrusted_tool_plan")
        reason_codes.append("untrusted_tool_plan")

    capability_allowed = _requested_capability_allowed(facts)
    if capability_allowed is False:
        rule_ids.append("warden.capability_not_allowed")
        reason_codes.append("capability_not_allowed")

    sink_allowed = _sink_allowed(facts)
    if bool(facts.features.get("canary_present")) and sink_allowed is False:
        rule_ids.append("warden.canary_sink_violation")
        reason_codes.append("canary_sink_violation")

    if bool(facts.features.get("instruction_shape")) and bool(facts.features.get("obfuscated")) and _is_untrusted(facts):
        rule_ids.append("warden.hidden_instruction_shape")
        reason_codes.append("hidden_instruction_shape")

    if not rule_ids:
        return GateDecision(stack=stack_name, decision=Decision.ALLOW)

    decision = Decision.BLOCK
    if rule_ids == ["warden.hidden_instruction_shape"]:
        decision = Decision.QUARANTINE
    return GateDecision(
        stack=stack_name,
        decision=decision,
        blocked_by=BlockedBy.YARA_RULE,
        rule_ids=tuple(rule_ids),
        reason_codes=tuple(reason_codes),
    )


def evaluate_stack(
    facts: NormalizedFacts,
    stack: StackName | str,
    fides_judge: FidesJudge | None = None,
) -> GateDecision:
    stack_name = StackName.coerce(stack)
    if stack_name == StackName.NO_GUARD:
        return GateDecision(stack=stack_name, decision=Decision.ALLOW)
    if stack_name == StackName.REGEX_BASELINE:
        return evaluate_regex_baseline(facts)
    if stack_name == StackName.YARA_RULES:
        return evaluate_warden(facts, StackName.YARA_RULES)
    if stack_name == StackName.RULES_PLUS_FIDES:
        warden = evaluate_warden(facts, StackName.RULES_PLUS_FIDES)
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
        judge = fides_judge or StaticFidesJudge()
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
) -> tuple[GateDecision, ...]:
    facts = NormalizedFacts.from_attack_case(case)
    return tuple(evaluate_stack(facts, stack, fides_judge=fides_judge) for stack in stacks)
