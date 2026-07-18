from canaryweave.generator import generate_scenario, generate_suite
from canaryweave.metrics import summarize_by_attack_type, summarize_by_scenario_family, summarize_by_source_family
from canaryweave.registry import default_registry
from canaryweave.scenario import AttackType, ScenarioMetadata, SourceFamily
from canaryweave.simulator import run_suite
from canaryweave.scenario import Mode
from canaryweave.source_adapters import synthetic_source_summary


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


def test_sampling_abuse_generation_covers_new_families_deterministically():
    registry = default_registry()
    expected = {
        "sampling_role_relabel_consensus",
        "sampling_context_window_shadowing",
        "sampling_candidate_replay_gap",
    }

    first = generate_suite(
        20260515,
        160,
        registry=registry,
        attack_type=AttackType.SAMPLING_ABUSE,
        source_summary=synthetic_source_summary(),
    )
    second = generate_suite(
        20260515,
        160,
        registry=registry,
        attack_type=AttackType.SAMPLING_ABUSE,
        source_summary=synthetic_source_summary(),
    )

    assert first == second
    assert expected <= {scenario.metadata.scenario_family for scenario in first}


def test_sampling_abuse_metadata_is_safe_and_payload_free():
    suite = generate_suite(
        8080,
        80,
        attack_type=AttackType.SAMPLING_ABUSE,
        source_summary=synthetic_source_summary(),
    )
    forbidden_fragments = tuple(
        [
            "ignore" + " previous",
            "system" + " prompt",
            "developer" + " message",
            "http" + "://",
            "https" + "://",
            "creden" + "tial",
            "pass" + "word",
        ]
    )

    for scenario in suite:
        metadata = scenario.typed_metadata
        metadata_text = " ".join(
            [
                metadata.scenario_family,
                metadata.attack_type.value,
                metadata.source_family.value,
                metadata.source_adapter,
                metadata.source_digest,
                metadata.abuse_axis,
                metadata.trust_failure,
                *metadata.notes.keys(),
                *metadata.notes.values(),
            ]
        ).lower()

        assert metadata.scenario_family.startswith("sampling_")
        assert metadata.attack_type is AttackType.SAMPLING_ABUSE
        assert "CANARY_" not in metadata_text
        assert all(fragment not in metadata_text for fragment in forbidden_fragments)


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
