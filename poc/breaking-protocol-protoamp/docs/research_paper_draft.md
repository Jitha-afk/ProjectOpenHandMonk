# Controlled Reproducibility for MCP Protocol-Safety Evaluation: A Benign PROTOAMP-Style Harness

## Abstract

Recent MCP security work argues that protocol-mediated tool integration can amplify prompt-injection, provenance confusion, and cross-server trust failures in LLM agents. The paper "Breaking the Protocol" describes PROTOAMP, an evaluation framework for comparing MCP-integrated agents with non-MCP baselines, and proposes ATTEST MCP for capability attestation and message authentication. However, the local manuscript does not include the PROTOAMP source code, scenario corpus, exact payloads, seeds, host instrumentation, or raw logs needed for exact numerical reproduction. We therefore build a controlled PROTOAMP-style harness that preserves the public experimental shape while replacing harmful payloads and real sensitive data with deterministic benign canaries, inert symbolic actions, local JSON-RPC-shaped traces, and policy-defined violation markers. The harness compares matched `baseline`, `mcp`, and `attest` modes over synthetic protocol-confusion scenarios, computes attack-success-rate-style metrics through deterministic trace parsing, and evaluates an ATTEST-inspired local HMAC/capability shim. This work is not a reproduction of the original 847-scenario results; it is a safe reproducibility scaffold and methodology for future artifact-level MCP protocol-safety evaluation.

## 1. Introduction

MCP-style tool integration changes the security boundary for LLM applications. Instead of a single model producing text, hosts coordinate clients, servers, tools, resources, prompts, and sometimes sampling requests over JSON-RPC transports. This creates useful composability, but it also creates protocol-mediated trust questions: which server originated a message, which capability was actually authorized, and whether data from one server should influence another server's tool invocation.

"Breaking the Protocol" identifies three protocol-level concerns: absence of capability attestation, bidirectional sampling without origin authentication, and implicit trust propagation in multi-server settings. The paper also reports a PROTOAMP benchmark and ATTEST MCP defense results. Those claims are important, but exact reproduction requires artifacts not present in the paper text available in the local research corpus: source code, benchmark adapters, prompts, scenario mappings, raw logs, classifier code, seeds, and model/backend configuration.

This POC takes the conservative route. We do not attempt to recreate harmful payloads, real exfiltration paths, or production MCP exploit servers. Instead, we ask a narrower reproducibility question: can the evaluation structure be reconstructed safely enough to test the measurement logic? The answer is yes. A controlled harness can model protocol-confusion classes as benign canary propagation and unauthorized symbolic action execution, then compare direct-function, MCP-like unprotected, and attested/protected modes under deterministic metrics.

Contributions:

1. A source-grounded boundary for what can and cannot be reproduced from the public paper text.
2. A safe PROTOAMP-style Python harness using synthetic scenarios, inert symbolic actions, and local JSON-RPC-shaped logs.
3. Deterministic ASR-style metrics for benign canary propagation and unauthorized action execution.
4. An ATTEST-inspired local shim that binds scenario, action, capability, and nonce with HMAC.
5. A reporting template that separates local toy-harness findings from unreproduced paper-scale claims.

## 2. Related Work

### 2.1 Breaking the Protocol

The motivating paper claims that MCP architectural choices amplify attack success compared to equivalent non-MCP integrations. Its public methodology describes MCP server wrappers, direct-call baselines, three injection surfaces (resource content, tool response payloads, and sampling request prompts), JSON-RPC logging, and scenarios adapted from existing agent-security benchmarks plus novel protocol-specific cases.

The paper is sufficient to reconstruct a benchmark pattern. It is not sufficient to reproduce the reported numbers. Alan's source brief documents the missing items: no local PROTOAMP repository, no payload corpus, no adaptation rules, no client instrumentation schema, no adversarial server specification, and no raw traces.

### 2.2 MCP Security Benchmarks and Taxonomies

Local related work such as MCPSecBench, MCPGuard, "Trivial Trojans," and "When MCP Servers Attack" supports the general risk model: MCP servers can affect host/model context through tool descriptions, tool outputs, resource content, prompts, configuration, and multi-server composition. These sources motivate systematic testing, but this POC borrows only categories and architectural lessons. It does not copy raw exploit payloads or run vulnerable external servers.

### 2.3 Defenses

