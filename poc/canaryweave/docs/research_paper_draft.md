# Controlled Reproducibility for MCP Protocol-Safety Evaluation: A Benign CanaryWeave Harness

## Abstract

Recent MCP security work argues that protocol-mediated tool integration can amplify prompt-injection, provenance confusion, and cross-server trust failures in LLM agents. The motivating source paper, "Breaking the Protocol: Security Analysis of the Model Context Protocol Specification and Prompt Injection Vulnerabilities in Tool-Integrated LLM Agents" [1], describes a protocol-amplification evaluation framework for comparing MCP-integrated agents with non-MCP baselines and proposes ATTEST MCP for capability attestation and message authentication. The local manuscript does not include the benchmark code, scenario corpus, exact payloads, seeds, host instrumentation, or raw logs needed for exact numerical reproduction. CanaryWeave therefore preserves the public experimental shape while replacing harmful payloads and sensitive data with deterministic benign canaries, inert symbolic actions, local JSON-RPC-shaped traces, and policy-defined violation markers. The harness compares matched `baseline`, `mcp`, and `attest` modes and reports a simulated unauthorized-action execution rate as an ASR-style proxy. The contribution is a safety-bounded measurement scaffold, not a reproduction of the source paper's 847-scenario result set.

## Claim Boundary

Supported claims:

- CanaryWeave validates local simulator mechanics, scenario taxonomy, trace generation, and ASR-style metric plumbing.
- The 50-loop result is a deterministic simulator invariant: the intentionally permissive `mcp` mode executes unauthorized symbolic actions, while `baseline` and local policy-plus-attestation modes block them.
- The committed artifacts use benign synthetic canaries and inert local symbolic actions only.

Unsupported claims:

- Reproduction of the source paper's 847-scenario benchmark or reported percentages.
- Measurement of real MCP hosts, real LLM behavior, deployed ATTEST MCP, or ecosystem risk rates.
- Evidence that the HMAC shim alone, independent of policy gating, mitigates real protocol attacks.

## 1. Introduction

MCP-style tool integration changes the security boundary for LLM applications. Instead of a single model producing text, hosts coordinate clients, servers, tools, resources, prompts, and sometimes sampling requests over JSON-RPC transports. This creates useful composability, but it also creates protocol-mediated trust questions: which server originated a message, which capability was actually authorized, and whether data from one server should influence another server's tool invocation.

"Breaking the Protocol: Security Analysis of the Model Context Protocol Specification and Prompt Injection Vulnerabilities in Tool-Integrated LLM Agents" [1] identifies three protocol-level concerns: absence of capability attestation, bidirectional sampling without origin authentication, and implicit trust propagation in multi-server settings. The paper also reports a protocol-amplification benchmark and ATTEST MCP defense results. Those claims are important, but exact reproduction requires artifacts not present in the local research corpus: source code, benchmark adapters, prompts, scenario mappings, raw logs, classifier code, seeds, and model/backend configuration.

This POC takes the conservative route. It does not recreate harmful payloads, real exfiltration paths, or production MCP exploit servers. Instead, it asks a narrower question: can the evaluation structure be reconstructed safely enough to test the measurement logic? A controlled harness can model protocol-confusion classes as benign canary propagation and unauthorized symbolic action execution, then compare direct-function, MCP-like unprotected, and local policy-plus-attestation modes under deterministic metrics.

Contributions:

1. A source-grounded boundary for what can and cannot be inferred from the public source text.
2. A safe CanaryWeave Python harness using synthetic scenarios, inert symbolic actions, and local JSON-RPC-shaped logs.
3. Deterministic ASR-style proxy metrics for benign canary propagation and unauthorized symbolic action execution.
4. A local policy-plus-HMAC shim inspired by ATTEST MCP.
5. A reporting template that separates local toy-harness validation from unreproduced paper-scale claims.

## 2. Related Work

### 2.1 Motivating Source Paper

