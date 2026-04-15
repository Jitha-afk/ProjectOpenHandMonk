# Source bibliography notes

This note is a compact drafting scaffold for issue #6: use the citation key in outlines and manuscript notes, treat the “what it supports” column as the safest current use of each source, and let the confidence note determine whether a source can support only framing language or stronger claims after closer reading. The duplicate `Securing the Model Context Protocol...` PDF is intentionally collapsed into one row.

| Citation key | Short title | Source type | What it supports in the paper | Confidence note |
|---|---|---|---|---|
| S1 | Beyond the Protocol | Research paper | Broad MCP attack-surface framing; lifecycle attack points; trust-boundary discussion. | Medium — current project intake is title/abstract/introduction level only. |
| S2 | Breaking the Protocol | Research paper | Spec-level weakness framing, prompt-injection amplification concerns, multi-server trust propagation. | Medium — useful for direction; verify any exact metrics or protocol-fix claims before relying on them. |
| S3 | Enterprise-Grade Security for MCP | Framework paper | Enterprise control framing: zero trust, defense in depth, governance, mitigation structure. | Medium — suitable for control framing; confirm specifics before strong claims. |
| S4 | MCP Safety Audit | Audit/exploit paper | Case for pre-deployment auditing, exploit demonstrations, and scanner-style validation. | Medium — supports broad exploitability and audit need at a high level. |
| S5 | MCPGuard | Tooling paper | Automated server-vulnerability detection, scanning, and CI/admission-control discussion. | Medium — good for automation angle; validate coverage claims from full text. |
| S6 | MCPSecBench | Benchmark paper | Evaluation design, benchmark framing, attack categories, and test-scenario selection. | Medium — promising benchmark source, but still only intake-depth reviewed. |
| S7 | Securing MCP: Risks, Controls, and Governance | Governance/control paper | Governance language, provenance, sandboxing, DLP, private registries, auditable controls. | Medium — duplicate PDF copies collapsed here; current use should stay high level. |
| S9 | Systematic Analysis of MCP Security | Research paper | Attack-taxonomy breadth and test-matrix ideas beyond malicious-server-only cases. | Medium — use for taxonomy framing; verify counts and method classes before specificity. |
| S10 | SoK: Security and Safety in the MCP Ecosystem | SoK / taxonomy paper | Related-work umbrella, security-vs-safety distinctions, and defense-family organization. | Medium — likely strong organizing source, but not yet close-read. |
| S11 | Trivial Trojans | PoC / attack paper | Concrete cross-tool exfiltration example and low-barrier adversary narrative. | Medium-Low — strong example value, but verify details before leaning on it heavily. |
| S12 | When MCP Servers Attack | Taxonomy/feasibility paper | Malicious-server taxonomy, server-vetting risks, and limits of current scanners. | Medium — supports procurement/vetting arguments; verify exact taxonomy claims before precision. |
| SPEC-2025 | MCP Specification (2025-11-25) | Specification | Protocol facts, feature descriptions, and normative security-relevant behavior for auth, transports, roots, elicitation, sampling, tools, resources, and prompts. | High for protocol facts — not evidence of real-world efficacy or adoption outcomes. |
| README | Project README | Project source | Project objective, scope, key questions, and current artifact map for manuscript positioning. | High for repo-local scope only — not an external research citation. |
| BRIEF | Project brief | Internal brief | Problem statement, intended contribution, in-scope/out-of-scope boundaries, and first-wave claims. | High for internal framing only — use to keep scope disciplined, not as external evidence. |
| VALPLAN | Validation and POC plan | Internal design/validation memo | Evidence standard, claim-to-artifact workflow, experiment tracks, metrics, and formal-core plan. | High for internal methods planning only — not support for empirical conclusions until experiments exist. |
