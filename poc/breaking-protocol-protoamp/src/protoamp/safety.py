from __future__ import annotations

import re

from .scenario import ActionKind, Scenario, ScenarioMetadata, ToolAction


class SafetyError(ValueError):
    """Raised when synthetic benchmark content violates safety guardrails."""


ALLOWED_ACTIONS = frozenset(
    {
        "read_public_note",
        "summarize_note",
        "write_report",
        "classify_note",
        "transform_text",
        "emit_canary",
        "append_extra_marker",
        "toggle_test_flag",
        "record_decoy_value",
    }
)

ALLOWED_CAPABILITIES = ALLOWED_ACTIONS

SAFE_LABEL_RE = re.compile(r"^[A-Za-z0-9_.:, -]+$")
DIGEST_RE = re.compile(r"^(synthetic:[a-z0-9_.-]+|sha256:[0-9a-f]{64})$")

RISKY_TOKENS = tuple(
    token.lower()
    for token in [
        "http://",
        "https://",
        "ftp://",
        "curl ",
        "wget ",
        "ssh ",
        "bash ",
        "powershell",
        "subprocess",
        "socket",
        "webhook",
        "exfil",
        "exfiltrate",
        "steal",
        "credential",
        "password",
        "api_key",
        "apikey",
        "secret_key",
        "private_key",
        "access_token",
        "bearer ",
        "sk_live",
        "sk_test",
        "ghp_",
        "akia",
        "/etc/passwd",
        ".env",
        "rm -rf",
        "chmod",
        "reverse shell",
    ]
)


def assert_safe_text(text: str) -> None:
    if not isinstance(text, str):
        raise SafetyError("text must be a string")
    if not text or not text.strip():
        raise SafetyError("text must be non-empty")
    if len(text) > 2_000:
        raise SafetyError("text is too long for the controlled POC")
    lowered = text.lower()
    for token in RISKY_TOKENS:
        if token in lowered:
            raise SafetyError(f"risky token rejected: {token}")
    # Prevent command-like snippets with multiple shell metacharacters. Single
    # punctuation is fine in prose; clusters are unnecessary in synthetic cases.
    metachar_count = sum(text.count(ch) for ch in [";", "|", "`", "$", "&&", "||"])
    if metachar_count >= 2:
        raise SafetyError("command-like metacharacter cluster rejected")


def validate_metadata(metadata: ScenarioMetadata) -> None:
    for value in [
        metadata.scenario_family,
        metadata.attack_type.value,
        metadata.source_family.value,
        metadata.source_adapter,
        metadata.abuse_axis,
        metadata.trust_failure,
    ]:
        assert_safe_text(str(value))
        if not SAFE_LABEL_RE.match(str(value)):
            raise SafetyError(f"unsafe metadata label: {value}")
    if metadata.source_record_count < 0:
        raise SafetyError("source_record_count must be non-negative")
    if not DIGEST_RE.match(metadata.source_digest):
        raise SafetyError("unsafe source digest")
    for key, value in metadata.notes.items():
        assert_safe_text(str(key))
        assert_safe_text(str(value))


def validate_action(action: ToolAction) -> None:
    if action.name not in ALLOWED_ACTIONS:
        raise SafetyError(f"action not allowlisted: {action.name}")
    if action.capability not in ALLOWED_CAPABILITIES:
        raise SafetyError(f"capability not allowlisted: {action.capability}")
    if not isinstance(action.kind, ActionKind):
        raise SafetyError("action kind must be an ActionKind")
    for value in [action.name, action.capability, action.kind.value, *action.args.values()]:
        assert_safe_text(str(value))


def validate_scenario(scenario: Scenario) -> None:
    assert_safe_text(scenario.id)
    assert_safe_text(scenario.user_goal)
    assert_safe_text(scenario.context)
    for capability in scenario.allowed_capabilities:
        if capability not in ALLOWED_CAPABILITIES:
            raise SafetyError(f"scenario capability not allowlisted: {capability}")
    if not scenario.canaries:
        raise SafetyError("scenario must contain at least one canary")
    for canary in scenario.canaries:
        assert_safe_text(canary)
        if not canary.startswith("CANARY_"):
            raise SafetyError("canaries must use CANARY_ prefix")
    if not scenario.actions:
        raise SafetyError("scenario must contain actions")
    action_names = {action.name for action in scenario.actions}
    for action in scenario.actions:
        validate_action(action)
    for expected in scenario.expected_unauthorized:
        if expected not in action_names:
            raise SafetyError(f"expected unauthorized action missing: {expected}")
    validate_metadata(scenario.typed_metadata)
