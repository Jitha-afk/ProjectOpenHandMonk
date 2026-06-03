from __future__ import annotations

import argparse
import json
from pathlib import Path

from .fides import FidesIFCLayer
from .fixtures import smoke_cases
from .metrics import summarize_smoke
from .rule_engine import RuleEngine
from .rule_loader import load_rules


def run_smoke(output: Path | str | None = None) -> dict:
    root = Path(__file__).resolve().parents[2]
    engine = RuleEngine(load_rules(root / "rules"))
    report = summarize_smoke(smoke_cases(), engine, FidesIFCLayer(enabled=True))
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="CanaryWeave FIDES controlled smoke/eval runner")
    subparsers = parser.add_subparsers(dest="command")

    smoke = subparsers.add_parser("smoke", help="Run legacy smoke report")
    smoke.add_argument("--fixture-set", default="smoke", choices=["smoke"])
    smoke.add_argument("--output", type=Path, default=Path("artifacts/smoke_report.json"))

    eval_parser = subparsers.add_parser("eval", help="Run WARDEN/FIDES pre-context gate evaluation")
    eval_parser.add_argument("--config", type=Path, default=None, help="Eval YAML config (default: data/evals/smoke.yaml)")
    eval_parser.add_argument("--datasets-config", type=Path, default=None, help="Dataset catalog YAML (default: conf/datasets.yaml)")
    eval_parser.add_argument("--stacks-config", type=Path, default=None, help="Stack catalog YAML (default: conf/stacks.yaml)")
    eval_parser.add_argument("--dataset", action="append", default=None, help="Limit run to one or more configured dataset IDs")
    eval_parser.add_argument("--iterations", type=int, default=50)
    eval_parser.add_argument("--output", type=Path, default=Path("artifacts/evals/gate_eval_report.json"))
    eval_parser.add_argument("--public-report", action="store_true", help="Write aggregate public-safe report")
    eval_parser.add_argument(
        "--fail-on-missing-optional-dataset",
        action="store_true",
        help="Treat skipped optional datasets as an eval error instead of reporting an explicit skip",
    )

    parser.add_argument("--fixture-set", default="smoke", choices=["smoke"], help=argparse.SUPPRESS)
    parser.add_argument("--output", type=Path, default=None, help=argparse.SUPPRESS)

    args = parser.parse_args(argv)
    if args.command == "eval":
        from .runner import EvaluationRunConfig, run_evaluation

        adapters = ()
        stacks = None
        iterations = args.iterations
        default_output = None
        use_public_report = args.public_report
        if args.config is not None:
            from .config import load_eval_config

            loaded = load_eval_config(args.config, datasets_config=args.datasets_config, stacks_config=args.stacks_config)
            adapters = loaded.adapters
            if args.dataset:
                selected = {str(dataset_id) for dataset_id in args.dataset}
                adapters = tuple(adapter for adapter in adapters if adapter.dataset_id in selected)
            stacks = loaded.stacks
            iterations = args.iterations if "--iterations" in (argv or []) else loaded.iterations
            default_output = loaded.default_output
            if not args.public_report and loaded.public_report is not None:
                use_public_report = loaded.public_report

        if stacks is None:
            run_config = EvaluationRunConfig(adapters=adapters, iterations=iterations)
        else:
            run_config = EvaluationRunConfig(adapters=adapters, iterations=iterations, stacks=stacks)
        report = run_evaluation(run_config)
        missing = [
            result
            for result in report.get("adapter_results", [])
            if result.get("status") == "skipped_missing_local_path"
        ]
        if args.fail_on_missing_optional_dataset and missing:
            print(json.dumps({"error": "missing_optional_dataset", "adapter_results": missing}, indent=2, sort_keys=True))
            return 2
        if use_public_report:
            from .reporting import build_public_report

            report = build_public_report(report)
        output_path = args.output
        if args.output == Path("artifacts/evals/gate_eval_report.json") and default_output is not None:
            output_path = default_output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    output = args.output or Path("artifacts/smoke_report.json")
    report = run_smoke(output)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
