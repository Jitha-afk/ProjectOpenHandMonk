import json
from pathlib import Path

from canaryweave.events import JsonRpcEventLogger
from canaryweave.generator import generate_scenario
from canaryweave.scenario import ActionKind, AttackType, Mode
from canaryweave.simulator import run_suite


def test_event_log_includes_action_kind_for_trace_disambiguation(tmp_path):
    scenario = generate_scenario(1337, 0, attack_type=AttackType.SAMPLING_ABUSE)
    log_path = tmp_path / "events.jsonl"

    with JsonRpcEventLogger(log_path) as logger:
        run_suite([scenario], Mode.MCP, logger=logger)

    rows = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
    kinds = [row["params"]["action_kind"] for row in rows]

    assert set(kinds) <= {kind.value for kind in ActionKind}
    assert ActionKind.UNAUTHORIZED.value in kinds