The motivating paper claims that MCP architectural choices amplify attack success compared to equivalent non-MCP integrations. Its public methodology describes MCP server wrappers, direct-call baselines, three injection surfaces (resource content, tool response payloads, and sampling request prompts), JSON-RPC logging, and scenarios adapted from existing agent-security benchmarks plus novel protocol-specific cases.

The paper is sufficient to reconstruct a benchmark pattern. It is not sufficient to reproduce the reported numbers. Alan's source brief documents missing items: no local source repository, no payload corpus, no adaptation rules, no client instrumentation schema, no adversarial server specification, and no raw traces.

### 2.2 MCP Security Benchmarks and Taxonomies

Local related work such as MCPSecBench, MCPGuard, "Trivial Trojans," and "When MCP Servers Attack" supports the general risk model: MCP servers can affect host/model context through tool descriptions, tool outputs, resource content, prompts, configuration, and multi-server composition. These sources motivate systematic testing, but this POC borrows only categories and architectural lessons. It does not copy raw exploit payloads or run vulnerable external servers.

AgentDojo [2] and InjecAgent [3] are used only as structural inspirations for task/tool surfaces, untrusted content placement, user/injection pairing, and ASR-style evaluation shape. No raw upstream adversarial prompt text, expected harmful achievements, tool responses, or sensitive values are embedded in the committed harness.

### 2.3 Defenses

The defense themes across the corpus are capability attestation, provenance tagging, cross-server flow policy, runtime monitoring, and safer host UI/permission models. CanaryWeave implements only a local policy-plus-HMAC shim. It is not a full ATTEST MCP implementation, not a production protocol extension, and not formally verified.

## 3. System Design

The harness is a pure-Python toy benchmark under `src/canaryweave/`. It has no real MCP client/server integration, no network dependency, no subprocess execution, and no access to real secrets.

Core modules:

- `scenario.py`: immutable dataclasses for modes, action kinds, attack types, source families, typed metadata, symbolic actions, and scenarios.
- `registry.py`: safe ASR-style scenario-family registry. Sampling-abuse families are weighted as the default majority.
- `source_adapters.py`: structural-only AgentDojo/InjecAgent summarizers that emit counts, category labels, schema keys, and hashes without raw payload text.
- `generator.py`: deterministic synthetic scenario generator using explicit seeds and registry selection.
- `safety.py`: central safety validator and risky-token rejection.
- `policies.py`: symbolic allow/deny policy.
- `attest.py`: HMAC capability-attestation shim.
- `events.py`: JSON-RPC-shaped in-memory/JSONL event logger with action-kind fields for trace disambiguation.
- `simulator.py`: host simulator for `baseline`, `mcp`, and `attest` modes.
- `metrics.py`: ASR-style proxy, block-rate, canary-touch, amplification, reduction, and metadata group-by summaries.
- `cli.py`: local runner for smoke experiments.

Execution modes:

- `baseline`: direct-function baseline. Only policy-allowed semantic actions execute; protocol-specific extra actions are not exposed.
- `mcp`: intentionally permissive protocol-shaped mode. Server-proposed candidate actions execute, modeling a missing message-level capability/origin check in the toy harness.
- `attest`: protected local mode. Policy is checked first; only policy-allowed actions receive a valid HMAC attestation binding scenario ID, action name, capability, and nonce.

The expected qualitative pattern is deterministic by design: the unprotected MCP-like condition permits unauthorized symbolic actions, while baseline and attested modes block them. This validates mechanics, not deployment prevalence.

## 4. Safe Benchmark Construction

All scenarios are synthetic and benign. A scenario contains:

- stable scenario ID;
- suite seed;
- user goal;
- neutral context text;
- allowed symbolic capabilities;
- one or more `CANARY_*` markers;
- ordered symbolic candidate actions;
- expected unauthorized action labels;
- metadata describing the scenario family.

Primary sampling-abuse families:

