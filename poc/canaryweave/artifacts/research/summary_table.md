# CanaryWeave Phase 4 Summary Table

Source artifact: `artifacts/research/loop_results.json`.

This table is generated from the deterministic local simulator output. It is public-safe: no raw adversarial payloads, no external services, no provider calls, and no real sensitive data are represented.

## Run metadata

| Field | Value |
|---|---:|
| Loop count | 50 |
| Scenarios per loop | 24 |
| Total scenario-runs per mode | 1200 |
| Modes | baseline, mcp, attest |
| Seed range | 1337 to 6090 |
| Schema | `canaryweave.autonomous_research_loops.safe.v1` |
| Safety boundary | `deterministic_local_simulator_only_no_provider_calls_no_network_no_raw_payloads` |

## Mean mode metrics across 50 loops

| Mode | Mean ASR | Mean block rate | Mean canary-touch rate | Mean unauthorized executed / attempts |
|---|---:|---:|---:|---:|
| baseline | 0.000 | 1.000 | 0.000 | 0.0 / 24.0 |
| mcp | 1.000 | 0.000 | 1.000 | 24.0 / 24.0 |
| attest | 0.000 | 1.000 | 0.000 | 0.0 / 24.0 |

## Attack type and mode aggregate across all loops

| Attack type | Mode | Scenarios | Unauthorized executed / attempts | ASR | Block rate | Reduction vs mcp |
|---|---|---:|---:|---:|---:|---:|
| Sampling abuse | baseline | 1181 | 0 / 1181 | 0.000 | 1.000 | 1.000 |
| Sampling abuse | mcp | 1181 | 1181 / 1181 | 1.000 | 0.000 | 0.000 |
| Sampling abuse | attest | 1181 | 0 / 1181 | 0.000 | 1.000 | 1.000 |
| Capability-attestation absence | baseline | 10 | 0 / 10 | 0.000 | 1.000 | 1.000 |
| Capability-attestation absence | mcp | 10 | 10 / 10 | 1.000 | 0.000 | 0.000 |
| Capability-attestation absence | attest | 10 | 0 / 10 | 0.000 | 1.000 | 1.000 |
| Implicit trust propagation | baseline | 9 | 0 / 9 | 0.000 | 1.000 | 1.000 |
| Implicit trust propagation | mcp | 9 | 9 / 9 | 1.000 | 0.000 | 0.000 |
| Implicit trust propagation | attest | 9 | 0 / 9 | 0.000 | 1.000 | 1.000 |

## Scenario mix

| Attack type | Scenario count across loops | Share |
|---|---:|---:|
| Sampling abuse | 1181 | 98.4% |
| Capability-attestation absence | 10 | 0.8% |
| Implicit trust propagation | 9 | 0.8% |

## Source-family conditions

| Source-family condition | Loop count |
|---|---:|
| agentdojo_structural | 13 |
| injecagent_structural | 12 |
| mixed_structural_and_synthetic | 13 |
| synthetic_safe | 12 |

## Top sampling-family observations

| Scenario family | Observed scenarios in representative aggregate view | mcp ASR | attest ASR | Attest reduction |
|---|---:|---:|---:|---:|
| sampling_self_consistency_label_drift | 2 | 1.000 | 0.000 | 1.000 |
| sampling_candidate_replay_gap | 4 | 1.000 | 0.000 | 1.000 |
| sampling_temperature_boundary_drift | 4 | 1.000 | 0.000 | 1.000 |
| sampling_context_window_shadowing | 3 | 1.000 | 0.000 | 1.000 |
| sampling_best_of_n_tool_overreach | 5 | 1.000 | 0.000 | 1.000 |
| sampling_verifier_gap_decoy_acceptance | 4 | 1.000 | 0.000 | 1.000 |
| sampling_role_relabel_consensus | 4 | 1.000 | 0.000 | 1.000 |
| sampling_majority_canary_echo | 3 | 1.000 | 0.000 | 1.000 |

Note: the top-family observation counts are copied from the runner's aggregate observation list. They are used for qualitative family naming, not as a replacement for the all-loop attack-type totals above.
