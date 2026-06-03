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
