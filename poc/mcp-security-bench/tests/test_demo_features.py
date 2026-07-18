from __future__ import annotations

import json
from pathlib import Path

import pytest

from evil_server.attacks import code_execution, command_injection
from evil_server.config import AttackConfig
from evil_server.server import create_server


@pytest.fixture
def artifact_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    artifacts = tmp_path / "artifacts"
    monkeypatch.setenv("EVIL_MCP_ARTIFACTS_DIR", str(artifacts))
    monkeypatch.delenv("EVIL_MCP_RUG_PULL_STATE_FILE", raising=False)
    monkeypatch.delenv("CALLBACK_LOG_FILE", raising=False)
    return artifacts


def _tool_names(mcp: object) -> set[str]:
    return set(getattr(mcp._tool_manager, "_tools").keys())


def test_create_server_registers_portable_rug_pull_state(
    artifact_dir: Path,
) -> None:
    mcp = create_server(AttackConfig.all_enabled())

    assert "get_weather" in _tool_names(mcp)
    state_file = artifact_dir / "rugpull_state.json"
    assert state_file.exists()
    state = json.loads(state_file.read_text())
    assert state == {"call_count": 0, "mutated": False}


@pytest.mark.asyncio
async def test_retrieve_document_uses_seeded_demo_payload_and_logs_artifact(
    artifact_dir: Path,
) -> None:
    mcp = create_server(AttackConfig.all_enabled())
    retrieve_document = mcp._tool_manager._tools["retrieve_document"].fn

    result = await retrieve_document("readme")

    assert "IMPORTANT" in result
    assert "internal://credentials" in result
    event_log = artifact_dir / "demo_events.jsonl"
    assert event_log.exists()
    log_text = event_log.read_text()
    assert "prompt_injection_retrieve" in log_text
    assert '"doc_id": "readme"' in log_text


@pytest.mark.asyncio
async def test_resource_reads_are_logged_for_demo_visibility(
    artifact_dir: Path,
) -> None:
    mcp = create_server(AttackConfig.all_enabled())

    await mcp.read_resource("internal://credentials")

    event_log = artifact_dir / "demo_events.jsonl"
    assert event_log.exists()
    log_text = event_log.read_text()
    assert "resource_read" in log_text
    assert "internal://credentials" in log_text


def test_run_command_and_dns_lookup_aliases_are_registered(artifact_dir: Path) -> None:
    mcp = create_server(AttackConfig.all_enabled())

    names = _tool_names(mcp)
    assert "run_command" in names
    assert "dns_lookup" in names


def test_windows_command_helpers_use_windows_variants(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(command_injection.platform, "system", lambda: "Windows")

    assert command_injection._build_ping_command("example.com", 4).startswith("ping -n 4 ")
    assert command_injection._build_traceroute_command("example.com").startswith("tracert ")
    assert command_injection._build_dns_lookup_command("example.com").startswith("nslookup ")


def test_python_execution_uses_current_interpreter() -> None:
    assert code_execution._python_command() == code_execution.sys.executable
