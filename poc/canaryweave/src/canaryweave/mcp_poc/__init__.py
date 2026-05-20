"""Spec-shaped MCP stdio sampling POC for CanaryWeave.

This package is intentionally local-only and benign: the demo server exposes an
inert canary sink, the victim client uses a deterministic sampler, and the
hardened policy demonstrates origin-aware mitigation for server-initiated MCP
sampling requests.
"""

from .guardrail import GuardrailDecision, SamplingGuardrail
from .victim_client import McpSamplingPocResult, VictimPolicy, run_mcp_sampling_poc

__all__ = [
    "GuardrailDecision",
    "SamplingGuardrail",
    "McpSamplingPocResult",
    "VictimPolicy",
    "run_mcp_sampling_poc",
]
