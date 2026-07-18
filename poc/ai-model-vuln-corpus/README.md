# AI Model Vulnerability Corpus

> Build a source-backed corpus of vulnerable or intentionally unsafe AI model artifacts for controlled-lab security testing.

## Status
`complete — research inventory and engineering handoff`

The issue #3 research scope is complete. This workspace provides a source-backed candidate inventory, format coverage matrix, controlled-lab testing playbook, and executive summary. It does not contain acquired model artifacts, a downloader, a scanner, or product-efficacy results. Any acquisition or execution work requires a separately approved implementation phase.

See `FINAL_STATUS.md` for the closure record and validation boundaries.

## Objective
Create a comprehensive, evidence-backed inventory of AI model artifacts that are either intentionally vulnerable, incidentally unsafe, maliciously crafted, or widely discussed in security research as risky to load or distribute. The immediate goal is to identify strong candidates for later testing of Microsoft Defender for Cloud model security capabilities.

## Key Questions
- Which publicly discussed AI model artifacts or model packages are plausibly suitable as controlled test fixtures?
- Which artifact formats map cleanly to the Defender for Cloud supported format list?
- Which candidates are legal, safe, and practical to download and handle in an isolated lab?
- Where do we need synthetic or reconstructed samples because original artifacts are unavailable, unsafe, or legally unclear?

## Team Notes
- **Alan (Research):** Build the evidence-backed candidate inventory, with provenance, source URLs, confidence notes, and risk classification.
- **Mira (Writing):** Turn raw findings into a readable benchmark/report and operator documentation for future testing.
- **Turing (Engineering):** Define artifact intake, validation, and testability rules aligned to Defender-supported model formats and controlled-lab constraints.

## Findings
The completed research handoff is organized under `research/`, `design/`, and `docs/`. The strongest candidates favor controlled synthetic reconstruction and non-executing validation over acquiring opaque real-world artifacts.

## Structure
```
ai-model-vuln-corpus/
├── research/    ← Alan's research notes and raw findings
├── design/      ← Project planning, format mapping, evaluation rules
├── src/         ← Turing's helper code or automation if needed
├── tests/       ← Validation and fixture checks
└── docs/        ← Mira's polished documentation and write-ups
```

## Log
| Date | Agent | Update |
|------|-------|--------|
| 2026-04-14 | Hermes | Created project workspace for GitHub issue #3 and assigned workstreams to Alan, Mira, and Turing. |
