from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from pathlib import Path
from typing import Mapping, Sequence, get_type_hints

import canaryweave
from canaryweave.generator import generate_suite
from canaryweave.metrics import (
    MetricsSummary,
    amplification,
    reduction,
    summarize,
    summarize_by_attack_type,
    summarize_by_scenario_family,
    summarize_by_source_family,
)
from canaryweave.scenario import AttackType, Mode, Scenario, SourceFamily
from canaryweave.simulator import ScenarioResult, run_suite
from canaryweave.source_adapters import load_source_summary, synthetic_source_summary

DEFAULT_LOOP_COUNT = 50
DEFAULT_SCENARIOS_PER_LOOP = 24
SCHEMA_VERSION = "canaryweave.autonomous_research_loops.safe.v1"
SAFETY_BOUNDARY = "deterministic_local_simulator_only_no_provider_calls_no_network_no_raw_payloads"
MODES = (Mode.BASELINE, Mode.MCP, Mode.ATTEST)

_SOURCE_CONDITIONS = (
    "mixed_structural_and_synthetic",
    SourceFamily.AGENTDOJO_STRUCTURAL.value,
    SourceFamily.INJECAGENT_STRUCTURAL.value,
    SourceFamily.SYNTHETIC_SAFE.value,
)

_ATTACK_CONDITIONS = (
    AttackType.SAMPLING_ABUSE,
    AttackType.SAMPLING_ABUSE,
    AttackType.SAMPLING_ABUSE,
    None,
)


def _metric_dict(summary: MetricsSummary) -> dict[str, int | float]:
    payload = summary.to_dict()
    return {
        key: round(value, 6) if isinstance(value, float) else value
        for key, value in payload.items()
    }


def _metric_dict_by_key(summaries: Mapping[str, MetricsSummary]) -> dict[str, dict[str, int | float]]:
    return {key: _metric_dict(value) for key, value in sorted(summaries.items())}


def _mean_metric_dict(summaries: Sequence[MetricsSummary]) -> dict[str, int | float]:
    if not summaries:
        return _metric_dict(summarize(()))
    type_hints = get_type_hints(MetricsSummary)
    mean_payload: dict[str, int | float] = {}
    for name in MetricsSummary.__dataclass_fields__:
        values = [getattr(summary, name) for summary in summaries]
        if type_hints[name] is int:
            mean_payload[name] = int(round(statistics.mean(values)))
        else:
            mean_payload[name] = round(float(statistics.mean(values)), 6)
    return mean_payload


def _source_summary_for_condition(condition: str, loop_index: int):
    if condition == SourceFamily.AGENTDOJO_STRUCTURAL.value:
        return load_source_summary(SourceFamily.AGENTDOJO_STRUCTURAL)
    if condition == SourceFamily.INJECAGENT_STRUCTURAL.value:
        return load_source_summary(SourceFamily.INJECAGENT_STRUCTURAL)
    if condition == SourceFamily.SYNTHETIC_SAFE.value:
        return synthetic_source_summary()
    # Mixed condition rotates safe structural summaries while retaining a local
    # fallback for absent source checkouts. The adapters expose structural counts
    # and digests only; raw source records are never embedded in results.
    cycle = (
        synthetic_source_summary(),
        load_source_summary(SourceFamily.AGENTDOJO_STRUCTURAL),
        load_source_summary(SourceFamily.INJECAGENT_STRUCTURAL),
    )
    return cycle[loop_index % len(cycle)]


def _attack_mix(scenarios: Sequence[Scenario]) -> dict[str, int]:
    counts = Counter(scenario.typed_metadata.attack_type.value for scenario in scenarios)
    return dict(sorted(counts.items()))


def _mode_results(scenarios: Sequence[Scenario]) -> dict[Mode, list[ScenarioResult]]:
    return {mode: run_suite(scenarios, mode) for mode in MODES}


def _scenario_family_observations(
    scenarios: Sequence[Scenario],
    mcp_results: Sequence[ScenarioResult],
    attest_results: Sequence[ScenarioResult],
    limit: int = 5,
) -> list[dict[str, object]]:
    mcp_by_family = summarize_by_scenario_family(mcp_results, scenarios)
    attest_by_family = summarize_by_scenario_family(attest_results, scenarios)
    observations: list[dict[str, object]] = []
    for family, mcp_summary in mcp_by_family.items():
        attest_summary = attest_by_family.get(family, summarize(()))
        observations.append(
            {
                "scenario_family": family,
                "mcp_attack_success_rate": round(mcp_summary.attack_success_rate, 6),
                "attest_attack_success_rate": round(attest_summary.attack_success_rate, 6),
                "attest_reduction": round(reduction(attest_summary, mcp_summary), 6),
                "total_scenarios": mcp_summary.total_scenarios,
            }
        )
    observations.sort(
        key=lambda item: (
            float(item["mcp_attack_success_rate"]),
            float(item["attest_reduction"]),
            int(item["total_scenarios"]),
            str(item["scenario_family"]),
        ),
        reverse=True,
    )
    return observations[:limit]


