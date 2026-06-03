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
    eval_parser.add_argument("--iterations", type=int, default=50)
    eval_parser.add_argument("--output", type=Path, default=Path("artifacts/evals/gate_eval_report.json"))
    eval_parser.add_argument("--public-report", action="store_true", help="Write aggregate public-safe report")

    parser.add_argument("--fixture-set", default="smoke", choices=["smoke"], help=argparse.SUPPRESS)
    parser.add_argument("--output", type=Path, default=None, help=argparse.SUPPRESS)

    args = parser.parse_args(argv)
    if args.command == "eval":
        from .runner import EvaluationRunConfig, run_evaluation

        report = run_evaluation(EvaluationRunConfig(iterations=args.iterations))
        if args.public_report:
            from .reporting import build_public_report

            report = build_public_report(report)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    output = args.output or Path("artifacts/smoke_report.json")
    report = run_smoke(output)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
