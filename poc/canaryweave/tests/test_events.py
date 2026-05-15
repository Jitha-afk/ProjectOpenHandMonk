import json

from canaryweave.events import Event, JsonRpcEventLogger


def test_event_serializes_as_jsonrpc_shape():
    event = Event(
        event_type="decision",
        scenario_id="scenario-1",
        mode="attest",
        action="summarize_note",
        capability="summarize_note",
        allowed=True,
        reason="attestation_valid",
        canary_touched=False,
        sequence=1,
    )

    payload = event.to_jsonrpc()

    assert payload["jsonrpc"] == "2.0"
    assert payload["method"] == "canaryweave.event"
    assert payload["id"] == "scenario-1:1"
    assert payload["params"]["allowed"] is True


def test_logger_writes_jsonl(tmp_path):
    log_path = tmp_path / "events.jsonl"
    logger = JsonRpcEventLogger(log_path)
    logger.log(
        Event(
            "decision",
            "scenario-1",
            "mcp",
            "emit_canary",
            "emit_canary",
            False,
            "denied_unauthorized_kind",
            False,
            1,
        )
    )
    logger.close()

    line = log_path.read_text(encoding="utf-8").strip()
    parsed = json.loads(line)
    assert parsed["jsonrpc"] == "2.0"
    assert parsed["params"]["reason"] == "denied_unauthorized_kind"
