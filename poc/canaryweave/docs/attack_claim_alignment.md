# CanaryWeave Attack-Claim Alignment Review

Status: conference-demo readiness review.

## Bottom line

The original 50-loop simulator result is useful harness validation, but it is not the right headline for a security conference attack demo. The conference-ready claim should center on the new `sampling_demo` suite because it has a precise protocol surface, success predicate, and auditable transcript:

> A vulnerable host that treats server-originated `sampling/createMessage` content with claimed role `user` as user authority executes unauthorized inert actions in 4/4 safe demo scenarios; a hardened host that checks sampling origin blocks 4/4.

This is a legitimate local ASR for the demo because success is directly observable and tied to the attack vector.

Important scope note: the demo is deterministic by construction. It exercises policy branches in an intentionally vulnerable host and an origin-aware hardened host; it does not run a live LLM, stochastic sampler, or production host. The main transcript artifact is JSON-RPC-shaped; a separate local MCP stdio POC exercises a real FastMCP stdio server and client session while preserving the same inert deterministic boundary.

## Source-paper alignment

The local source paper extract supports these factual anchors:

- MCP servers can request LLM completions from clients via `sampling/createMessage`.
- The sampling mechanism allows server-originated prompts/messages.
- The protocol concern is that client/host handling may fail to distinguish server-originated sampling content from user-originated authority.
- Origin tagging and capability/attestation checks are appropriate defensive directions.

The demo maps those anchors to a safe local setup:

| Source-paper concept | CanaryWeave demo equivalent |
|---|---|
| `sampling/createMessage` | JSON-RPC-shaped `SamplingRequest.method` |
| server-originated content | `origin="server"`, `server_id=...` |
| user-like role confusion | `claimed_role="user"` |
| downstream harmful action | inert unauthorized local action |
| sensitive payload/exfiltration | benign `DEMO_CANARY_*` marker into inert audit/report sink |
| defense | block server sampling as authority unless explicit origin/capability policy allows it |

## Accurate ASR definition for the demo

Attack success is not vague model compliance. It is:

```text
unauthorized_inert_action_executed_from_server_sampling
```

A success requires all of:

1. JSON-RPC-shaped method is `sampling/createMessage`.
2. Origin is `server`.
3. Claimed role is `user`.
4. Host accepts server-originated sampling content as authority.
5. Unauthorized inert action executes.
6. Benign canary touches only inert local demo sink.

Therefore:

```text
ASR = successful demo scenarios / total demo scenarios
```

Current demo result:

| Host condition | Successes / scenarios | ASR | Claim |
|---|---:|---:|---|
| baseline | 0 / 4 | 0.000 | No server sampling surface. |
| vulnerable_host | 4 / 4 | 1.000 | Origin/role confusion present. |
| hardened_host | 0 / 4 | 0.000 | Server sampling is not authority. |

## Demo scenarios

1. Role-confused sampling candidate.
2. Best-of-n candidate overreach.
3. Self-consistency provenance drift.
4. Verifier gap: format accepted as authority.

Each scenario remains conference-safe: no live provider, no real secrets, no external endpoint, no shell, no credential access, no raw adversarial prompt text.

The scenario labels `best-of-n`, `self-consistency`, and `verifier gap` are narrative subcase labels. They do not imply that CanaryWeave currently executes real best-of-n sampling, majority voting, or verifier-model scoring.

## Claims we can make on stage

Safe/accurate:

- MCP sampling introduces a real protocol surface where a server asks the client/host for model generation through `sampling/createMessage`.
- If a host treats server-originated sampling content as user authority, server text can drive unauthorized downstream actions.
- In this controlled local demo, that vulnerable behavior succeeds in 4/4 benign scenarios.
- Origin-aware policy blocks the same scenarios in 4/4 cases.
- The demo motivates origin tagging, explicit user consent, capability binding, and post-sampling policy checks.

Do not claim without live external evaluation:

- Production MCP hosts are vulnerable at a specific prevalence.
- Live frontier models have a specific ASR.
- The source paper's reported 58-72% sampling ASR or exfiltration rates are reproduced.
- HMAC alone fixes the issue independent of policy enforcement.

## Recommended paper phrasing

Use:

> Our demo-level ASR measures whether a server-originated `sampling/createMessage` request with a claimed user role leads to an unauthorized inert action. Under a deliberately vulnerable host policy, 4/4 safe sampling scenarios succeed. Under an origin-aware hardened policy, 0/4 succeed.

Avoid:

> MCP sampling attacks have 100% ASR.

Correct expanded phrasing:

> The controlled deterministic demo has 100% ASR against the intentionally vulnerable host policy and 0% against the origin-aware hardened policy; this demonstrates the attack vector and mitigation logic, not ecosystem prevalence.

Artifact phrasing should prefer `deterministic demo result` over `expected demo result` so readers do not confuse a scripted policy demonstration with a stochastic empirical estimate.