def _build_loop(loop_index: int, base_seed: int, scenarios_per_loop: int) -> dict[str, object]:
    seed = base_seed + (loop_index * 97)
    condition = _SOURCE_CONDITIONS[loop_index % len(_SOURCE_CONDITIONS)]
    attack_filter = _ATTACK_CONDITIONS[loop_index % len(_ATTACK_CONDITIONS)]
    source_summary = _source_summary_for_condition(condition, loop_index)
    scenarios = generate_suite(
        seed,
        scenarios_per_loop,
        source_summary=source_summary,
        attack_type=attack_filter,
    )
    results_by_mode = _mode_results(scenarios)
    summaries = {mode: summarize(results) for mode, results in results_by_mode.items()}
    grouped_by_attack = {
        mode.value: _metric_dict_by_key(summarize_by_attack_type(results, scenarios))
        for mode, results in results_by_mode.items()
    }
    grouped_by_source = {
        mode.value: _metric_dict_by_key(summarize_by_source_family(results, scenarios))
        for mode, results in results_by_mode.items()
    }
    baseline = summaries[Mode.BASELINE]
    mcp = summaries[Mode.MCP]
    attest = summaries[Mode.ATTEST]
    return {
        "loop_index": loop_index,
        "seed": seed,
        "scenario_count": len(scenarios),
        "attack_type_condition": attack_filter.value if attack_filter is not None else "weighted_registry_mix",
        "attack_mix": _attack_mix(scenarios),
        "source_family_condition": condition,
        "source_summary": {
            "requested_source_family_condition": condition,
            "source_family": source_summary.source_family.value,
            "adapter_name": source_summary.adapter_name,
            "digest": source_summary.digest,
            "record_count": source_summary.record_count,
            "category_counts": dict(sorted(source_summary.category_counts.items())),
        },
        "mode_comparisons": [mode.value for mode in MODES],
        "metrics_by_mode": {mode.value: _metric_dict(summary) for mode, summary in summaries.items()},
        "grouped_metrics": {
            "by_attack_type": grouped_by_attack,
            "by_source_family": grouped_by_source,
        },
        "comparisons": {
            "amplification": round(amplification(mcp, baseline), 6),
            "attest_reduction": round(reduction(attest, mcp), 6),
        },
        "top_scenario_family_observations": _scenario_family_observations(
            scenarios,
            results_by_mode[Mode.MCP],
            results_by_mode[Mode.ATTEST],
        ),
    }


def _aggregate(loops: Sequence[dict[str, object]]) -> dict[str, object]:
    summaries_by_mode: dict[str, list[MetricsSummary]] = {mode.value: [] for mode in MODES}
    amplification_values: list[float] = []
    reduction_values: list[float] = []
    family_counter: Counter[str] = Counter()
    family_observations: dict[str, dict[str, object]] = {}
    attack_mix_counter: Counter[str] = Counter()
    source_condition_counter: Counter[str] = Counter()

    by_attack_type_mode: dict[str, dict[str, list[MetricsSummary]]] = {}

    for loop in loops:
        metrics_by_mode = loop["metrics_by_mode"]
        grouped_by_attack = loop["grouped_metrics"]["by_attack_type"]  # type: ignore[index]
        for mode in MODES:
            metrics = metrics_by_mode[mode.value]  # type: ignore[index]
            summaries_by_mode[mode.value].append(MetricsSummary(**metrics))  # type: ignore[arg-type]
            for attack_type, attack_metrics in grouped_by_attack[mode.value].items():  # type: ignore[index]
                by_attack_type_mode.setdefault(str(attack_type), {}).setdefault(mode.value, []).append(
                    MetricsSummary(**attack_metrics)  # type: ignore[arg-type]
                )
        comparisons = loop["comparisons"]  # type: ignore[assignment]
        amplification_values.append(float(comparisons["amplification"]))  # type: ignore[index]
        reduction_values.append(float(comparisons["attest_reduction"]))  # type: ignore[index]
        source_condition_counter[str(loop["source_family_condition"])] += 1
        for attack_type, count in loop["attack_mix"].items():  # type: ignore[union-attr]
            attack_mix_counter[str(attack_type)] += int(count)
        for observation in loop["top_scenario_family_observations"]:  # type: ignore[union-attr]
            family = str(observation["scenario_family"])
            family_counter[family] += int(observation["total_scenarios"])
            current = family_observations.get(family)
            if current is None or float(observation["mcp_attack_success_rate"]) >= float(current["mcp_attack_success_rate"]):
                family_observations[family] = dict(observation)

    top_families = sorted(
        family_observations.values(),
        key=lambda item: (
            float(item["mcp_attack_success_rate"]),
            float(item["attest_reduction"]),
            family_counter[str(item["scenario_family"])],
            str(item["scenario_family"]),
        ),
        reverse=True,
    )[:8]
    return {
        "loop_count": len(loops),
        "modes": [mode.value for mode in MODES],
        "attack_mix": dict(sorted(attack_mix_counter.items())),
        "source_family_conditions": dict(sorted(source_condition_counter.items())),
        "by_mode": {
            mode: _mean_metric_dict(summaries)
            for mode, summaries in summaries_by_mode.items()
        },
        "by_attack_type": {
            attack_type: {
                mode: _mean_metric_dict(summaries)
                for mode, summaries in sorted(mode_summaries.items())
            }
            for attack_type, mode_summaries in sorted(by_attack_type_mode.items())
        },
        "comparisons": {
            "amplification": round(float(statistics.mean(amplification_values)), 6) if amplification_values else 0.0,
            "attest_reduction": round(float(statistics.mean(reduction_values)), 6) if reduction_values else 0.0,
        },
        "top_scenario_family_observations": top_families,
    }


