from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from .adapters import AdapterConfig, DatasetAdapter, SyntheticAdapter
from .cases import AttackCase
from .decisions import Decision, GateDecision, StackName
from .gate import FidesJudge, evaluate_case


@dataclass(frozen=True)
class EvaluationRunConfig:
    adapters: tuple[DatasetAdapter, ...] = ()
    iterations: int = 50
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


def run_evaluation(config: EvaluationRunConfig | None = None, fides_judge: FidesJudge | None = None) -> dict[str, object]:
    config = config or EvaluationRunConfig()
    stacks = tuple(StackName.coerce(stack) for stack in config.stacks)
    adapter_results = [adapter.load() for adapter in config.adapters]
    cases: list[AttackCase] = []
    for result in adapter_results:
        cases.extend(result.cases)

    stack_counts = _empty_stack_counts(stacks)
    per_case_results: list[dict[str, object]] = []
    provider_calls = 0

    for case in cases:
        for iteration in range(config.iterations):
            iteration_case = _with_iteration(case, iteration)
            decisions = evaluate_case(iteration_case, stacks=stacks, fides_judge=fides_judge)
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
                    **summary,
                }
            )

    total_iterations = len(cases) * config.iterations
    return {
        "schema_version": "canaryweave_fides.gate_eval.v1",
        "iterations": config.iterations,
        "total_cases": len(cases),
        "total_iterations": total_iterations,
        "defense_stacks": stack_counts,
        "adapter_results": [result.to_dict() for result in adapter_results],
        "case_results": per_case_results,
        "provider_calls": provider_calls,
        "safety_boundary": "public-safe report: payload text and private custody fields are excluded",
    }
