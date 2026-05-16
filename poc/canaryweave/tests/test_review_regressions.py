import importlib.util
import json
import sys
from pathlib import Path


def _load_script(name: str):
    path = Path(__file__).resolve().parents[1] / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


autonomous_research_loops = _load_script("autonomous_research_loops")
model_asr_dry_run = _load_script("model_asr_dry_run")

build_loop_results = autonomous_research_loops.build_loop_results
MODEL_SETS = model_asr_dry_run.MODEL_SETS


def test_loop_finding_uses_sampling_only_evidence():
    payload = build_loop_results(loops=6, seed=1337)
    finding = payload["finding"]
    sampling_metrics = payload["aggregate"]["by_attack_type"]["sampling_abuse"]

    assert finding["topic"] == "sampling_abuse"
    assert finding["evidence"]["mcp_attack_success_rate"] == sampling_metrics["mcp"]["attack_success_rate"]
    assert finding["evidence"]["baseline_attack_success_rate"] == sampling_metrics["baseline"]["attack_success_rate"]
    assert finding["evidence"]["attest_attack_success_rate"] == sampling_metrics["attest"]["attack_success_rate"]


def test_committed_loop_artifact_schema_and_no_raw_canaries():
    artifact = Path("artifacts/research/loop_results.json")
    payload = json.loads(artifact.read_text(encoding="utf-8"))
    serialized = artifact.read_text(encoding="utf-8")

    assert payload["schema_version"] == "canaryweave.autonomous_research_loops.safe.v1"
    assert payload["loop_count"] == len(payload["loops"]) == 50
    assert payload["scenarios_per_loop"] == 24
    assert set(payload["aggregate"]["by_mode"]) == {"baseline", "mcp", "attest"}
    assert "CANARY_" not in serialized


def test_model_sets_match_registry_ids():
    registry = Path("configs/model_registry.safe.yaml").read_text(encoding="utf-8")
    for model_ids in MODEL_SETS.values():
        for model_id in model_ids:
            assert f"model_id: {model_id}" in registry