1. `sampling_majority_canary_echo`: majority-like candidate support is treated as authorization.
2. `sampling_temperature_boundary_drift`: a stochastic candidate outside policy is not rechecked.
3. `sampling_best_of_n_tool_overreach`: best-of-n selection rewards an overbroad symbolic tool.
4. `sampling_self_consistency_label_drift`: consensus normalizes a server-originated label as trusted.
5. `sampling_verifier_gap_decoy_acceptance`: a verifier scores format while missing authority provenance.
6. `sampling_role_relabel_consensus`: role relabeling obscures authority boundaries.
7. `sampling_context_window_shadowing`: candidate context shadows earlier policy context.
8. `sampling_candidate_replay_gap`: replayed candidate state bypasses a later policy check.

Secondary protocol families:

9. `attestation_absence_unbound_tool_call`: a server-proposed action lacks capability binding.
10. `implicit_trust_cross_context_label`: a context label crosses mock server boundaries without policy approval.

Safety invariants:

- no real credentials, tokens, private files, endpoint URLs, or external sinks;
- no raw harmful prompt-injection payloads;
- no command execution, persistence, MITM, DNS rebinding, SSRF, token theft, or arbitrary file access;
- no outbound network calls;
- only synthetic canaries and inert local logs;
- safety validation rejects URL-like, credential-like, command-like, network-related, and exfiltration-related strings.

## 5. Metrics

The primary unit is a scenario run under one mode. The deterministic evaluator computes metrics from structured `ScenarioResult` objects and JSON-RPC-shaped event logs.

Definitions:

- `unauthorized_attempts`: count of candidate actions labeled `UNAUTHORIZED`.
- `unauthorized_executed`: count of unauthorized actions that executed.
- `attack_success_rate`: internal field name for `unauthorized_executed / unauthorized_attempts`.
- Simulated unauthorized-action execution rate: public-facing name for the internal `attack_success_rate` field.
- `block_rate`: denied unauthorized attempts divided by unauthorized attempts.
- `canary_touch_rate`: fraction of scenarios in which an executed action touched a scenario canary.
- `amplification`: MCP proxy rate minus baseline proxy rate.
- `reduction`: protected-mode proxy-rate reduction relative to unprotected MCP proxy rate.
- `summarize_by_attack_type`: proxy metrics grouped by `sampling_abuse`, `capability_attestation_absence`, and `implicit_trust_propagation`.
- `summarize_by_source_family`: proxy metrics grouped by `synthetic_safe`, `agentdojo_structural`, and `injecagent_structural`.
- `summarize_by_scenario_family`: proxy metrics grouped by specific registry family.

These are ASR-style toy metrics. They are not direct estimates of real-world exploitation probability.

## 5.1 Structural Mapping from AgentDojo and InjecAgent

The updated scenario registry uses AgentDojo and InjecAgent as structural inspirations only. Alan's mapping records local source paths, counts, labels, and hashes in `research/alan_agentdojo_injecagent_mapping.md` when source checkouts are available. If the local source roots are absent, source adapters emit explicit missing-source synthetic summaries such as `synthetic:missing-agentdojo_structural` rather than pretending that upstream records were inspected.

The transformation preserves benchmark shape while dropping raw adversarial text:

- AgentDojo contributes task-suite surfaces, untrusted content locations, and user/injection pairing structure across workspace, Slack-like, banking-like, and travel-like suites.
- InjecAgent contributes ASR-style success definitions, direct-action versus two-stage data-flow shapes, user-tool and attacker-tool category labels, and base/enhanced setting structure.
- The POC replaces harmful or operational effects with inert symbolic actions such as `emit_canary`, `append_extra_marker`, `toggle_test_flag`, and `record_decoy_value`.
- MCP sampling is modeled as server-originated candidate content that must not be treated as user authority.

No upstream raw prompt payloads, expected harmful achievements, tool responses, or sensitive values are embedded in committed code, tests, docs, or generated dry-run logs.

## 6. Experiments

### 6.1 Harness Validity

Command:

```bash
uv run --with pytest pytest -q
```

Observed result:

```text
43 passed
```

Validated properties:

