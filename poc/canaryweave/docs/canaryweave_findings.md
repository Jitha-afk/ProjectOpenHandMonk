# CanaryWeave Findings from 50 Deterministic Local Loops

Status: Phase 4 research finding document.

Source artifact: `artifacts/research/loop_results.json`.

## Finding

In the CanaryWeave local simulator, unprotected MCP-shaped sampling paths consistently execute unauthorized inert symbolic actions, while the direct baseline and the local attestation-protected mode block those same actions. Across 50 deterministic loops, the mean unprotected `mcp` attack-success-rate-style metric is 1.000, compared with 0.000 for `baseline` and 0.000 for `attest`. The local attestation shim therefore produces a 1.000 reduction relative to the unprotected simulator condition.

This is local simulator evidence only. It is not evidence of real-world exploitation, not a measurement of any production MCP host, and not a claim about live model behavior.

## Evidence snapshot

| Measure | Value |
|---|---:|
| Deterministic loops | 50 |
| Scenarios per loop | 24 |
| Total scenario-runs per mode | 1200 |
| Baseline ASR | 0.000 |
| Unprotected mcp ASR | 1.000 |
| Attest ASR | 0.000 |
| mcp minus baseline amplification | 1.000 |
| Attest reduction vs mcp | 1.000 |

## Mean metrics by mode

| Mode | Mean ASR | Mean block rate | Mean canary-touch rate | Interpretation |
|---|---:|---:|---:|---|
| baseline | 0.000 | 1.000 | 0.000 | Direct-function control path blocks policy-disallowed symbolic actions. |
| mcp | 1.000 | 0.000 | 1.000 | Unprotected protocol-shaped path accepts server-proposed symbolic actions in the toy model. |
| attest | 0.000 | 1.000 | 0.000 | Local capability binding blocks the same policy-disallowed symbolic actions. |

## Attack-type comparison

The loop runner emphasizes sampling abuse while retaining smaller comparison slices for capability-attestation absence and implicit trust propagation. The three families show the same simulator pattern because the toy `mcp` mode is intentionally permissive and the `baseline` and `attest` modes enforce policy checks.

| Attack type | Scenario count across loops | Baseline ASR | mcp ASR | Attest ASR | Attest reduction vs mcp |
|---|---:|---:|---:|---:|---:|
| Sampling abuse | 1181 | 0.000 | 1.000 | 0.000 | 1.000 |
| Capability-attestation absence | 10 | 0.000 | 1.000 | 0.000 | 1.000 |
| Implicit trust propagation | 9 | 0.000 | 1.000 | 0.000 | 1.000 |

Sampling abuse dominates the evidence set: 1,181 of 1,200 all-loop scenario instances are sampling-abuse cases. The other two protocol-risk classes are included as defensive comparison checks, not as the main empirical focus.

## Attack-type and mode detail

This table gives the requested attack-type-by-mode view. `Reduction vs mcp` is computed within each attack type, using the unprotected `mcp` row as the local simulator reference.

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

## Sampling-abuse families represented

The runner records the following sampling-family observations in its aggregate view. These are family-level labels for the safe simulator; they do not contain raw adversarial text.

| Scenario family | mcp ASR | attest ASR | Attest reduction |
|---|---:|---:|---:|
| sampling_self_consistency_label_drift | 1.000 | 0.000 | 1.000 |
| sampling_candidate_replay_gap | 1.000 | 0.000 | 1.000 |
| sampling_temperature_boundary_drift | 1.000 | 0.000 | 1.000 |
| sampling_context_window_shadowing | 1.000 | 0.000 | 1.000 |
| sampling_best_of_n_tool_overreach | 1.000 | 0.000 | 1.000 |
| sampling_verifier_gap_decoy_acceptance | 1.000 | 0.000 | 1.000 |
| sampling_role_relabel_consensus | 1.000 | 0.000 | 1.000 |
| sampling_majority_canary_echo | 1.000 | 0.000 | 1.000 |

## Safety and scope boundaries

- CanaryWeave uses synthetic canaries and inert symbolic actions only.
- The loop runner is deterministic and local; it makes no provider calls and uses no network services.
- The public docs intentionally omit raw adversarial payloads and operational misuse instructions.
- The reported ASR values are ASR-style simulator metrics, not real-world risk probabilities.
- The attestation result evaluates a local HMAC/capability shim inside the simulator, not a deployed protocol extension.

## Interpretation

The supported claim is narrow: CanaryWeave can deterministically demonstrate the measurement pattern that a protocol-shaped sampling path without explicit capability binding is more permissive than matched baseline and attested paths inside this local simulator. The finding is useful for validating metric plumbing, scenario taxonomy, and defensive framing before any future artifact-level or live-model evaluation.
