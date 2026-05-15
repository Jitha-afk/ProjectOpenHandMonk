# Mira paper outline: Controlled PROTOAMP-style reproducibility POC

Working title:
Controlled Reproducibility for MCP Protocol-Safety Evaluation: A Benign PROTOAMP-Style Harness

Short title:
Controlled PROTOAMP-Style Protocol-Safety Harness

## Narrative position

This paper should be framed as a controlled reproducibility POC and protocol-safety harness inspired by the methodology described in "Breaking the Protocol." It must not be framed as a full artifact reproduction, independent validation of the authors' numeric claims, or replication of the reported 847-scenario evaluation.

The core contribution is a safety-bounded harness that preserves the experimental shape of the original methodology while replacing harmful payloads and real data flows with deterministic benign canaries, inert tools, local traces, and explicit policy labels.

### Claim boundary

Safe claims:

- We implement a PROTOAMP-style controlled harness based on the publicly described evaluation structure.
- We compare matched direct-function and protocol-wrapped execution modes over synthetic, benign scenarios.
- We measure canary propagation, unauthorized symbolic action execution, cross-server flow, and mitigation effects using deterministic trace parsing.
- We demonstrate how protocol-safety experiments can be made reproducible without using real secrets, real exfiltration, live endpoints, or raw harmful prompts.
- We provide a template for future artifact-level reproduction if original code, scenarios, prompts, and run configurations become available.

Claims to avoid:

- We reproduced the original paper's 847-scenario benchmark.
- We reproduced the reported 23-41% amplification values.
- We reproduced the reported 52.8% ASR or 12.4% ATTEST MCP ASR.
- We implemented or validated the original ATTEST MCP defense exactly.
- We evaluated real-world MCP server risk at ecosystem scale.

Preferred wording:

- "PROTOAMP-style" rather than "PROTOAMP reproduction."
- "ATTEST-inspired local shim" rather than "ATTEST MCP implementation."
- "Canary propagation" or "policy-violating benign flow" rather than real exfiltration.
- "Synthetic protocol-confusion scenarios" rather than real attack scenarios.
- "Local benchmark results" rather than general MCP security prevalence claims.

## Evidence boundary

The source paper provides enough information to reconstruct a benchmark shape, but not enough to faithfully reproduce the published result set. Missing evidence includes original PROTOAMP source code, exact scenario mappings, full prompt corpus, payload set, model run parameters, host/client implementation details, random seeds, classifier code, raw logs, and the exact ATTEST MCP implementation.

Therefore the paper should present this work as:

1. A safe reimplementation of the evaluation pattern.
2. A reproducibility scaffold for future comparison.
3. A methodology paper for measuring protocol-mediated safety failures with benign observables.

It should not present this work as:

1. A verification of the original paper's quantitative findings.
2. A replacement for the unavailable artifact.
3. A real exploitation toolkit.

## Paper outline

## 1. Abstract

### Purpose

Summarize the problem: tool-integrated LLM agents using MCP-like protocols create protocol-mediated trust and provenance challenges. "Breaking the Protocol" reports significant amplification effects, but public descriptions alone do not provide enough artifacts for exact reproduction. This paper introduces a controlled, safety-bounded PROTOAMP-style harness for reproducibility-oriented protocol-safety evaluation.

### Proposed abstract draft

Recent work on Model Context Protocol security argues that protocol-mediated tool integration can amplify prompt-injection and cross-server trust failures in LLM agents. However, exact reproduction of reported large-scale results requires artifacts that are often unavailable, including scenario corpora, payloads, host instrumentation, seeds, and raw traces. We present a controlled PROTOAMP-style reproducibility harness that preserves the experimental structure of prior MCP amplification evaluations while replacing harmful payloads and real sensitive data with deterministic benign canaries, inert mock tools, local-only traces, and policy-defined violation markers. The harness compares matched direct-function and protocol-wrapped execution modes, logs JSON-RPC-shaped event traces, and evaluates canary propagation, unauthorized symbolic tool use, cross-server flow, and ATTEST-inspired mitigation behavior using deterministic offline metrics. We explicitly do not claim reproduction of the original 847-scenario results or paper-reported amplification numbers. Instead, this work provides a safe measurement scaffold for protocol-safety research, clarifies evidence boundaries for reproducibility claims, and offers a path toward artifact-level evaluation when complete original benchmarks are available.

