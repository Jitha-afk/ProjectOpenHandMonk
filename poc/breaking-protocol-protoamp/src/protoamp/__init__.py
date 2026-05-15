"""Controlled PROTOAMP-style MCP protocol-safety benchmark POC.

This package intentionally uses only synthetic scenarios, benign canaries,
and local in-memory/logged actions. It is not a real MCP client/server and
must not be used to run offensive payloads.
"""

from .generator import generate_scenario, generate_suite
from .metrics import compare_by_mode, summarize, summarize_by_attack_type, summarize_by_scenario_family, summarize_by_source_family
from .scenario import ActionKind, AttackType, Mode, Scenario, ScenarioMetadata, SourceFamily, ToolAction
from .simulator import HostSimulator, run_suite

__all__ = [
    "ActionKind",
    "AttackType",
    "HostSimulator",
    "Mode",
    "Scenario",
    "ScenarioMetadata",
    "SourceFamily",
    "ToolAction",
    "compare_by_mode",
    "generate_scenario",
    "generate_suite",
    "run_suite",
    "summarize",
    "summarize_by_attack_type",
    "summarize_by_scenario_family",
    "summarize_by_source_family",
]
