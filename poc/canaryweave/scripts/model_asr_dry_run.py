from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path

from canaryweave.generator import generate_suite
from canaryweave.scenario import AttackType, Mode, Scenario
from canaryweave.source_adapters import synthetic_source_summary

MODEL_SETS = {
    "smoke_core": (
        "openai_gpt4o_smoke",
        "anthropic_claude_sonnet_4_6_smoke",
    ),
    "smoke_frontier": (
        "openai_gpt4o_smoke",
        "openai_gpt4o_mini_smoke",
        "anthropic_claude_sonnet_4_6_smoke",
        "anthropic_claude_sonnet_4_smoke",
        "local_or_openrouter_frontier_placeholder",
    ),
}


@dataclass(frozen=True)
class DryRunTrial:
    schema_version: str
    model_id: str
    mode: str
    scenario_id: str
    attack_type: str
    scenario_family: str
    source_family: str
    canary_redacted: str
    prompt_template_id: str
    expected_policy: str


def _redact_canary(canary: str) -> str:
    import hashlib

    return f"CANARY_REDACTED:{hashlib.sha256(canary.encode('utf-8')).hexdigest()[:16]}"


def _trial_for(model_id: str, mode: Mode, scenario: Scenario) -> DryRunTrial:
    metadata = scenario.typed_metadata
    return DryRunTrial(
        schema_version="canaryweave.model_trial.safe.v1",
        model_id=model_id,
        mode=mode.value,
        scenario_id=scenario.id,
        attack_type=metadata.attack_type.value,
        scenario_family=metadata.scenario_family,
        source_family=metadata.source_family.value,
        canary_redacted=_redact_canary(scenario.canaries[0]),
        prompt_template_id="benign_sampling_boundary_v1",
        expected_policy="do_not_route_server_sampling_canary_to_denied_mock_sink",
    )


def build_dry_run_trials(seed: int, count: int, model_ids: list[str], modes: list[Mode]) -> list[DryRunTrial]:
    scenarios = generate_suite(
        seed,
        count,
        source_summary=synthetic_source_summary(),
        attack_type=AttackType.SAMPLING_ABUSE,
    )
    return [
        _trial_for(model_id, mode, scenario)
        for model_id in model_ids
        for mode in modes
        for scenario in scenarios
    ]


def summarize_trials(trials: list[DryRunTrial]) -> dict[str, object]:
    by_attack = Counter(trial.attack_type for trial in trials)
    by_model = Counter(trial.model_id for trial in trials)
    by_mode = Counter(trial.mode for trial in trials)
    return {
        "schema_version": "canaryweave.model_dry_run_summary.safe.v1",
        "total_trials": len(trials),
        "by_attack_type": dict(sorted(by_attack.items())),
        "by_model": dict(sorted(by_model.items())),
        "by_mode": dict(sorted(by_mode.items())),
        "safety_boundary": "dry_run_only_no_provider_calls_no_raw_payloads",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build safe dry-run model ASR trial plans")
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument(
        "--model-set",
        choices=sorted(MODEL_SETS),
        default="smoke_frontier",
        help="Named safe model placeholder set to include when --model-id is not provided.",
    )
    parser.add_argument(
        "--model-id",
        action="append",
        default=[],
        help="Model registry id to include. Can be repeated.",
    )
    parser.add_argument(
        "--mode",
        choices=[mode.value for mode in Mode],
        action="append",
        default=[],
        help="Harness mode to include. Can be repeated.",
    )
    parser.add_argument("--output", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    model_ids = args.model_id or list(MODEL_SETS[args.model_set])
    modes = [Mode(value) for value in (args.mode or [Mode.MCP.value, Mode.ATTEST.value])]
    trials = build_dry_run_trials(args.seed, args.count, model_ids, modes)
    payload = {
        "summary": summarize_trials(trials),
        "trials": [asdict(trial) for trial in trials],
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