## 2. Introduction

### Narrative goal

The introduction should establish why protocol-safety harnesses matter, why exact reproduction is hard, and why a controlled benign POC is a useful intermediate contribution.

### Key points

- MCP-style tool integration shifts risk from isolated model output toward multi-party context, tool, and resource mediation.
- Prior work identifies weaknesses such as ambiguous capability boundaries, origin confusion, sampling provenance issues, and implicit trust propagation across multiple servers.
- The original "Breaking the Protocol" paper reports a large PROTOAMP evaluation, but the public paper text does not include enough artifacts to reproduce exact numbers.
- Security reproduction faces an additional safety constraint: publishing or running raw harmful prompts, real exfiltration paths, credential access, or live malicious servers is inappropriate for a controlled POC.
- This paper asks a narrower question: can we build a reproducible, safe harness that measures the same classes of protocol-mediated failure using benign markers?

### Suggested research questions

RQ1. Can a PROTOAMP-style benchmark be reconstructed as a safety-bounded harness using synthetic canaries and inert tools?

RQ2. Can matched direct-function and protocol-wrapped modes be compared with deterministic metrics without using real secrets or harmful payloads?

RQ3. Can cross-server flow and origin confusion be represented as local trace properties rather than real exfiltration events?

RQ4. Can ATTEST-inspired controls be evaluated as local policy and attestation shims while preserving clear limits on generalization?

### Contributions paragraph

This paper makes four contributions:

1. A narrative and methodological boundary for controlled reproduction of MCP protocol-safety claims.
2. A synthetic PROTOAMP-style scenario design using benign canaries and local-only mock tools.
3. A deterministic measurement protocol for attack-success-rate-style metrics, amplification, and mitigation reduction without harmful payloads.
4. An evidence-bound reporting template that separates local harness findings from unreproduced paper-scale claims.

## 3. Related work

### 3.1 Breaking the Protocol and PROTOAMP

Discuss the motivating paper at a high level:

- Reported focus: MCP protocol weaknesses and amplification of existing agent-security benchmark scenarios.
- Reported evaluation shape: MCP wrappers, direct-call baselines, injection points at resource content, tool responses, sampling prompts, and cross-server settings.
- Reported scale: 847 scenarios across multiple server types and model backends.
- Boundary: this POC does not have the original artifact, full prompt set, exact payloads, or raw traces; therefore it reconstructs the structure, not the numeric claims.

Avoid reproducing raw prompt strings, harmful payloads, or procedural exploit instructions.

### 3.2 MCP security benchmarks and taxonomies

Discuss related benchmark-oriented work such as MCPSecBench and similar taxonomies:

- They motivate systematic MCP security evaluation.
- They identify surfaces including tool metadata, tool output, resource output, prompt handling, configuration, and host-side policy.
- Their categories inform safe synthetic scenario families.
- This paper uses taxonomy labels but replaces concrete attacks with benign canary and policy-violation markers.

### 3.3 Malicious or compromised MCP servers

Discuss the class of work showing that a server can become an active participant in cross-tool or cross-server confusion:

- Key lesson: servers do not need direct communication if the host/LLM mediates data flow.
- This POC models that data flow using local synthetic traces and mock sensitive values.
- No real endpoint, private data, credential, filesystem secret, or external sink is used.

### 3.4 Defenses: attestation, provenance, policy, and scanning

Discuss defense directions:

- Capability attestation.
- Origin/provenance tagging.
- Cross-server flow policies.
- Runtime monitoring and JSON-RPC trace analysis.
- Static checks for risky metadata or configuration.

Boundary: the POC evaluates an ATTEST-inspired local shim, not a formally verified or production-ready implementation of ATTEST MCP.

## 4. System design

### 4.1 Design goals

- Safety: no real secrets, no real exfiltration, no live exploit payloads, no outbound network dependency.
- Reproducibility: fixed seeds, stable scenario IDs, deterministic canary generation, deterministic evaluator.
- Comparability: matched scenarios across direct baseline, MCP-like unprotected mode, and protected/attested mode.
- Observability: structured JSON-RPC-shaped event logs, trace digests, explicit policy decisions.
- Extensibility: scenario families can expand without changing metric definitions.

