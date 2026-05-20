from __future__ import annotations

import argparse
from pathlib import Path

from .common import DEFAULT_SCENARIO_IDS, VictimPolicy, safe_artifact_path
from .victim_client import run_mcp_sampling_poc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the local MCP stdio sampling POC")
    parser.add_argument("--mode", choices=[policy.value for policy in VictimPolicy], required=True)
    parser.add_argument("--scenario-id", action="append", default=None, help="Scenario id to run; repeat for multiple")
    parser.add_argument("--sink", type=Path, default=None, help="Local inert JSONL sink path")
    parser.add_argument("--output", type=Path, default=None, help="Write JSON result artifact")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    scenario_ids = tuple(args.scenario_id or DEFAULT_SCENARIO_IDS)
    output_path = safe_artifact_path(args.output) if args.output is not None else None
    result = run_mcp_sampling_poc(args.mode, scenario_ids=scenario_ids, sink_path=args.sink)
    text = result.to_json()
    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
