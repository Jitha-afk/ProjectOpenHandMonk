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
    parser = argparse.ArgumentParser(description="CanaryWeave FIDES controlled smoke runner")
    parser.add_argument("--fixture-set", default="smoke", choices=["smoke"])
    parser.add_argument("--output", type=Path, default=Path("artifacts/smoke_report.json"))
    args = parser.parse_args(argv)
    report = run_smoke(args.output)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