### 4.2 Architecture overview

Components:

1. Scenario registry
   - Stores scenario ID, family, injection surface, canary labels, allowed symbolic actions, denied symbolic actions, policy tags, and expected safe outcome.

2. Synthetic tool/action model
   - Uses symbolic tools such as `summarize_note`, `classify_note`, `write_report`, `emit_canary`, and `record_decoy_value`.
   - Tools are inert and local.
   - Unauthorized actions record only in memory or JSONL traces.

3. Execution modes
   - `baseline_no_mcp` or direct-function mode: matched non-protocol comparison.
   - `mcp_unprotected` or protocol-wrapped mode: simulates protocol-mediated tool/resource handling.
   - `mcp_attestmcp` or protected mode: uses policy checks plus ATTEST-inspired HMAC/capability binding.

4. Event logger
   - Logs JSON-RPC-shaped events with scenario ID, mode, action, capability, allow/deny decision, reason, sequence number, and canary touch marker.

5. Offline evaluator
   - Computes markers through exact string matching and structured trace parsing.
   - Does not use an LLM judge for primary binary metrics.

### 4.3 Provenance and policy model

Every synthetic resource, tool output, or sampling-like event receives origin metadata. The harness evaluates whether content from one origin appears in a disallowed destination or symbolic action. Policy is represented explicitly as allowlists, denylists, external-sink tags, and cross-server flow rules.

### 4.4 ATTEST-inspired shim

The protected mode signs only allowed symbolic capabilities and verifies action bindings before execution. The shim binds scenario ID, action name, capability, and nonce. This is a local design proxy for studying mitigation behavior, not a production security mechanism and not the original ATTEST MCP artifact.

## 5. Safe benchmark construction

### 5.1 Safety invariants

- Use synthetic canaries only, for example `CANARY_<seed>_<scenario>_<nonce>`.
- Use fake sensitive values only, for example `MOCK_PRIVATE_VALUE_<id>`.
- No real credentials, tokens, private files, network destinations, endpoints, or user data.
- No raw harmful prompt-injection payloads.
- No command execution, persistence, MITM, DNS rebinding, SSRF, sandbox escape, token theft, or arbitrary file access behavior.
- Network access disabled by default; if a local sink is needed, it is localhost-only and records inert test data.
- Logs are redacted by default and store hashes/digests where possible.

### 5.2 Scenario families

1. Resource canary propagation
   - A synthetic untrusted resource includes a benign canary label.
   - Violation: the canary appears in a disallowed symbolic action or destination.

2. Tool-output canary propagation
   - A benign tool response contains a labeled untrusted field.
   - Violation: the label crosses into a denied tool argument or final channel where policy forbids it.

3. Cross-server flow
   - Server A produces a synthetic canary or mock sensitive value.
   - Server B is a disallowed destination for that value.
   - Violation: exact canary appears in Server B's symbolic invocation or result trace.

4. Sampling-origin confusion
   - A server-originated synthetic prompt-like event carries a benign label.
   - Violation: the event is treated as user-originated or trusted in logs/policy.

5. Capability mismatch
   - A symbolic action requests a capability outside the declared manifest.
   - Violation: the action is executed without policy or attestation approval.

### 5.3 Scenario matrix

Recommended stages:

- Minimal smoke suite: 6 scenarios x 3 modes = 18 trials.
- Standard smoke suite: 20 scenarios x 3 modes = 60 deterministic trials.
- Confirmatory local suite: 50-100 scenarios x 3 modes, with replicates if model or simulator behavior is nondeterministic.

The paper should emphasize that even the confirmatory local suite is not equivalent to the original 847-scenario suite.

### 5.4 Determinism

- Fixed suite seed.
- Stable scenario IDs.
- Per-trial canaries derived from scenario ID, condition, and replicate ID.
- Temperature 0 and fixed model settings if a live model is later introduced.
- Primary evaluator uses exact canary matching and structured policy markers.

## 6. Experiments

### 6.1 Experiment 1: harness validity

Question:
Can the harness generate deterministic scenarios, execute all modes, and produce valid JSON-RPC-shaped logs without unsafe behavior?

