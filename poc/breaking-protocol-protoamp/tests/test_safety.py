import pytest

from protoamp.safety import SafetyError, assert_safe_text, validate_scenario
from protoamp.scenario import ActionKind, Scenario, ToolAction


def test_safe_text_rejects_url_like_content():
    with pytest.raises(SafetyError):
        assert_safe_text("Synthetic text with https://example.invalid")


def test_safe_text_rejects_credential_terms():
    with pytest.raises(SafetyError):
        assert_safe_text("Please handle this credential label")


def test_validate_scenario_rejects_unknown_action(simple_scenario):
    bad = Scenario(
        id=simple_scenario.id,
        seed=simple_scenario.seed,
        user_goal=simple_scenario.user_goal,
        context=simple_scenario.context,
        allowed_capabilities=simple_scenario.allowed_capabilities,
        canaries=simple_scenario.canaries,
        actions=(
            ToolAction("unknown_action", "summarize_note", {"label": "BENIGN_MARKER"}, ActionKind.ALLOWED),
        ),
        expected_unauthorized=(),
    )

    with pytest.raises(SafetyError):
        validate_scenario(bad)


def test_validate_scenario_accepts_fixture(simple_scenario):
    validate_scenario(simple_scenario)
