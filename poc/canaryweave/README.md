# CanaryWeave ASR Research Harness

> Controlled CanaryWeave research harness for studying MCP protocol-level trust boundaries with benign canaries and simulated actions.

## Status
`validated` / `research finding drafted`

## Objective
Build a safe, deterministic proof-of-concept that reconstructs the experimental shape of the source paper without using the authors' unavailable benchmark code, raw exploit payloads, real secrets, or outbound exfiltration.

The POC implements:
- synthetic MCP-protocol-confusion scenarios;
- a typed ASR scenario registry with sampling-abuse majority weighting;
- safe structural source adapters for AgentDojo and InjecAgent local clones;
- a toy host simulator for `baseline`, `mcp`, and `attest` conditions;
- JSON-RPC-shaped event logging;
- benign ASR/amplification metrics grouped by attack/source/scenario family;
- an ATTESTMCP-inspired HMAC/capability shim;
- a safe model-ASR dry-run scaffold for Hermes/Klive model research;
- a research-paper draft with explicit evidence boundaries.

## Key Questions
- Can we build a safe CanaryWeave-like harness from the paper's public methodology?
- What exact claims in "the source paper" are reproducible from the text alone, and what requires missing artifacts?
- How should simulated unauthorized-action execution metrics be computed without harmful payloads or real exfiltration?
- Does a message-level attestation/policy shim block synthetic protocol-confusion actions in this controlled harness?

## Team Notes
- **Alan (Research):** Source-grounded brief in `research/alan_source_brief.md`.
- **Mira (Writing):** Paper outline in `docs/mira_paper_outline.md`; final draft in `docs/research_paper_draft.md`.
- **Turing (Engineering):** Implementation plan in `design/turing_implementation_plan.md`; Python package in `src/canaryweave/`.
- **Klive (Evaluation):** Metrics protocol in `research/klive_metrics_protocol.md`.

## Findings
- The source paper describes a protocol-safety methodology but does not provide a public code URL or full payload/scenario corpus in the local copy.
- A faithful 847-scenario numeric reproduction is therefore not supported from the source text alone.
- This POC safely reconstructs the measurement shape: matched baseline/MCP/attested conditions, symbolic capabilities, JSON-RPC traces, benign canaries, and deterministic ASR-style metrics.
- AgentDojo and InjecAgent were inspected only for structural metadata: paths, counts, schema/category labels, hashes, task/tool surfaces, and benchmark shape. Raw upstream adversarial payload text is not copied into scenarios, docs, tests, or logs.
- New ASR-style scenario families primarily model sampling abuse: majority-vote candidate echo, temperature boundary drift, best-of-n overreach, self-consistency label drift, and verifier-gap decoy acceptance. Secondary families cover capability-attestation absence and implicit trust propagation.
- 50-loop local finding: sampling abuse dominates the scenario mix (1,181 / 1,200 scenario instances). In the deterministic simulator, the intentionally permissive `mcp` mode has a simulated unauthorized-action execution rate of 1.0, while local `attest` has 0.0.
- Conference demo finding: four JSON-RPC-shaped `sampling/createMessage` scenarios demonstrate role/provenance confusion with a precise success predicate: an unauthorized inert action executes from server-originated sampling content. The vulnerable host ASR is 4/4 and the hardened host ASR is 0/4.

These are controlled harness/demo results, not claims about all real MCP hosts, live model behavior, or the source paper's reported ASR values.

The sampling demo is a deterministic policy demonstration, not a live-model stochastic evaluation or full MCP wire trace. Scenario labels such as best-of-n, self-consistency, and verifier gap are illustrative subcases encoded as safe local scenario text/metadata.

## Quickstart

From this directory:

```bash
uv run --with pytest pytest -q
PYTHONPATH=src python3 -m canaryweave.cli --seed 1337 --count 20 --mode baseline --log artifacts/runs/baseline.jsonl
PYTHONPATH=src python3 -m canaryweave.cli --seed 1337 --count 20 --mode mcp --log artifacts/runs/mcp.jsonl
PYTHONPATH=src python3 -m canaryweave.cli --seed 1337 --count 20 --mode attest --log artifacts/runs/attest.jsonl
```

Sampling-only dry run:

```bash
PYTHONPATH=src python3 -m canaryweave.cli --seed 1337 --count 20 --attack-type sampling_abuse --mode mcp
```

Safe model-ASR plan generation, with no provider API calls:

```bash
PYTHONPATH=src python3 scripts/model_asr_dry_run.py --model-set smoke_core --seed 1337 --count 4 --output artifacts/runs/model_dry_run.json
PYTHONPATH=src python3 scripts/sampling_demo.py --output artifacts/research/sampling_demo.json
PYTHONPATH=src python3 scripts/autonomous_research_loops.py --loops 50 --output artifacts/research/loop_results.json
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
canaryweave/
├── configs/     ← safe disabled-by-default model registry placeholders
├── research/    ← Alan/Klive source notes, mappings, and metrics protocol
├── design/      ← Turing implementation plans
├── scripts/     ← dry-run helpers that do not call provider APIs
├── src/         ← controlled Python harness
├── tests/       ← pytest validation
├── artifacts/   ← local JSONL smoke traces
└── docs/        ← Mira outline, scaffold docs, and research paper draft
```

## Log
| Date | Agent | Update |
|------|-------|--------|
| 2026-05-15 | Hermes | Created POC branch/folder and delegated research, design, metrics, and writing workstreams. |
| 2026-05-15 | Alan | Wrote source-grounded brief; identified missing source artifact and reproduction limits. |
| 2026-05-15 | Turing | Designed controlled CanaryWeave/ATTESTMCP harness. |
| 2026-05-15 | Klive | Defined deterministic ASR/amplification metrics. |
| 2026-05-15 | Mira | Drafted paper outline and evidence-boundary language. |
| 2026-05-15 | Hermes | Implemented harness, tests, CLI, and smoke traces. |
| 2026-05-15 | Alan/Klive/Turing | Mapped AgentDojo/InjecAgent structures, model-ASR protocol, and sampling-abuse scenario plan without raw payloads. |
| 2026-05-15 | Hermes | Added typed ASR registry, safe source adapters, sampling-weighted generation, grouped metrics, and model dry-run scaffold. |
| 2026-05-15 | Hermes | Added conference-safe deterministic sampling demo and claim-alignment guardrails. |