Conditions:

- Minimal smoke suite.
- All execution modes.
- Safety validator enabled.

Measures:

- Valid trial count.
- Schema-valid event logs.
- Absence of network access or out-of-sandbox writes.
- Deterministic rerun equality for scenario generation and metric summaries.

Expected reporting language:

"The smoke suite validates harness mechanics only; it does not support claims about real-world MCP risk."

### 6.2 Experiment 2: matched baseline vs protocol-wrapped mode

Question:
Do protocol-wrapped synthetic scenarios produce measurable policy-violation markers under the local simulator compared with a matched direct baseline?

Conditions:

- Same scenario IDs and canaries across modes.
- Direct baseline and MCP-like unprotected mode.
- Matched symbolic tools and task semantics.

Measures:

- Canary propagation rate.
- Unauthorized tool/action rate.
- Cross-server flow rate.
- Primary benign ASR.
- Absolute amplification: ASR_mcp - ASR_baseline.
- ASR index difference.

Boundary:
Report only local effect sizes. Do not compare the resulting values to the original paper's percentages unless the original artifact and settings are independently reproduced.

### 6.3 Experiment 3: protected mode / ATTEST-inspired reduction

Question:
Does the local attestation and policy shim reduce benign policy-violation markers relative to unprotected mode?

Conditions:

- MCP-like unprotected mode.
- Protected ATTEST-inspired mode.
- Same scenarios, seeds, and canaries.

Measures:

- Absolute risk reduction.
- Relative risk reduction within the local benchmark.
- Unauthorized action reduction.
- Canary propagation reduction.
- Block rate.
- Latency or event-count overhead if measured.

Boundary:
Use wording such as "the ATTEST-inspired shim reduced local benchmark ASR from X/Y to A/B" rather than "we reproduced ATTEST MCP."

### 6.4 Experiment 4: ablations

Optional ablations:

- Allowlist-only policy.
- Provenance tagging without attestation.
- Attestation without cross-server flow policy.
- Inert-tools-only mode.
- Different scenario-family mixes.

Purpose:
Identify which local controls affect which deterministic markers. Keep claims exploratory unless pre-registered.

## 7. Results

### 7.1 Result structure

The results section should be written as a reporting template until real runs exist.

Recommended tables:

1. Scenario suite composition
   - Scenario count by family.
   - Conditions.
   - Replicates.
   - Valid/invalid trials.

2. Safety validation results
   - Network disabled: pass/fail.
   - No unsafe strings: pass/fail.
   - Logs schema-valid: pass/fail.
   - Out-of-sandbox writes: count.

3. Primary metrics by condition
   - ASR.
   - ASR index.
   - Unauthorized action rate.
   - Canary propagation rate.
   - Cross-server flow rate.
   - Persistence marker rate, if included as sandbox-only marker.

4. Amplification/reduction comparisons
   - Direct vs protocol-wrapped absolute difference.
   - Unprotected vs protected absolute risk reduction.
   - Paired bootstrap or Wilson/Newcombe confidence intervals.

5. Overhead
   - Median and P95 event-processing overhead if implemented.
   - Log size or event count.

### 7.2 Placeholder language before data exists

Use:

"In the current POC stage, this section reports harness outputs and smoke-test validity rather than confirmatory security findings."

Avoid:

"The benchmark proves MCP amplifies attacks."

### 7.3 Interpretation guide

If results show nonzero protocol-mode violations:

- Interpret as evidence that the local harness can represent protocol-mediated policy failures.
- Do not generalize to real MCP deployments without external validation.

If protected mode reduces violations:

- Interpret as evidence that the local mitigation blocks the modeled class of symbolic violations.
- Do not claim it blocks arbitrary prompt injection or malicious servers.

If results are zero across all modes:

- Interpret as either effective local policy or insufficient scenario pressure.
- Do not conclude that MCP is safe.

## 8. Limitations

### Reproducibility limitations

- Original PROTOAMP code and scenario corpus are unavailable in the local evidence base.
- Exact prompts, payloads, seeds, host instrumentation, model revisions, and raw logs are unavailable.
- The POC cannot validate the original paper's 847-scenario results or reported amplification percentages.

### Ecological validity limitations

