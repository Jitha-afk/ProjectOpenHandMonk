from canaryweave_fides.adapters import AdapterConfig, SyntheticAdapter
from canaryweave_fides.reporting import build_public_report
from canaryweave_fides.runner import EvaluationRunConfig, run_evaluation


def test_public_report_summarizes_security_and_maintainability_metrics():
    raw = run_evaluation(EvaluationRunConfig(adapters=(SyntheticAdapter(AdapterConfig()),), iterations=2))

    report = build_public_report(raw)

    assert report["schema_version"] == "canaryweave_fides.public_report.v1"
    assert report["total_iterations"] == raw["total_iterations"]
    assert "asr" in report["security_metrics"]["no_guard"]
    assert "asr_reduction_vs_regex" in report["security_metrics"]["yara_rules"]
    assert report["incremental_metrics"]["warden_incremental_catches_vs_regex"] >= 0
    assert report["incremental_metrics"]["fides_incremental_catches_vs_warden"] >= 0
    assert report["maintainability_metrics"]["rule_engine_codename"] == "WARDEN"
    assert report["safety"]["public_safe"] is True


def test_public_report_does_not_include_case_level_payload_fields():
    raw = run_evaluation(EvaluationRunConfig(adapters=(SyntheticAdapter(AdapterConfig(max_cases=1)),), iterations=1))
    report = build_public_report(raw)
    text = str(report).lower()

    assert "case_results" not in report
    assert "raw_ref" not in text
    assert "private_data" not in text
    assert "payload" not in text


def test_public_report_omits_model_output_and_judge_transcripts_from_private_rows():
    raw = run_evaluation(EvaluationRunConfig(adapters=(SyntheticAdapter(AdapterConfig(max_cases=1)),), iterations=1))
    raw["case_results"][0]["decisions"][0]["model_output"] = "PRIVATE_MODEL_OUTPUT_SHOULD_NOT_BE_PUBLIC"
    raw["case_results"][0]["decisions"][0]["judge_transcript"] = "PRIVATE_JUDGE_TRANSCRIPT_SHOULD_NOT_BE_PUBLIC"

    report = build_public_report(raw)
    text = str(report)

    assert "PRIVATE_MODEL_OUTPUT_SHOULD_NOT_BE_PUBLIC" not in text
    assert "PRIVATE_JUDGE_TRANSCRIPT_SHOULD_NOT_BE_PUBLIC" not in text
    assert report["safety"]["model_outputs_included"] is False
    assert report["safety"]["judge_transcripts_included"] is False


def test_incremental_metrics_keys_include_case_id_to_avoid_collisions():
    raw = {
        "schema_version": "canaryweave_fides.gate_eval.v1",
        "iterations": 1,
        "total_cases": 2,
        "total_iterations": 2,
        "provider_calls": 0,
        "case_results": [
            {
                "case_id": "case.allowed",
                "dataset_id": "synthetic",
                "case_kind": "attack",
                "attack_category": "same_category",
                "surface": "mcp_tool",
                "iteration": 0,
                "decisions": [
                    {"stack": "regex_baseline", "decision": "allow", "rule_ids": []},
                    {"stack": "yara_rules", "decision": "allow", "rule_ids": []},
                    {"stack": "rules_plus_fides", "decision": "allow", "rule_ids": []},
                ],
            },
            {
                "case_id": "case.blocked",
                "dataset_id": "synthetic",
                "case_kind": "attack",
                "attack_category": "same_category",
                "surface": "mcp_tool",
                "iteration": 0,
                "decisions": [
                    {"stack": "regex_baseline", "decision": "block", "rule_ids": ["regex.marker"]},
                    {"stack": "yara_rules", "decision": "block", "rule_ids": ["cwfr-0001"]},
                    {"stack": "rules_plus_fides", "decision": "block", "rule_ids": ["cwfr-0001"]},
                ],
            },
        ],
    }

    report = build_public_report(raw)

    assert report["incremental_metrics"]["warden_incremental_catches_vs_regex"] == 0
