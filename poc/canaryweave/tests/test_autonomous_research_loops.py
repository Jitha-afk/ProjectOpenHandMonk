import importlib.util
import json
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "autonomous_research_loops.py"
SPEC = importlib.util.spec_from_file_location("autonomous_research_loops", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
autonomous_research_loops = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(autonomous_research_loops)

DEFAULT_LOOP_COUNT = autonomous_research_loops.DEFAULT_LOOP_COUNT
build_loop_results = autonomous_research_loops.build_loop_results


REQUIRED_METRIC_FIELDS = {
    "total_scenarios",
    "total_actions",
    "executed_actions",
    "unauthorized_attempts",
    "unauthorized_executed",
    "attack_success_rate",
    "block_rate",
    "canary_touch_rate",
}

FORBIDDEN_RAW_PAYLOAD_MARKERS = tuple(
    [
        "ignore" + " previous",
        "system" + " prompt",
        "developer" + " message",
        "ex" + "fil",
        "creden" + "tial",
        "pass" + "word",
        "http" + "://",
        "https" + "://",
    ]
)


def test_loop_runner_default_count_is_50():
    payload = build_loop_results()

    assert DEFAULT_LOOP_COUNT == 50
    assert payload["loop_count"] == 50
    assert len(payload["loops"]) == 50


def test_loop_runner_is_deterministic():
    first = build_loop_results(loops=6, seed=2026)
    second = build_loop_results(loops=6, seed=2026)

    assert first == second
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)


def test_loop_runner_outputs_required_metric_fields():
    payload = build_loop_results(loops=4, seed=1337)

    assert payload["schema_version"] == "canaryweave.autonomous_research_loops.safe.v1"
    assert payload["safety_boundary"] == "deterministic_local_simulator_only_no_provider_calls_no_network_no_raw_payloads"
    assert payload["aggregate"]["loop_count"] == 4
    assert payload["aggregate"]["modes"] == ["baseline", "mcp", "attest"]
    assert payload["aggregate"]["by_mode"].keys() == {"baseline", "mcp", "attest"}

    for loop in payload["loops"]:
        assert set(loop["metrics_by_mode"]) == {"baseline", "mcp", "attest"}
        assert loop["attack_mix"]
        assert loop["source_family_condition"] in {
            "mixed_structural_and_synthetic",
            "agentdojo_structural",
            "injecagent_structural",
            "synthetic_safe",
        }
        assert "amplification" in loop["comparisons"]
        assert "attest_reduction" in loop["comparisons"]
        assert loop["top_scenario_family_observations"]
        for metrics in loop["metrics_by_mode"].values():
            assert REQUIRED_METRIC_FIELDS <= metrics.keys()

    for metrics in payload["aggregate"]["by_mode"].values():
        assert REQUIRED_METRIC_FIELDS <= metrics.keys()
    assert "amplification" in payload["aggregate"]["comparisons"]
    assert "attest_reduction" in payload["aggregate"]["comparisons"]
    assert payload["aggregate"]["top_scenario_family_observations"]


def test_loop_runner_finding_mentions_sampling_abuse_without_raw_payloads():
    payload = build_loop_results(loops=5, seed=99)
    finding = payload["finding"]
    finding_text = json.dumps(finding, sort_keys=True).lower()

    assert finding["topic"] == "sampling_abuse"
    assert "sampling abuse" in finding["summary"].lower()
    assert "local simulator" in finding["summary"].lower()
    assert finding["raw_payloads_included"] is False
    assert all(marker not in finding_text for marker in FORBIDDEN_RAW_PAYLOAD_MARKERS)
    assert "CANARY_" not in json.dumps(payload)
