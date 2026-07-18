from __future__ import annotations

import argparse
import json
from pathlib import Path

from .events import JsonRpcEventLogger
from .generator import generate_suite
from .metrics import summarize, summarize_by_attack_type, summarize_by_scenario_family, summarize_by_source_family
from .scenario import AttackType, Mode, SourceFamily
from .simulator import run_suite
from .source_adapters import load_source_summary, summarize_agentdojo, summarize_injecagent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run controlled CanaryWeave POC suite")
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--mode", choices=[mode.value for mode in Mode], default=Mode.ATTEST.value)
    parser.add_argument("--log", type=Path, default=None)
    parser.add_argument("--attack-type", choices=[attack.value for attack in AttackType], default=None)
    parser.add_argument("--source-family", choices=[family.value for family in SourceFamily], default=SourceFamily.SYNTHETIC_SAFE.value)
    parser.add_argument("--agentdojo-root", type=Path, default=Path("/tmp/canaryweave-source-repos/agentdojo"))
    parser.add_argument("--injecagent-root", type=Path, default=Path("/tmp/canaryweave-source-repos/InjecAgent"))
    parser.add_argument("--print-source-summary", action="store_true")
    return parser


def _load_summary_for_args(args: argparse.Namespace):
    source_family = SourceFamily(args.source_family)
    if source_family is SourceFamily.AGENTDOJO_STRUCTURAL:
        return summarize_agentdojo(args.agentdojo_root)
    if source_family is SourceFamily.INJECAGENT_STRUCTURAL:
        return summarize_injecagent(args.injecagent_root)
    return load_source_summary(source_family)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    source_summary = _load_summary_for_args(args)
    if args.print_source_summary:
        print(json.dumps(source_summary.to_safe_dict(), indent=2, sort_keys=True))
        return 0
    attack_type = AttackType(args.attack_type) if args.attack_type is not None else None
    scenarios = generate_suite(
        args.seed,
        args.count,
        source_summary=source_summary,
        attack_type=attack_type,
    )
    logger = JsonRpcEventLogger(args.log) if args.log is not None else JsonRpcEventLogger()
    try:
        results = run_suite(scenarios, Mode(args.mode), logger=logger)
    finally:
        logger.close()
    summary = summarize(results)
    output = {
        "mode": args.mode,
        "seed": args.seed,
        "count": args.count,
        "source_family": args.source_family,
        "attack_type_filter": args.attack_type,
        "metrics": summary.to_dict(),
        "by_attack_type": {key: value.to_dict() for key, value in summarize_by_attack_type(results, scenarios).items()},
        "by_source_family": {key: value.to_dict() for key, value in summarize_by_source_family(results, scenarios).items()},
        "by_scenario_family": {key: value.to_dict() for key, value in summarize_by_scenario_family(results, scenarios).items()},
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
