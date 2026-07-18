import pytest

from canaryweave.generator import generate_scenario, generate_suite
from canaryweave.safety import validate_scenario


def test_generate_scenario_is_deterministic():
    first = generate_scenario(1337, 3)
    second = generate_scenario(1337, 3)

    assert first == second
    assert first.id == "scenario-1337-0003"


def test_generate_suite_count_and_safety():
    suite = generate_suite(7, 5)

    assert len(suite) == 5
    assert len({scenario.id for scenario in suite}) == 5
    for scenario in suite:
        validate_scenario(scenario)
        assert scenario.expected_unauthorized


def test_generate_suite_rejects_negative_count():
    with pytest.raises(ValueError):
        generate_suite(1, -1)