The defense themes across the corpus are capability attestation, provenance tagging, cross-server flow policy, runtime monitoring, and safer host UI/permission models. The POC implements only a local ATTEST-inspired shim. It is not a full ATTEST MCP implementation, not a production protocol extension, and not formally verified.

## 3. System Design

The harness is a pure-Python toy benchmark under `src/protoamp/`. It has no real MCP client/server integration, no network dependency, no subprocess execution, and no access to real secrets.

Core modules:

- `scenario.py`: immutable dataclasses for modes, action kinds, attack types, source families, typed metadata, symbolic actions, and scenarios.
- `registry.py`: safe ASR scenario-family registry. Sampling-abuse families are weighted as the default majority.
- `source_adapters.py`: structural-only AgentDojo/InjecAgent summarizers that emit counts, category labels, schema keys, and hashes without raw payload text.
- `generator.py`: deterministic synthetic scenario generator using explicit seeds and registry selection.
- `safety.py`: central safety validator and risky-token rejection.
- `policies.py`: symbolic allow/deny policy.
- `attest.py`: HMAC capability-attestation shim.
- `events.py`: JSON-RPC-shaped in-memory/JSONL event logger.
- `simulator.py`: host simulator for `baseline`, `mcp`, and `attest` modes.
- `metrics.py`: ASR, block-rate, canary-touch, amplification, reduction, and metadata group-by summaries.
- `cli.py`: local runner for smoke experiments.

Execution modes:

- `baseline`: direct-function baseline. Only policy-allowed semantic actions execute; protocol-specific extra actions are not exposed.
- `mcp`: unprotected protocol-wrapped mode. Server-proposed candidate actions execute, modeling missing message-level capability/origin enforcement in the toy harness.
- `attest`: protected mode. Policy is checked first; only policy-allowed actions receive a valid HMAC attestation binding scenario ID, action name, capability, and nonce.

The intentionally simple simulator makes the expected qualitative pattern easy to verify: the unprotected MCP-like condition permits canary-touching unauthorized symbolic actions, while baseline and attested modes block them.

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

Current typed scenario families:

Primary sampling-abuse families:

1. `sampling_majority_canary_echo`: majority-like candidate support is treated as authorization.
2. `sampling_temperature_boundary_drift`: a stochastic candidate outside policy is not rechecked.
3. `sampling_best_of_n_tool_overreach`: best-of-n selection rewards an overbroad symbolic tool.
4. `sampling_self_consistency_label_drift`: consensus normalizes a server-originated label as trusted.
5. `sampling_verifier_gap_decoy_acceptance`: a verifier scores format while missing authority provenance.

Secondary protocol families:

6. `attestation_absence_unbound_tool_call`: a server-proposed action lacks capability binding.
7. `implicit_trust_cross_context_label`: a context label crosses mock server boundaries without policy approval.

The registry can also preserve legacy synthetic families for compatibility, but new generated suites use typed metadata and sampling-weighted selection.

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
- `attack_success_rate`: `unauthorized_executed / unauthorized_attempts`.
- `block_rate`: denied unauthorized attempts divided by unauthorized attempts.
- `canary_touch_rate`: fraction of scenarios in which an executed action touched a scenario canary.
- `amplification`: MCP ASR minus baseline ASR.
- `reduction`: protected-mode ASR reduction relative to unprotected MCP ASR.
- `summarize_by_attack_type`: ASR grouped by `sampling_abuse`, `capability_attestation_absence`, and `implicit_trust_propagation`.
- `summarize_by_source_family`: ASR grouped by `synthetic_safe`, `agentdojo_structural`, and `injecagent_structural`.
- `summarize_by_scenario_family`: ASR grouped by specific registry family.

These are ASR-style toy metrics. They are not direct estimates of real-world exploitation probability.

## 5.1 Structural Mapping from AgentDojo and InjecAgent

