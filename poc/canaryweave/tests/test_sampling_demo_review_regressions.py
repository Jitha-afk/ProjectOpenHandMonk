import importlib.util
import json
from pathlib import Path

from canaryweave.demo_sampling import build_sampling_demo_suite, evaluate_sampling_demo_suite
from canaryweave.safety import RISKY_TOKENS


def _load_sampling_demo_script():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "sampling_demo.py"
    spec = importlib.util.spec_from_file_location("sampling_demo_script", script_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build_payload = _load_sampling_demo_script().build_payload


def _json_text(value: object) -> str:
    return json.dumps(value, sort_keys=True).lower()


def test_sampling_demo_artifact_rejects_risky_runtime_tokens():
    payload = build_payload()
    text = _json_text(payload)

    banned = [token for token in RISKY_TOKENS if token in text]

    assert banned == []


def test_sampling_demo_transcripts_preserve_request_provenance_and_canary_flow():
    suite = build_sampling_demo_suite()
    result = evaluate_sampling_demo_suite(suite)
    scenarios_by_id = {scenario.scenario_id: scenario for scenario in suite.scenarios}

    assert len(result.transcripts) == len(suite.scenarios)
    for transcript in result.transcripts:
        scenario = scenarios_by_id[transcript.scenario_id]
        request = scenario.sampling_request

        assert request.jsonrpc == "2.0"
        assert request.method == transcript.jsonrpc_method == "sampling/createMessage"
        assert request.origin == "server"
        assert request.claimed_role == transcript.claimed_role == "user"
        assert request.canary_label.startswith("DEMO_CANARY_")
        assert transcript.vulnerable_decision.action_kind == "unauthorized"
        assert transcript.hardened_decision.action_kind == "unauthorized"
        assert transcript.vulnerable_decision.canary_touched is True
        assert transcript.hardened_decision.canary_touched is False
        assert scenario.unauthorized_action.args["sink"] == "inert_demo_audit_log"


def test_sampling_demo_payload_labels_result_as_deterministic_not_prevalence():
    payload = build_payload()
    claim_text = _json_text(payload.get("claim", ""))
    scope_text = _json_text(payload.get("scope", {}))

    assert "deterministic" in claim_text + scope_text
    assert "intentionally vulnerable" in claim_text + scope_text
    assert "not ecosystem prevalence" in claim_text + scope_text
    assert "not live-model" in claim_text + scope_text
    assert "not a full mcp wire trace" in claim_text + scope_text


def test_sampling_demo_docs_explain_narrative_algorithm_labels():
    docs = "\n".join(
        Path(path).read_text(encoding="utf-8").lower()
        for path in [
            "docs/sampling_attack_demo.md",
            "docs/attack_claim_alignment.md",
            "docs/research_paper_draft.md",
        ]
    )

    assert "does not run an actual best-of-n sampler" in docs
    assert "does not run a self-consistency vote" in docs
    assert "does not run a separate verifier model" in docs
    assert "does not instantiate a real mcp client" in docs
