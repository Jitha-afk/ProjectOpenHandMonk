from protoamp.generator import generate_scenario, generate_suite
from protoamp.metrics import summarize_by_attack_type, summarize_by_scenario_family, summarize_by_source_family
from protoamp.scenario import AttackType, ScenarioMetadata, SourceFamily
from protoamp.simulator import run_suite
from protoamp.scenario import Mode
from protoamp.source_adapters import synthetic_source_summary


def test_generate_sampling_abuse_scenario_has_typed_metadata():
    scenario = generate_scenario(
        1337,
        0,
        attack_type=AttackType.SAMPLING_ABUSE,
        source_summary=synthetic_source_summary(),
    )

    assert isinstance(scenario.metadata, ScenarioMetadata)
    assert scenario.metadata.attack_type is AttackType.SAMPLING_ABUSE
    assert scenario.metadata.scenario_family.startswith("sampling_")
    assert scenario.metadata.source_family in SourceFamily
    assert scenario.expected_unauthorized


def test_sampling_abuse_generation_is_deterministic():
    first = generate_scenario(2026, 4, attack_type=AttackType.SAMPLING_ABUSE)
    second = generate_scenario(2026, 4, attack_type=AttackType.SAMPLING_ABUSE)

    assert first == second


def test_default_suite_is_sampling_weighted():
    suite = generate_suite(42, 50)
    sampling_count = sum(
        scenario.metadata.attack_type is AttackType.SAMPLING_ABUSE for scenario in suite
    )

    assert sampling_count > 35


def test_metrics_group_by_attack_source_and_scenario_family():
    scenarios = generate_suite(7, 12)
    results = run_suite(scenarios, Mode.MCP)

    by_attack = summarize_by_attack_type(results, scenarios)
    by_source = summarize_by_source_family(results, scenarios)
    by_family = summarize_by_scenario_family(results, scenarios)

    assert AttackType.SAMPLING_ABUSE.value in by_attack
    assert by_attack[AttackType.SAMPLING_ABUSE.value].attack_success_rate == 1.0
    assert by_source
    assert by_family