The updated scenario registry uses AgentDojo and InjecAgent as structural inspirations only. Alan's mapping records exact local source paths, counts, labels, and hashes in `research/alan_agentdojo_injecagent_mapping.md`. The transformation preserves benchmark shape while dropping raw adversarial text:

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
32 passed
```

Validated properties:

- deterministic scenario generation;
- safety validator accepts generated safe scenarios and rejects risky text;
- HMAC attestations verify and reject tampering/wrong secrets;
- simulator mode behavior matches expected policy;
- JSON-RPC-shaped logs parse correctly;
- metric summaries and mode deltas compute deterministically.
- registry selection keeps sampling abuse as the majority scenario class while retaining the two secondary protocol classes.
- source adapters return structural metadata and hashes without exposing raw upstream payload text.
- the dry-run model scaffold emits redacted canary plans without provider calls.

### 6.2 Smoke Run

Commands:

```bash
PYTHONPATH=src python3 -m protoamp.cli --seed 1337 --count 5 --mode baseline --log artifacts/runs/baseline.jsonl
PYTHONPATH=src python3 -m protoamp.cli --seed 1337 --count 5 --mode mcp --log artifacts/runs/mcp.jsonl
PYTHONPATH=src python3 -m protoamp.cli --seed 1337 --count 5 --mode attest --log artifacts/runs/attest.jsonl
```

Observed summaries:

| Mode | ASR | Block Rate | Canary Touch Rate | Unauthorized Executed / Attempts |
|---|---:|---:|---:|---:|
| baseline | 0.0 | 1.0 | 0.0 | 0 / 5 |
| mcp | 1.0 | 0.0 | 1.0 | 5 / 5 |
| attest | 0.0 | 1.0 | 0.0 | 0 / 5 |

Interpretation: in the toy harness, the MCP-like unprotected mode executes protocol-proposed unauthorized symbolic actions, while the direct baseline and attested mode block them. This demonstrates the harness mechanics; it does not validate the original paper's reported 23-41% amplification or 52.8%/12.4% ASR numbers.

### 6.3 Safe Model-ASR Dry Run

The scaffold includes a disabled-by-default model registry for GPT-4o-family, Claude Sonnet-family, and other Hermes-configured model placeholders. The current implementation does not call provider APIs. Instead, it creates a reviewable dry-run plan:

```bash
PYTHONPATH=src python3 scripts/model_asr_dry_run.py --seed 1337 --count 4 --output artifacts/runs/model_dry_run.json
```

Observed local summary from the dry run:

```text
total_trials: 24
by_attack_type: sampling_abuse=24
by_mode: mcp=12, attest=12
by_model: openai_gpt4o_smoke=8, anthropic_claude_sonnet_4_6_smoke=8, local_or_openrouter_frontier_placeholder=8
```

The plan redacts canaries and records only neutral prompt template identifiers. Live Hermes/Klive or provider-backed runs are future work behind explicit model-ID verification, inert local mock tools, and deterministic trace scoring.

## 7. Limitations

1. The harness is a simulator, not a real MCP host/client/server stack.
2. No live LLM is used in the current implementation; the model scaffold is dry-run planning only.
3. Scenario outcomes are deterministic by construction and intentionally simplified.
4. The unprotected MCP mode is deliberately permissive to test metric plumbing; it should not be interpreted as a measured property of a specific MCP host.
5. The ATTEST-inspired shim is local and symbolic, not a deployed protocol extension.
6. The original PROTOAMP artifact and scenario corpus are unavailable in the local paper/corpus, so paper-scale numerical reproduction is out of scope.
7. Safety validation is a guardrail for this repository, not a comprehensive content moderation or exploit-detection system.

## 8. Ethics and Safety

This POC avoids distributing or executing harmful payloads. It uses synthetic canaries, inert symbolic actions, and local logs. It does not access real user data, environment variables, private files, credentials, network services, or external endpoints. The paper draft and docs intentionally use high-level descriptions and benign placeholders rather than operational exploit instructions.

The goal is defensive reproducibility: make protocol-safety measurement inspectable without normalizing unsafe benchmark artifacts in public docs.

## 9. Future Work

- Add a real MCP stdio wrapper around the same inert tools while preserving no-network/no-secret constraints.
- Add provenance tags and explicit cross-server flow policies to model multi-server composition more richly.
- Add confidence intervals and paired comparison output for larger deterministic suites.
- Add optional live-model adapters only after model availability verification, provider budget controls, safe prompts, no-network sinks, and strict logging redaction.
- Compare against original PROTOAMP if the authors release code, scenarios, seeds, and raw logs.

## 10. Conclusion

From the paper text alone, we can reconstruct the shape of a PROTOAMP-style evaluation but not the original benchmark artifact or its reported numbers. The implemented POC provides a safe, deterministic scaffold for studying MCP protocol-safety measurement with benign canaries and symbolic actions. It demonstrates how to separate reproducible local mechanics from unsupported claims, which is essential for responsible research on tool-integrated LLM security.