- deterministic scenario generation;
- safety validator accepts generated safe scenarios and rejects risky text;
- HMAC attestations verify and reject tampering/wrong secrets;
- simulator mode behavior matches expected policy;
- JSON-RPC-shaped logs parse correctly and include action kind for disambiguation;
- metric summaries and mode deltas compute deterministically;
- registry selection keeps sampling abuse as the majority scenario class while retaining the two secondary protocol classes;
- source adapters return structural metadata and hashes without exposing raw upstream payload text;
- the dry-run model scaffold emits redacted canary plans without provider calls;
- committed loop artifacts match schema and omit raw canaries.

### 6.2 Smoke Run

Commands:

```bash
PYTHONPATH=src python3 -m canaryweave.cli --seed 1337 --count 5 --mode baseline --log artifacts/runs/baseline.jsonl
PYTHONPATH=src python3 -m canaryweave.cli --seed 1337 --count 5 --mode mcp --log artifacts/runs/mcp.jsonl
PYTHONPATH=src python3 -m canaryweave.cli --seed 1337 --count 5 --mode attest --log artifacts/runs/attest.jsonl
```

Observed summaries:

| Mode | Simulated unauthorized-action execution rate | Block Rate | Canary Touch Rate | Unauthorized Executed / Attempts |
|---|---:|---:|---:|---:|
| baseline | 0.0 | 1.0 | 0.0 | 0 / 5 |
| mcp | 1.0 | 0.0 | 1.0 | 5 / 5 |
| attest | 0.0 | 1.0 | 0.0 | 0 / 5 |

Interpretation: in the toy harness, the intentionally permissive MCP-like mode executes protocol-proposed unauthorized symbolic actions, while the direct baseline and local policy-plus-attestation mode block them. This demonstrates the harness mechanics; it does not validate the original paper's reported 23-41% amplification or 52.8%/12.4% ASR numbers.

### 6.3 Safe Model-ASR Dry Run

The scaffold includes a disabled-by-default model registry for GPT-4o-family, Claude Sonnet-family, and other Hermes-configured model placeholders. The current implementation does not call provider APIs. Instead, it creates a reviewable dry-run plan:

```bash
PYTHONPATH=src python3 scripts/model_asr_dry_run.py --model-set smoke_core --seed 1337 --count 4 --output artifacts/runs/model_dry_run.json
```

Observed local summary from the canonical dry run:

```text
total_trials: 16
by_attack_type: sampling_abuse=16
by_mode: mcp=8, attest=8
by_model: openai_gpt4o_smoke=8, anthropic_claude_sonnet_4_6_smoke=8
```

The plan redacts canaries and records only neutral prompt template identifiers. Live Hermes/Klive or provider-backed runs are future work behind explicit model-ID verification, inert local mock tools, and deterministic trace scoring.

### 6.4 Safe Sampling Attack Demo

For conference demonstration, CanaryWeave includes a focused `sampling/createMessage` demo suite with a stricter attack-success predicate than the broad simulator loops. A scenario succeeds only if a server-originated sampling request with `origin="server"` and `claimed_role="user"` causes an unauthorized inert action to execute and carry a benign `DEMO_CANARY_*` marker into an inert local sink.

Command:

```bash
PYTHONPATH=src python3 scripts/sampling_demo.py --output artifacts/research/sampling_demo.json
```

Expected deterministic demo result:

| Host condition | Successes / scenarios | Demo ASR |
|---|---:|---:|
| baseline | 0 / 4 | 0.000 |
| vulnerable host | 4 / 4 | 1.000 |
| hardened host | 0 / 4 | 0.000 |

This supports the stage claim: a host that treats server-originated `sampling/createMessage` content as user authority is vulnerable in the controlled demo, while an origin-aware policy blocks the same cases. It does not support a prevalence claim about production MCP hosts or live LLMs.

### 6.5 Fifty-Loop Local Validation

The 50-loop artifact is generated with:

```bash
PYTHONPATH=src python3 scripts/autonomous_research_loops.py --loops 50 --output artifacts/research/loop_results.json
```

