import pytest

from canaryweave.registry import ScenarioFamilySpec, ScenarioRegistry, default_registry
from canaryweave.scenario import AttackType, SourceFamily
from canaryweave.source_adapters import synthetic_source_summary


def _dummy_builder(seed, index, source_summary):
    from canaryweave.generator import build_registered_scenario

    return build_registered_scenario(
        seed=seed,
        index=index,
        scenario_family="dummy_family",
        attack_type=AttackType.SAMPLING_ABUSE,
        source_family=SourceFamily.SYNTHETIC_SAFE,
        source_adapter="synthetic_static",
        abuse_axis="dummy_axis",
        trust_failure="dummy_boundary",
        allowed_action="summarize_note",
        unauthorized_action="emit_canary",
        source_summary=source_summary or synthetic_source_summary(),
    )


def _spec(name="dummy_family", weight=1):
    return ScenarioFamilySpec(
        name=name,
        attack_type=AttackType.SAMPLING_ABUSE,
        source_family=SourceFamily.SYNTHETIC_SAFE,
        source_adapter="synthetic_static",
        abuse_axis="dummy_axis",
        trust_failure="dummy_boundary",
        weight=weight,
        builder=_dummy_builder,
        description="Dummy safe family.",
    )


def test_default_registry_contains_sampling_abuse_majority():
    registry = default_registry()

    sampling_weight = sum(spec.weight for spec in registry.by_attack_type(AttackType.SAMPLING_ABUSE))
    other_weight = sum(
        spec.weight for spec in registry.all() if spec.attack_type is not AttackType.SAMPLING_ABUSE
    )

    assert sampling_weight > other_weight
    assert "sampling_majority_canary_echo" in registry.weighted_names()


def test_default_registry_contains_new_sampling_families():
    registry = default_registry()
    names = {spec.name for spec in registry.by_attack_type(AttackType.SAMPLING_ABUSE)}

    assert {
        "sampling_role_relabel_consensus",
        "sampling_context_window_shadowing",
        "sampling_candidate_replay_gap",
    } <= names


def test_sampling_weight_exceeds_all_secondary_classes_combined():
    registry = default_registry()

    sampling_weight = sum(spec.weight for spec in registry.by_attack_type(AttackType.SAMPLING_ABUSE))
    secondary_weight = sum(
        spec.weight
        for spec in registry.all()
        if spec.attack_type is not AttackType.SAMPLING_ABUSE
    )

    assert sampling_weight > secondary_weight
    assert sampling_weight > (2 * secondary_weight)


def test_registry_rejects_duplicate_family_name():
    registry = ScenarioRegistry()
    registry.register(_spec())

    with pytest.raises(ValueError):
        registry.register(_spec())


def test_registry_rejects_non_positive_weight():
    with pytest.raises(ValueError):
        _spec(weight=0)


def test_registry_filters_by_attack_type():
    specs = default_registry().by_attack_type(AttackType.CAPABILITY_ATTESTATION_ABSENCE)

    assert specs
    assert all(spec.attack_type is AttackType.CAPABILITY_ATTESTATION_ABSENCE for spec in specs)
