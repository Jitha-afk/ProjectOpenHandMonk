from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from canaryweave.demo_sampling import build_sampling_demo_suite, evaluate_sampling_demo_suite


def _tool_action_dict(action) -> dict[str, object]:
    return {
        "name": action.name,
        "capability": action.capability,
        "args": dict(action.args),
        "kind": action.kind.value,
    }


def build_payload() -> dict[str, object]:
    suite = build_sampling_demo_suite()
    result = evaluate_sampling_demo_suite(suite)
    return {
        "schema_version": "canaryweave.sampling_demo.safe.v1",
        "claim": "Controlled deterministic MCP sampling role/provenance demo: an intentionally vulnerable host accepts server-originated sampling content as user authority; this is not ecosystem prevalence and not live-model evidence.",
        "scope": {
            "demo_type": "deterministic policy demonstration",
            "vulnerable_policy": "intentionally vulnerable host accepts server sampling as authority",
            "hardened_policy": "origin-aware host blocks server sampling as authority",
            "evidence_boundary": "not ecosystem prevalence; not live-model behavior; not a full MCP wire trace",
        },
        "attack_success_condition": "unauthorized_inert_action_executed_from_server_sampling",
        "safety_boundary": "benign_canary_only_no_external_side_effects",
        "total_scenarios": result.total_scenarios,
        "metrics": {
            "baseline_attack_success_rate": result.baseline.attack_success_rate,
            "vulnerable_host_attack_success_rate": result.vulnerable_host.attack_success_rate,
            "hardened_host_attack_success_rate": result.hardened_host.attack_success_rate,
            "vulnerable_successes": result.vulnerable_host.successes,
            "hardened_successes": result.hardened_host.successes,
        },
        "scenarios": [
            {
                "scenario_id": scenario.scenario_id,
                "title": scenario.title,
                "user_goal": scenario.user_goal,
                "sampling_request": asdict(scenario.sampling_request),
                "allowed_action": _tool_action_dict(scenario.allowed_action),
                "unauthorized_action": _tool_action_dict(scenario.unauthorized_action),
                "expected_policy": scenario.expected_policy,
            }
            for scenario in suite.scenarios
        ],
        "transcripts": [asdict(transcript) for transcript in result.transcripts],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Emit safe MCP sampling attack demo artifact")
    parser.add_argument("--output", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    encoded = json.dumps(build_payload(), indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
