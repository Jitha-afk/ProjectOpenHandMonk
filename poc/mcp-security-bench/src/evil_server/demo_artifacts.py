"""Shared demo artifact helpers for the evil MCP server.

Keeps all audience-facing proof files in one place so demos are easy to verify.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _resolve_path(path_str: str) -> Path:
    path = Path(path_str).expanduser()
    if not path.is_absolute():
        path = Path.cwd() / path
    return path


def get_artifacts_dir() -> Path:
    path = _resolve_path(os.environ.get("EVIL_MCP_ARTIFACTS_DIR", "artifacts"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_demo_event_log_path() -> Path:
    path = get_artifacts_dir() / "demo_events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_callback_log_path() -> Path:
    configured = os.environ.get("CALLBACK_LOG_FILE")
    path = _resolve_path(configured) if configured else get_artifacts_dir() / "callback_log.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_rug_pull_state_path() -> Path:
    configured = os.environ.get("EVIL_MCP_RUG_PULL_STATE_FILE")
    path = _resolve_path(configured) if configured else get_artifacts_dir() / "rugpull_state.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def write_text_artifact(name: str, content: str) -> Path:
    path = get_artifacts_dir() / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def append_text_artifact(name: str, content: str) -> Path:
    path = get_artifacts_dir() / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(content)
    return path


def log_event(event: str, **details: Any) -> Path:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "marker": "🚨 MCP DEMO ARTIFACT",
        **details,
    }
    path = get_demo_event_log_path()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return path
