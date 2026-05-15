from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Attestation:
    """Test-only capability attestation bound to one symbolic action."""

    scenario_id: str
    action_name: str
    capability: str
    nonce: str
    signature: str


def canonical_payload(
    scenario_id: str, action_name: str, capability: str, nonce: str
) -> bytes:
    payload = {
        "scenario_id": scenario_id,
        "action_name": action_name,
        "capability": capability,
        "nonce": nonce,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sign_capability(
    secret: bytes, scenario_id: str, action_name: str, capability: str, nonce: str
) -> Attestation:
    payload = canonical_payload(scenario_id, action_name, capability, nonce)
    signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()
    return Attestation(scenario_id, action_name, capability, nonce, signature)


def verify_capability(secret: bytes, attestation: Attestation) -> bool:
    expected = sign_capability(
        secret,
        attestation.scenario_id,
        attestation.action_name,
        attestation.capability,
        attestation.nonce,
    )
    return hmac.compare_digest(expected.signature, attestation.signature)


def attestation_to_dict(attestation: Attestation) -> dict[str, str]:
    return asdict(attestation)
