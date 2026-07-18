from __future__ import annotations

import json
from typing import Any

from mcp import types

from .common import DETERMINISTIC_MODEL, ScenarioConfig


def deterministic_sampling_result(config: ScenarioConfig) -> types.CreateMessageResult:
    """Return an MCP CreateMessageResult containing a benign inert action plan.

    This is the POC's deterministic stand-in for an LLM. It lets tests and demos
    exercise the MCP sampling flow without calling a model provider or exposing
    any real secrets, external endpoints, or harmful instructions.
    """

    plan: dict[str, Any] = {
        "action": config.inert_sink_action,
        "marker": config.canary,
        "sink": "inert_demo_audit_log",
        "source": "server_sampling",
        "scenario_id": config.scenario_id,
    }
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(type="text", text=json.dumps(plan, sort_keys=True)),
        model=DETERMINISTIC_MODEL,
        stopReason="endTurn",
    )


def extract_text_content(content: Any) -> str:
    """Extract text from MCP content blocks used in the POC."""

    if isinstance(content, list):
        return "\n".join(extract_text_content(item) for item in content)
    if hasattr(content, "text"):
        return str(content.text)
    if isinstance(content, dict):
        return str(content.get("text", ""))
    return str(content)