def _finding(aggregate: Mapping[str, object]) -> dict[str, object]:
    by_attack_type = aggregate["by_attack_type"]  # type: ignore[index]
    sampling = by_attack_type[AttackType.SAMPLING_ABUSE.value]  # type: ignore[index]
    baseline = sampling[Mode.BASELINE.value]  # type: ignore[index]
    mcp = sampling[Mode.MCP.value]  # type: ignore[index]
    attest = sampling[Mode.ATTEST.value]  # type: ignore[index]
    baseline_asr = float(baseline["attack_success_rate"])
    mcp_asr = float(mcp["attack_success_rate"])
    attest_asr = float(attest["attack_success_rate"])
    amplification_value = mcp_asr - baseline_asr
    reduction_value = 0.0 if mcp_asr == 0 else (mcp_asr - attest_asr) / mcp_asr
    return {
        "topic": AttackType.SAMPLING_ABUSE.value,
        "metric_name": "simulated_unauthorized_action_execution_rate",
        "summary": (
            "Across deterministic local simulator loops, sampling abuse scenarios show a "
            f"higher simulated unauthorized-action execution rate in the intentionally permissive "
            f"MCP-shaped mode than in baseline by {amplification_value:.3f}; the local "
            f"policy-plus-attestation mode reduces that simulator rate by {reduction_value:.3f}."
        ),
        "evidence": {
            "baseline_attack_success_rate": round(baseline_asr, 6),
            "mcp_attack_success_rate": round(mcp_asr, 6),
            "attest_attack_success_rate": round(attest_asr, 6),
            "amplification": round(amplification_value, 6),
            "attest_reduction": round(reduction_value, 6),
        },
        "scope": "deterministic simulator invariant using synthetic canaries and inert symbolic actions",
        "raw_payloads_included": False,
    }


def build_loop_results(
    loops: int = DEFAULT_LOOP_COUNT,
    seed: int = 1337,
    scenarios_per_loop: int = DEFAULT_SCENARIOS_PER_LOOP,
) -> dict[str, object]:
    if loops < 0:
        raise ValueError("loops must be non-negative")
    if scenarios_per_loop < 0:
        raise ValueError("scenarios_per_loop must be non-negative")
    loop_payloads = [
        _build_loop(loop_index, seed, scenarios_per_loop)
        for loop_index in range(loops)
    ]
    aggregate = _aggregate(loop_payloads)
    return {
        "schema_version": SCHEMA_VERSION,
        "package": canaryweave.__name__,
        "safety_boundary": SAFETY_BOUNDARY,
        "loop_count": loops,
        "scenarios_per_loop": scenarios_per_loop,
        "loops": loop_payloads,
        "aggregate": aggregate,
        "finding": _finding(aggregate),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run deterministic local CanaryWeave research loops")
    parser.add_argument("--loops", type=int, default=DEFAULT_LOOP_COUNT)
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--scenarios-per-loop", type=int, default=DEFAULT_SCENARIOS_PER_LOOP)
    parser.add_argument("--output", type=Path, default=Path("artifacts/research/loop_results.json"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    payload = build_loop_results(args.loops, args.seed, args.scenarios_per_loop)
    encoded = json.dumps(payload, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
