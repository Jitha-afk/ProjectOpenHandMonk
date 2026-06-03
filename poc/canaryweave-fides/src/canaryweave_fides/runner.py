from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from .adapters import AdapterConfig, DatasetAdapter, SyntheticAdapter
from .cases import AttackCase, GroundTruth, _public_safe
from .decisions import Decision, GateDecision, StackName
from .gate import FidesJudge, FidesJudgeMode, StaticFidesJudge, build_fides_judge, build_test_double_evidence_results, evaluate_case
from .rule_engine import RuleEngine


@dataclass(frozen=True)
class EvaluationRunConfig:
    adapters: tuple[DatasetAdapter, ...] = ()
    iterations: int = 50
    fides_mode: FidesJudgeMode | str = FidesJudgeMode.DISABLED
    fides_test_double_evidence_rules: tuple[Mapping[str, Any], ...] = ()
    stacks: tuple[StackName | str, ...] = (
        StackName.NO_GUARD,
        StackName.REGEX_BASELINE,
        StackName.YARA_RULES,
        StackName.RULES_PLUS_FIDES,
    )

    def __post_init__(self) -> None:
        adapters = tuple(self.adapters) if self.adapters else (SyntheticAdapter(AdapterConfig()),)
        object.__setattr__(self, "adapters", adapters)
        object.__setattr__(self, "iterations", int(self.iterations))
        object.__setattr__(self, "fides_mode", FidesJudgeMode.coerce(self.fides_mode))
        object.__setattr__(self, "fides_test_double_evidence_rules", tuple(dict(rule) for rule in self.fides_test_double_evidence_rules))
        object.__setattr__(self, "stacks", tuple(StackName.coerce(stack) for stack in self.stacks))
        if self.iterations < 1:
            raise ValueError("iterations must be >= 1")


def _with_iteration(case: AttackCase, iteration: int) -> AttackCase:
    return AttackCase(
        case_id=case.case_id,
        dataset_id=case.dataset_id,
        split=case.split,
        case_kind=case.case_kind,
        attack_category=case.attack_category,
        surface=case.surface,
        safe_features=case.safe_features,
        policy_context=case.policy_context,
        expected_behavior=case.expected_behavior,
        ground_truth=case.ground_truth,
        iteration_seed=iteration,
        raw_ref=case.raw_ref,
        private_data=case.private_data,
    )


def _empty_stack_counts(stacks: Sequence[StackName]) -> dict[str, dict[str, int]]:
    return {stack.value: {"allow": 0, "quarantine": 0, "block": 0} for stack in stacks}


def _summarize_decisions(decisions: Iterable[GateDecision]) -> dict[str, object]:
    decision_list = tuple(decisions)
    return {
        "decisions": [decision.to_dict() for decision in decision_list],
        "provider_calls": sum(decision.provider_calls for decision in decision_list),
    }


def run_evaluation(
    config: EvaluationRunConfig | None = None,
    fides_judge: FidesJudge | None = None,
    rule_engine: RuleEngine | None = None,
) -> dict[str, object]:
    config = config or EvaluationRunConfig()
    stacks = tuple(StackName.coerce(stack) for stack in config.stacks)
    adapter_results = [adapter.load() for adapter in config.adapters]
    cases: list[AttackCase] = []
    for result in adapter_results:
        cases.extend(result.cases)

    test_double_results = {}
    if config.fides_mode == FidesJudgeMode.TEST_DOUBLE and config.fides_test_double_evidence_rules:
        test_double_results = build_test_double_evidence_results(cases, config.fides_test_double_evidence_rules)
    if fides_judge is not None:
        judge = fides_judge
    elif test_double_results:
        judge = StaticFidesJudge(test_double_results)
    else:
        judge = build_fides_judge(config.fides_mode)

    stack_counts = _empty_stack_counts(stacks)
    per_case_results: list[dict[str, object]] = []
    provider_calls = 0

    for case in cases:
        for iteration in range(config.iterations):
            iteration_case = _with_iteration(case, iteration)
            decisions = evaluate_case(iteration_case, stacks=stacks, fides_judge=judge, rule_engine=rule_engine)
            summary = _summarize_decisions(decisions)
            provider_calls += int(summary["provider_calls"])
            for decision in decisions:
                stack_counts[decision.stack.value][decision.decision.value] += 1
            per_case_results.append(
                {
                    "case_id": iteration_case.case_id,
                    "dataset_id": iteration_case.dataset_id,
                    "split": iteration_case.split,
                    "case_kind": iteration_case.case_kind.value,
                    "attack_category": iteration_case.attack_category,
                    "surface": iteration_case.surface,
                    "iteration": iteration,
                    "safe_features": _public_safe(iteration_case.safe_features),
                    "policy_context": _public_safe(iteration_case.policy_context),
                    "ground_truth": (
                        iteration_case.ground_truth.to_dict()
                        if isinstance(iteration_case.ground_truth, GroundTruth)
                        else _public_safe(iteration_case.ground_truth or {})
                    ),
                    **summary,
                }
            )

    total_iterations = len(cases) * config.iterations
    return {
        "schema_version": "canaryweave_fides.gate_eval.v1",
        "iterations": config.iterations,
        "total_cases": len(cases),
        "total_iterations": total_iterations,
        "fides_mode": FidesJudgeMode.coerce(config.fides_mode).value,
        "fides_test_double": {
            "enabled": config.fides_mode == FidesJudgeMode.TEST_DOUBLE,
            "evidence_rules_configured": len(config.fides_test_double_evidence_rules),
            "fixture_verdicts_configured": len(test_double_results),
            "provider_calls_enabled": False,
            "judge_transcripts_included": False,
            "label": "FIDES TEST DOUBLE EVIDENCE MODE" if config.fides_mode == FidesJudgeMode.TEST_DOUBLE else "FIDES DISABLED",
        },
        "defense_stacks": stack_counts,
        "adapter_results": [result.to_dict() for result in adapter_results],
        "case_results": per_case_results,
        "provider_calls": provider_calls,
        "safety_boundary": "public-safe report: payload text and private custody fields are excluded",
    }