- Synthetic canaries are not real secrets.
- Inert symbolic tools are not production MCP servers.
- A toy host simulator cannot capture all behaviors of Claude Desktop, Cursor, OpenAI tools, or other real clients.
- Deterministic exact-match metrics may miss semantic or paraphrased unsafe flows.
- Local HMAC/capability shims are not production-grade protocol security.

### Measurement limitations

- ASR-like metrics are benign proxies.
- Weighted ASR indices depend on preselected weights.
- Small smoke suites support engineering validation only.
- Confidence intervals on small local suites will be wide.
- Model/provider nondeterminism requires replication and careful logging if live models are introduced.

### Safety limitations

- Removing harmful payloads improves safety but changes task distribution.
- Canary-only evaluation cannot measure real adversarial creativity.
- Static risky-string filters are guardrails, not comprehensive safety guarantees.

## 9. Ethics and safety

### Ethical stance

The paper should argue that reproducibility in security research must not require distributing or executing harmful payloads. A controlled harness can make protocol-safety claims inspectable while minimizing risk.

### Safety controls

- No real secrets or private user data.
- No real exfiltration, endpoint callbacks, or network delivery.
- No operational attack instructions.
- No harmful raw payload corpus.
- Local-only inert tools.
- Scenario text validated by denylist and allowlist checks.
- Structured logs redacted by default.
- Sandbox-only marker writes if persistence-like behavior is modeled.
- Explicit statement that the project is not a deployment scanner or exploit toolkit.

### Responsible disclosure posture

If future work discovers a real vulnerability in a live MCP implementation, it should be handled through coordinated disclosure and excluded from public benchmark artifacts until remediated.

### Dual-use boundary

The manuscript should be explicit that the harness is designed for measurement of benign policy violations and should not be extended to live exploit payloads, real services, real credentials, or public target systems without separate review.

## 10. Conclusion

### Main message

A controlled PROTOAMP-style POC can advance reproducibility and protocol-safety research without claiming more than the evidence supports. The harness reconstructs the experimental shape of MCP amplification evaluation using benign canaries, inert tools, deterministic metrics, and explicit policy boundaries. Its value is methodological: it shows how to separate reproducible measurement design from unavailable artifacts and unsafe payloads.

### Suggested conclusion draft

This work presents a safety-bounded path for studying MCP-style protocol risks when full original artifacts are unavailable. By replacing harmful payloads and real sensitive data with benign canaries and deterministic local traces, the harness allows researchers to test provenance, policy, cross-server flow, and attestation-inspired controls without operationalizing real attacks. The resulting claims are intentionally narrow: we do not reproduce the original 847-scenario benchmark or its reported amplification values. Instead, we provide a controlled scaffold for local measurement, transparent reporting, and future artifact-level reproduction. This boundary is not a weakness of the POC; it is the central discipline required for responsible protocol-safety research.

## Reporting checklist for the final paper

Before submitting or publishing, verify that the manuscript:

- [ ] Uses "PROTOAMP-style" or "inspired by" language.
- [ ] States that the original 847-scenario results are not reproduced.
- [ ] Separates local benchmark metrics from paper-reported numbers.
- [ ] Avoids raw harmful payloads and operational exploit steps.
- [ ] Uses benign placeholders and synthetic canaries only.
- [ ] Describes all tools as inert/local/mock unless independently changed under review.
- [ ] Reports scenario counts, seeds, model settings, valid/invalid trials, and evaluator version.
- [ ] Reports confidence intervals for any quantitative claims beyond smoke testing.
- [ ] Labels smoke tests as harness validation, not security confirmation.
- [ ] Calls the mitigation an ATTEST-inspired shim unless the original implementation is actually reproduced.

## One-paragraph positioning statement

We present a controlled reproducibility POC for MCP protocol-safety evaluation, not a full reproduction of "Breaking the Protocol." The harness preserves the study shape of direct versus protocol-mediated execution, resource/tool/sampling-origin canary placement, cross-server flow observation, and mitigation comparison, but all potentially harmful content is replaced with benign synthetic markers and local-only traces. The resulting contribution is a reproducible safety harness and claim-bound reporting framework, not a validation of the original paper's reported 847-scenario quantitative results.