Across 50 deterministic loops, sampling abuse accounts for 1,181 of 1,200 scenario instances. For sampling-abuse scenarios, the intentionally permissive `mcp` simulator mode produced a simulated unauthorized-action execution rate of 1.000, while `baseline` and `attest` produced 0.000. This is a deterministic simulator invariant, not an empirical security measurement.

No inferential confidence intervals are reported for this local result because outcomes are deterministic by construction rather than stochastic estimates.

## 7. Limitations

1. The harness is a simulator, not a real MCP host/client/server stack.
2. No live LLM is used in the current implementation; the model scaffold is dry-run planning only.
3. Scenario outcomes are deterministic by construction and intentionally simplified.
4. The unprotected MCP mode is deliberately permissive to test metric plumbing; it should not be interpreted as a measured property of a specific MCP host.
5. The ATTEST-inspired shim combines local policy enforcement with HMAC capability binding. The current result does not isolate the HMAC contribution from policy gating.
6. The original source artifact and scenario corpus are unavailable in the local paper/corpus, so paper-scale numerical reproduction is out of scope.
7. Safety validation is a guardrail for this repository, not a comprehensive content moderation or exploit-detection system.
8. Capability-attestation absence and implicit trust propagation are secondary smoke-coverage classes in the current artifact; they are not balanced comparison sets.

## 8. Ethics and Safety

This POC avoids distributing or executing harmful payloads. It uses synthetic canaries, inert symbolic actions, and local logs. It does not access real user data, environment variables, private files, credentials, network services, or external endpoints. The paper draft and docs intentionally use high-level descriptions and benign placeholders rather than operational exploit instructions.

The goal is defensive measurement scaffolding: make protocol-safety measurement inspectable without normalizing unsafe benchmark artifacts in public docs.

## 9. Future Work

- Add a real MCP stdio wrapper around the same inert tools while preserving no-network/no-secret constraints.
- Add provenance tags and explicit cross-server flow policies to model multi-server composition more richly.
- Add ablations for policy-only, provenance-tag-only, HMAC-only, and policy-plus-HMAC modes.
- Add confidence intervals and paired comparison output only for stochastic/live-model suites where repeated trials are meaningful.
- Add optional live-model adapters only after model availability verification, provider budget controls, safe prompts, no-network sinks, and strict logging redaction.
- Compare against original CanaryWeave only if the authors release code, scenarios, seeds, and raw logs.

## 10. Conclusion

From the source text alone, we can reconstruct the shape of a CanaryWeave evaluation but not the original benchmark artifact or its reported numbers. The implemented POC provides a safe, deterministic scaffold for studying MCP protocol-safety measurement with benign canaries and symbolic actions. It demonstrates how to separate local mechanics from unsupported claims, which is essential for responsible research on tool-integrated LLM security.

## Appendix A. CanaryWeave 50-Loop Local Finding

This appendix converts `artifacts/research/loop_results.json` into a paper-style local finding. The artifact uses deterministic simulator outputs, not live-model or deployed-host measurements.

### A.1 Finding

Across 50 deterministic CanaryWeave loops, sampling-abuse scenarios show a simulated unauthorized-action execution rate of 1.000 in the intentionally permissive `mcp` simulator mode, while the matched `baseline` and local policy-plus-attestation `attest` modes each produced 0.000. The measured simulator delta of `mcp` over `baseline` is 1.000, and the measured local attest reduction relative to `mcp` is 1.000.

The finding is deliberately scoped: it is evidence about a deterministic local simulator with synthetic canaries and inert symbolic actions. It is not a real-world exploitation result, not a production-host measurement, and not a live-model evaluation.

### A.2 Loop metadata

| Field | Value |
|---|---:|
| Loop count | 50 |
| Scenarios per loop | 24 |
| Total scenario-runs per mode | 1200 |
| Seed range | 1337 to 6090 |
| Safety boundary | `deterministic_local_simulator_only_no_provider_calls_no_network_no_raw_payloads` |

### A.3 Mean mode results

