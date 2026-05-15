from __future__ import annotations

import argparse
import json
from pathlib import Path

from .events import JsonRpcEventLogger
from .generator import generate_suite
from .metrics import summarize
from .scenario import Mode
from .simulator import run_suite


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run controlled PROTOAMP POC suite")
    parser.add_argument("--seed", type=int, default=1337)
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--mode", choices=[mode.value for mode in Mode], default=Mode.ATTEST.value)
    parser.add_argument("--log", type=Path, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    scenarios = generate_suite(args.seed, args.count)
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
        "metrics": summary.to_dict(),
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
