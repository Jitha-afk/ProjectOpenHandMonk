import importlib.util
import json
from pathlib import Path

import sys

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "model_asr_dry_run.py"
SPEC = importlib.util.spec_from_file_location("model_asr_dry_run", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
model_asr_dry_run = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = model_asr_dry_run
SPEC.loader.exec_module(model_asr_dry_run)

build_parser = model_asr_dry_run.build_parser
main = model_asr_dry_run.main


def test_model_set_smoke_core_is_available():
    parser = build_parser()
    args = parser.parse_args(["--model-set", "smoke_core"])

    assert args.model_set == "smoke_core"


def test_model_dry_run_model_set_writes_redacted_plan(tmp_path):
    output = tmp_path / "plan.json"

    result = main(["--model-set", "smoke_core", "--count", "2", "--output", str(output)])

    assert result == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["summary"]["total_trials"] == 8
    models = payload["summary"]["by_model"]
    assert set(models) == {"openai_gpt4o_smoke", "anthropic_claude_sonnet_4_6_smoke"}
    serialized = output.read_text(encoding="utf-8")
    assert "CANARY_REDACTED:" in serialized
    assert "CANARY_1337" not in serialized
