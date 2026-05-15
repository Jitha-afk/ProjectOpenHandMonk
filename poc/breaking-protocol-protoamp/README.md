# Breaking Protocol PROTOAMP POC

> Controlled PROTOAMP-style research harness for studying MCP protocol-level trust boundaries with benign canaries and simulated actions.

## Status
`building` / `testing`

## Objective
Build a safe, deterministic proof-of-concept that reproduces the experimental shape of the paper "Breaking the Protocol" without using the authors' unavailable PROTOAMP code, raw exploit payloads, real secrets, or outbound exfiltration.

The POC implements:
- synthetic MCP-protocol-confusion scenarios;
- a toy host simulator for `baseline`, `mcp`, and `attest` conditions;
- JSON-RPC-shaped event logging;
- benign ASR/amplification metrics;
- an ATTESTMCP-inspired HMAC/capability shim;
- a research-paper draft with explicit evidence boundaries.

## Key Questions
- Can we build a safe PROTOAMP-like harness from the paper's public methodology?
- What exact claims in "Breaking the Protocol" are reproducible from the text alone, and what requires missing artifacts?
- How should ASR-like metrics be computed without harmful payloads or real exfiltration?
- Does a message-level attestation/policy shim block synthetic protocol-confusion actions in this controlled harness?

## Team Notes
- **Alan (Research):** Source-grounded brief in `research/alan_source_brief.md`.
- **Mira (Writing):** Paper outline in `docs/mira_paper_outline.md`; final draft in `docs/research_paper_draft.md`.
- **Turing (Engineering):** Implementation plan in `design/turing_implementation_plan.md`; Python package in `src/protoamp/`.
- **Klive (Evaluation):** Metrics protocol in `research/klive_metrics_protocol.md`.

## Findings
- The paper describes PROTOAMP's methodology but does not provide a public code URL or full payload/scenario corpus in the local copy.
- A faithful 847-scenario numeric reproduction is therefore not supported from the paper text alone.
- This POC safely reproduces the measurement shape: matched baseline/MCP/attested conditions, symbolic capabilities, JSON-RPC traces, benign canaries, and deterministic ASR-style metrics.
- Smoke result with seed 1337/count 5:
  - `baseline`: ASR 0.0, canary touch rate 0.0
  - `mcp`: ASR 1.0, canary touch rate 1.0
  - `attest`: ASR 0.0, canary touch rate 0.0

These are toy-harness results, not claims about real MCP hosts or the original paper's reported ASR values.

## Quickstart

From this directory:

```bash
uv run --with pytest pytest -q
PYTHONPATH=src python3 -m protoamp.cli --seed 1337 --count 20 --mode baseline --log artifacts/runs/baseline.jsonl
PYTHONPATH=src python3 -m protoamp.cli --seed 1337 --count 20 --mode mcp --log artifacts/runs/mcp.jsonl
PYTHONPATH=src python3 -m protoamp.cli --seed 1337 --count 20 --mode attest --log artifacts/runs/attest.jsonl
```

## Safety Boundaries
- No real MCP client/server integration.
- No outbound network calls.
- No filesystem reads of secrets or environment variables.
- No raw exploit payloads in scenarios, docs, or tests.
- Only synthetic `CANARY_*` markers and inert local logs.
- The safety validator rejects URL-like, credential-like, command-like, and exfiltration-related text.

## Structure
```
breaking-protocol-protoamp/
├── research/    ← Alan/Klive source notes and metrics protocol
├── design/      ← Turing implementation plan
├── src/         ← controlled Python harness
├── tests/       ← pytest validation
├── artifacts/   ← local JSONL smoke traces
└── docs/        ← Mira outline and research paper draft
```

## Log
| Date | Agent | Update |
|------|-------|--------|
| 2026-05-15 | Hermes | Created POC branch/folder and delegated research, design, metrics, and writing workstreams. |
| 2026-05-15 | Alan | Wrote source-grounded brief; identified missing PROTOAMP artifact and reproduction limits. |
| 2026-05-15 | Turing | Designed controlled PROTOAMP/ATTESTMCP harness. |
| 2026-05-15 | Klive | Defined deterministic ASR/amplification metrics. |
| 2026-05-15 | Mira | Drafted paper outline and evidence-boundary language. |
| 2026-05-15 | Hermes | Implemented harness, tests, CLI, and smoke traces. |
