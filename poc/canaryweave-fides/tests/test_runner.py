from canaryweave_fides.adapters import AdapterConfig, SyntheticAdapter
from canaryweave_fides.runner import EvaluationRunConfig, run_evaluation


def test_runner_repeats_cases_for_configured_iterations():
    adapter = SyntheticAdapter(AdapterConfig(max_cases=1))

    report = run_evaluation(EvaluationRunConfig(adapters=(adapter,), iterations=3))

    assert report["schema_version"] == "canaryweave_fides.gate_eval.v1"
    assert report["iterations"] == 3
    assert report["total_cases"] == 1
    assert report["total_iterations"] == 3
    assert report["provider_calls"] == 0
    assert set(report["defense_stacks"]) == {"no_guard", "regex_baseline", "yara_rules", "rules_plus_fides"}
    assert report["defense_stacks"]["no_guard"]["allow"] == 3
    assert report["defense_stacks"]["yara_rules"]["block"] >= 1
    assert "adapter_results" in report
    assert report["adapter_results"][0]["dataset_id"] == "synthetic"


def test_runner_defaults_to_fifty_iterations():
    adapter = SyntheticAdapter(AdapterConfig(max_cases=1))
    config = EvaluationRunConfig(adapters=(adapter,))

    report = run_evaluation(config)

    assert report["iterations"] == 50
    assert report["total_iterations"] == 50


def test_runner_output_is_public_safe():
    adapter = SyntheticAdapter(AdapterConfig(max_cases=1))
    report = run_evaluation(EvaluationRunConfig(adapters=(adapter,), iterations=1))
    text = str(report).lower()

    assert "raw_ref" not in text
    assert "private_data" not in text