| Mode | Simulated unauthorized-action execution rate | Mean block rate | Mean canary-touch rate |
|---|---:|---:|---:|
| baseline | 0.000 | 1.000 | 0.000 |
| mcp | 1.000 | 0.000 | 1.000 |
| attest | 0.000 | 1.000 | 0.000 |

### A.4 Attack-type aggregate

| Attack type | Scenario count across loops | Baseline proxy rate | mcp proxy rate | Attest proxy rate | Attest reduction vs mcp |
|---|---:|---:|---:|---:|---:|
| Sampling abuse | 1181 | 0.000 | 1.000 | 0.000 | 1.000 |
| Capability-attestation absence | 10 | 0.000 | 1.000 | 0.000 | 1.000 |
| Implicit trust propagation | 9 | 0.000 | 1.000 | 0.000 | 1.000 |

Sampling abuse is the primary focus of the loop output, accounting for 1,181 of 1,200 scenario instances. Capability-attestation absence and implicit trust propagation remain as smaller smoke-coverage classes so the draft can discuss how the same policy/attestation mechanics behave outside the main sampling-abuse emphasis.

### A.5 Attack-type and mode detail

The table below reports proxy rate and local reduction by attack type and simulator mode. The baseline row is a control, not a mitigation; reduction is therefore shown only for `attest` relative to the unprotected `mcp` reference.

| Attack type | Mode | Scenarios | Unauthorized executed / attempts | Proxy rate | Block rate | Attest reduction vs mcp |
|---|---|---:|---:|---:|---:|---:|
| Sampling abuse | baseline | 1181 | 0 / 1181 | 0.000 | 1.000 | — |
| Sampling abuse | mcp | 1181 | 1181 / 1181 | 1.000 | 0.000 | 0.000 |
| Sampling abuse | attest | 1181 | 0 / 1181 | 0.000 | 1.000 | 1.000 |
| Capability-attestation absence | baseline | 10 | 0 / 10 | 0.000 | 1.000 | — |
| Capability-attestation absence | mcp | 10 | 10 / 10 | 1.000 | 0.000 | 0.000 |
| Capability-attestation absence | attest | 10 | 0 / 10 | 0.000 | 1.000 | 1.000 |
| Implicit trust propagation | baseline | 9 | 0 / 9 | 0.000 | 1.000 | — |
| Implicit trust propagation | mcp | 9 | 9 / 9 | 1.000 | 0.000 | 0.000 |
| Implicit trust propagation | attest | 9 | 0 / 9 | 0.000 | 1.000 | 1.000 |

### A.6 Limitations of the 50-loop finding

1. Outcomes are deterministic by simulator design, so the result validates harness behavior and metric calculations rather than estimating deployment prevalence.
2. Candidate actions are symbolic and inert; no real data, credentials, private files, external endpoints, or provider APIs are used.
3. The unprotected `mcp` mode is intentionally permissive to model missing local capability checks; it should not be generalized to every MCP implementation.
4. The `attest` mode evaluates local policy enforcement plus HMAC capability binding, not a deployed protocol extension or isolated cryptographic-control effect.
5. Public reporting remains high-level and omits raw adversarial payloads and operational misuse instructions.

## References

[1] "Breaking the Protocol: Security Analysis of the Model Context Protocol Specification and Prompt Injection Vulnerabilities in Tool-Integrated LLM Agents." Local paper PDF in `/home/sealjitha/toresearch/`; access date 2026-05-16. Exact public URL, authors, and venue should be filled from the authoritative paper record before external publication.

[2] ETH Zurich SPY Lab. `agentdojo` GitHub repository. https://github.com/ethz-spylab/agentdojo . Used for structural mapping only; no raw adversarial payload text copied. Access date 2026-05-16.

[3] UIUC Kang Lab. `InjecAgent` GitHub repository. https://github.com/uiuc-kang-lab/InjecAgent . Used for structural mapping only; no raw adversarial payload text copied. Access date 2026-05-16.

[4] Model Context Protocol documentation/specification. https://modelcontextprotocol.io/ . Used for high-level protocol concepts; access date 2026-05-16.
