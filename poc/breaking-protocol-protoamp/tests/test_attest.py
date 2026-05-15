from dataclasses import replace

from protoamp.attest import sign_capability, verify_capability


def test_attestation_verifies_for_untampered_payload():
    attestation = sign_capability(
        b"test-secret", "scenario-1", "summarize_note", "summarize_note", "nonce-1"
    )

    assert verify_capability(b"test-secret", attestation) is True


def test_attestation_rejects_tampered_action_name():
    attestation = sign_capability(
        b"test-secret", "scenario-1", "summarize_note", "summarize_note", "nonce-1"
    )
    tampered = replace(attestation, action_name="emit_canary")

    assert verify_capability(b"test-secret", tampered) is False


def test_attestation_rejects_wrong_secret():
    attestation = sign_capability(
        b"test-secret", "scenario-1", "summarize_note", "summarize_note", "nonce-1"
    )

    assert verify_capability(b"other-secret", attestation) is False
