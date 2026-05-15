"""Controlled PROTOAMP-style MCP protocol-safety benchmark POC.

This package intentionally uses only synthetic scenarios, benign canaries,
and local in-memory/logged actions. It is not a real MCP client/server and
must not be used to run offensive payloads.
"""

from .generator import generate_scenario, generate_suite
from .metrics import compare_by_mode, summarize
from .scenario import ActionKind, Mode, Scenario, ToolAction
from .simulator import HostSimulator, run_suite

__all__ = [
    "ActionKind",
    "HostSimulator",
    "Mode",
    "Scenario",
    "ToolAction",
    "compare_by_mode",
    "generate_scenario",
    "generate_suite",
    "run_suite",
    "summarize",
]
