# MCP Enterprise Security Survival Guide

> Evidence-grounded enterprise defense guidance for the latest Model Context Protocol, backed by research synthesis, validation plans, and targeted proof-of-concept defenses.

## Status
`researching`

## Objective
Develop a practitioner/research hybrid project that turns the latest MCP specification into an enterprise security playbook: threat model, control framework, testable defense proposals, and a publishable paper draft with clearly labeled evidence boundaries.

## Key Questions
- Which MCP 2025-11-25 features introduce the most important net-new enterprise risks?
- Which defenses are already supported by the literature, and which remain hypotheses requiring validation?
- What minimal control stack should enterprises deploy before piloting MCP-enabled systems?
- What can be meaningfully validated through proof-of-concept experiments in this repo?
- What narrow security-critical core can be formalized with machine-checkable properties?

## Team Notes
- **Alan (Research):** Build the source inventory, map the current literature, identify gaps, and keep claims tied to citations.
- **Mira (Writing):** Turn the research and validation outputs into a careful paper blueprint and later a full draft.
- **Turing (Engineering):** Define proof-of-concept tracks, measurable success criteria, and a pragmatic formal-methods plan for the enforcement core.
- **Hermes (Orchestration):** Keep the scope coherent, challenge unsupported claims, sequence workstreams, and prepare branch/PR updates.

## Findings
Initial kickoff findings from the first literature intake suggest that current MCP security work already pays substantial attention to attack taxonomies, malicious server/tool behaviors, and early defensive ideas, but appears to provide less enterprise-deployable guidance for the latest spec surface — especially authorization, Streamable HTTP hardening, roots confinement, elicitation safety, sampling/tool trust chains, provenance, and private-registry control planes. This is a preliminary synthesis, not a final literature conclusion.

## Current Working Artifacts
- `research/source-inventory-and-gap-analysis.md` — literature intake memo, gap analysis, and first-wave research questions
- `design/validation-and-poc-plan.md` — validation program, proof-of-concept tracks, and formal-methods framing
- `docs/paper-blueprint.md` — working abstract, section map, evidence rules, and publication strategy

## Structure
```
mcp-enterprise-security-survival-guide/
├── research/    ← Literature inventory, source notes, claim tracking
├── design/      ← Threat model, validation plan, formal properties, project briefs
├── src/         ← Future prototype defenses and enforcement components
├── tests/       ← Replay fixtures, attack cases, property checks, and scorecards
└── docs/        ← Paper drafts, figure plans, and publication artifacts
```

## Log
| Date | Agent | Update |
|------|-------|--------|
| 2026-04-15 | Hermes | Created issue branch and project workspace from template |
| 2026-04-15 | Alan | Produced initial source inventory and gap analysis from `/home/sealjitha/toresearch` plus latest MCP spec |
| 2026-04-15 | Turing | Produced validation and proof-of-concept plan with measurable criteria and formal-core recommendation |
| 2026-04-15 | Mira | Produced paper blueprint with abstract draft, section map, figure plan, and publication strategy |
