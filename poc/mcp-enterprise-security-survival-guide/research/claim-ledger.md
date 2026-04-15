# Claim Ledger — MCP Enterprise Security Survival Guide

## Evidence-status categories

Every claim the paper might make must carry one of the following labels so that drafters and reviewers know how much weight it can bear.

| Label | Meaning | Drafting rule |
|---|---|---|
| **CITED** | Directly supported by a primary source whose relevant section has been read or closely inspected. | May be stated with moderate confidence; cite the source explicitly. |
| **TITLE/ABSTRACT-ONLY** | Source exists and its title, abstract, or introduction supports the claim direction, but no close reading of the full argument or data has been performed yet. | State cautiously; note the inspection depth in the text. |
| **ANALOGICAL** | Inferred from adjacent security literature (API, plugin, zero-trust, LLM prompt injection) rather than MCP-specific evidence. | Frame as "consistent with established practice" rather than "demonstrated for MCP." |
| **SPEC-GROUNDED** | Claim is derived from reading the MCP specification (2025-11-25) directly; no independent experimental validation exists. | Cite the spec section; do not claim the mechanism has been tested in the field. |
| **HYPOTHESIS** | Plausible based on design reasoning or preliminary literature signals, but no direct evidence or experiment backs it yet. | Use hedged language ("we expect," "should," "may"); mark explicitly as requiring validation. |
| **LAB** | Supported by a reproducible experiment or prototype run inside this repository. | May be stated with confidence scoped to the lab conditions; describe the setup. |

At the time of writing, no claims carry the LAB label because no experiments have been run yet.

---

## Candidate claims

| ID | Claim text | Evidence status | Supporting sources | Notes / limits | Paper section |
|---|---|---|---|---|---|
| C-01 | MCP expands the enterprise attack surface beyond classic prompt injection to include server metadata, tool descriptions, resources, and cross-server composition. | TITLE/ABSTRACT-ONLY | S1 (Song et al., attack vectors across MCP lifecycle), S6 (MCPSecBench, 17 attack types across 4 surfaces), S9 (MCPLIB, 31 attack methods in 4 classes), S10 (SoK taxonomy of MCP primitives) | Multiple independent sources converge on this claim at the title/abstract level; no single full-text close reading completed. | §3 Threat model |
| C-02 | Malicious or poisoned tool descriptions are a first-class attack vector that can coerce LLMs into unintended tool invocations. | TITLE/ABSTRACT-ONLY | S1 (tool-description sanitization), S4 (coercion of industry-leading LLMs), S9 (tool poisoning attacks, TPA), S12 (malicious server taxonomy, PoC generation) | Repeatedly flagged across the corpus. Strength of experimental evidence not verified beyond abstracts. | §3 Threat model, §4 Risk scenarios |
| C-03 | Cross-server trust propagation allows a weakly trusted MCP server to influence actions on a strongly trusted server, enabling confused-deputy and privilege-escalation attacks. | TITLE/ABSTRACT-ONLY | S2 (trust propagation in multi-server configs), S10 (weaponized context in multi-agent environments), S11 (cross-tool exfiltration via trivial trojans) | S11 provides a concrete low-barrier PoC (title/abstract level). Full experimental details not close-read. | §4 Risk scenarios, §6 Defense techniques |
| C-04 | Existing MCP security scanning tools (McpSafetyScanner, MCPGuard, MCPSecBench) demonstrate that automated pre-deployment vulnerability detection is feasible but currently insufficient against evasive servers. | TITLE/ABSTRACT-ONLY | S4 (McpSafetyScanner), S5 (MCPGuard), S6 (MCPSecBench benchmark), S12 (tests current scanners, shows insufficiency) | S12 abstract explicitly claims current scanners are insufficient. Claims about scanner effectiveness rest on abstracts only. | §5 Control framework, §7 Evaluation plan |
| C-05 | The MCP 2025-11-25 specification introduces explicit security-relevant features — Origin validation, localhost binding for Streamable HTTP, OAuth 2.1-style authorization, roots as filesystem boundaries, elicitation with form/URL mode separation, and sampling with tool-use support — that are not yet fully analyzed in the academic literature. | SPEC-GROUNDED + TITLE/ABSTRACT-ONLY | MCP spec 2025-11-25 (authorization, transports, roots, sampling, elicitation sections); source-inventory-and-gap-analysis.md gap §A | Spec features confirmed by direct spec reading. Gap claim based on negative evidence: none of the 12 PDFs appear (from title/abstract) to center on these specific 2025-11-25 features. Absence of coverage is harder to prove than presence. | §2 Background, §3 Threat model |
| C-06 | A policy enforcement gateway placed between model intent and MCP tool execution can reduce unauthorized tool invocations without materially harming benign task completion. | HYPOTHESIS | validation-and-poc-plan.md Track 1; design reasoning from S3 (enterprise frameworks), S7 (inline policy enforcement) | No experiment exists. Quantitative thresholds (95% block, 90% benign pass) are provisional design targets from the validation plan, not measured results. | §6 Defense techniques, §7 Evaluation plan |
| C-07 | Provenance metadata and integrity envelopes attached to MCP tool responses can enable downstream trust decisions and reduce unsafe reliance on attacker-controlled output. | HYPOTHESIS | validation-and-poc-plan.md Track 2; S7 (provenance tracking), S10 (cryptographic provenance / ETDI) | S10 abstract mentions ETDI and cryptographic provenance but details not close-read. No prototype built yet. | §6 Defense techniques |
| C-08 | Per-user scoped authorization for remote MCP servers reduces blast radius of compromised or malicious tool use compared with shared static credentials. | ANALOGICAL + SPEC-GROUNDED | MCP spec 2025-11-25 (authorization section, OAuth 2.1 flows); S3 (zero-trust frameworks), S7 (per-user auth with scoped authorization); general OAuth/RBAC security literature | Well-established principle in API/cloud security. MCP-specific empirical evidence not yet available. | §5 Control framework |
| C-09 | Client-side enforcement of `roots` boundaries can prevent file reads outside approved `file://` roots even under indirect prompt injection from a malicious server. | HYPOTHESIS + SPEC-GROUNDED | MCP spec 2025-11-25 (roots section); source-inventory-and-gap-analysis.md gap §A.4 | The spec defines roots as boundary declarations. Whether current client implementations actually enforce them under adversarial conditions is untested. Source inventory flags this as an underexplored area. | §6 Defense techniques, §7 Evaluation plan |
| C-10 | Restricting sensitive data collection to URL-mode elicitation (with domain disclosure and user consent) lowers credential-harvesting risk relative to unrestricted form-mode handling. | HYPOTHESIS + SPEC-GROUNDED | MCP spec 2025-11-25 (elicitation section: secrets must not be collected via form mode); source-inventory-and-gap-analysis.md gap §A.3 | Spec mandates the restriction; no empirical study of evasion or compliance rates found in the PDF corpus. | §5 Control framework, §6 Defense techniques |
| C-11 | The MCP protocol's architectural design amplifies prompt-injection attack success rates compared with equivalent non-MCP integrations. | TITLE/ABSTRACT-ONLY | S2 (PROTOAMP framework: 23–41% amplification across 847 scenarios) | Single source with a specific quantitative claim. The 23–41% figure is from the S2 abstract. Replication and generalization unknown. Strong claim requiring close reading before the paper cites it as established. | §3 Threat model |
| C-12 | The ATTEST MCP protocol extension (capability attestation + message authentication) can reduce MCP attack success rates substantially (from ~53% to ~12% in one study) with low latency overhead. | TITLE/ABSTRACT-ONLY | S2 (ATTEST MCP: 52.8% → 12.4%, 8.3 ms median overhead) | Single source with specific numbers. Not independently replicated. Numbers from abstract only; methodology and threat model scope not close-read. | §6 Defense techniques |
| C-13 | Minimal, unsophisticated MCP servers (requiring only basic programming skills) can successfully perform cross-tool data exfiltration in current implementations. | TITLE/ABSTRACT-ONLY | S11 (Trivial Trojans: undergraduate-level Python, free web tools, weather server → banking exfiltration PoC) | Single source with a concrete PoC claim. Impressive if replicated, but details not close-read. | §4 Risk scenarios |
| C-14 | Enterprise MCP deployments require an audit schema covering auth events, server discovery, prompt/resource exposure, tool execution, sampling, elicitation, and policy decisions to reconstruct incidents end-to-end. | ANALOGICAL + SPEC-GROUNDED | MCP spec 2025-11-25 (multiple capability sections); S7 (auditable actions); source-inventory-and-gap-analysis.md gap §B.5; general enterprise logging practice (SOC 2, ISO 27001) | No MCP-specific audit standard exists. Claim is derived from combining spec surface area with established compliance requirements. | §5 Control framework, §8 Operational guidance |
| C-15 | A narrow formal specification (e.g., TLA+/Alloy) of the broker policy and trust-state machine is a realistic and valuable complement to empirical testing for the security-critical enforcement core. | HYPOTHESIS | validation-and-poc-plan.md (formal-methods section); S2 (formal security analysis framing); S10 (mentions runtime intent verification) | No formal spec has been written or model-checked for this project. Claim rests on design reasoning and the validation plan's stated approach. | §6 Defense techniques, §7 Evaluation plan |
| C-16 | Private registry allowlisting combined with signed server metadata improves resistance to malicious MCP server onboarding compared with unaudited public installation flows. | ANALOGICAL + TITLE/ABSTRACT-ONLY | S5 (zero-trust registry systems), S7 (private registries, gateway layers), S12 (lack of standardized review for MCP servers); general software supply-chain security practice | Well-established in software supply-chain security. MCP-specific signed-manifest mechanisms not yet standardized or empirically tested in MCP context. | §5 Control framework |
| C-17 | Response normalization and instruction/data separation in MCP tool outputs can reduce follow-on tool-output prompt injection. | HYPOTHESIS | validation-and-poc-plan.md Track 5; S10 (runtime intent verification) | Design-level proposal. No prototype or empirical measurement exists. Effectiveness against sophisticated injection unknown. | §6 Defense techniques |
| C-18 | Existing AI governance frameworks (NIST AI RMF, ISO/IEC 42001) do not yet cover MCP-specific threats in adequate detail for enterprise adoption. | TITLE/ABSTRACT-ONLY | S7 (explicitly states governance frameworks don't yet cover MCP threats) | Based on S7 abstract. The gap claim could become outdated as frameworks evolve. Time-sensitive. | §5 Control framework, §9 Limitations |

---

## 5 highest-confidence claims (citable now with appropriate hedging)

These claims have the strongest current evidence basis and can be stated in the paper draft with moderate confidence, provided the stated evidence limits are disclosed.

1. **C-01** — MCP expands the attack surface beyond prompt injection.
   Multiple independent sources (S1, S6, S9, S10) converge. Title/abstract-level only, but the convergence across 4+ independent teams is strong signal.

2. **C-02** — Malicious tool descriptions are a first-class attack vector.
   Corroborated across S1, S4, S9, S12. The mechanism (LLM follows tool-description instructions) is well-understood in adjacent prompt-injection literature.

3. **C-03** — Cross-server trust propagation enables confused-deputy attacks.
   Supported by S2, S10, S11. S11's low-barrier PoC claim (if verified) makes this especially concrete.

4. **C-05** — The 2025-11-25 spec introduces security-relevant features not yet fully analyzed in the literature.
   Spec sections confirmed by direct reading. Negative evidence (absence from PDF abstracts) is inherently weaker but currently holds.

5. **C-08** — Per-user scoped authorization reduces blast radius vs. shared credentials.
   Well-established in general API/cloud security, explicitly mentioned in S3 and S7, and aligned with the MCP spec's authorization model. Analogical strength is high.

---

## 5 claims that must remain hypotheses until experiments

These claims are plausible and important to the paper's argument, but cannot be stated as findings until the corresponding experiments or prototypes are completed.

1. **C-06** — Policy enforcement gateway reduces unauthorized tool invocations without breaking benign tasks.
   The quantitative targets (95% block, 90% benign pass) are design aspirations from the validation plan. No gateway prototype exists. Must remain hypothesis until Track 1 experiments run.

2. **C-09** — Client-side `roots` enforcement prevents out-of-scope file access under adversarial conditions.
   The spec declares roots as boundaries, but no stress test against indirect prompt injection or malicious server guidance has been conducted. Must remain hypothesis until tested.

3. **C-10** — URL-mode elicitation restriction lowers credential-harvesting success.
   The spec mandates the separation, but evasion rates, UX bypass paths, and real-world compliance are completely unmeasured. Must remain hypothesis until empirical study.

4. **C-15** — Narrow formal specification of the enforcement core is realistic and valuable.
   No formal spec has been written. The claim that it is "realistic" requires demonstrating a working spec and model-checking run. Must remain hypothesis until produced.

5. **C-17** — Response normalization reduces tool-output prompt injection.
   Pure design proposal with no prototype. Effectiveness against adversarial content, false-positive rates on benign output, and coverage of injection variants are all unknown. Must remain hypothesis until Track 5 experiments run.
