# First-Wave Fixture Plan

Goal: define the smallest first engineering wave of replayable evaluation fixtures for the broker-centered controls already prioritized in the project materials: policy gating, provenance handling, and cross-server trust control.

Working rules:
- Keep each packet independently buildable in one short implementation cycle.
- Ship each packet as a fixture spec plus golden expected outcomes, not code.
- Include at least one benign allow case inside each packet so false denials are visible early.
- Keep checks broker-observable: policy decision, trust label, approval state, and logged reason.

## Packet 0 — Common fixture contract
- Artifact type: fixture manifest template plus expected-outcome template.
- Intended assertion: every first-wave scenario can be described with the same minimum fields: actor, server trust tier, auth context, transport/origin context, roots context, elicitation mode, provenance state, requested action, expected broker outcome, and expected log note.
- Minimal success check: one reviewed template can represent at least one fixture from each packet below without adding new top-level fields.

## Packet 1 — Auth-bound policy fixtures
- Artifact type: paired replay fixtures for benign and abusive authorization states.
- Intended assertion: tool permission is decided from explicit auth context, not from model intent or server suggestion.
- Minimal success check: expected outcomes allow a correctly scoped per-user call, and deny or approval-gate variants with shared credentials, scope overreach, or user/server identity mismatch.

## Packet 2 — Streamable HTTP and Origin fixtures
- Artifact type: transport scenario manifests with request metadata and binding assumptions.
- Intended assertion: local Streamable HTTP access is only acceptable when binding and Origin conditions match the approved deployment shape.
- Minimal success check: the golden outcomes allow the approved localhost-plus-correct-Origin case, and deny or quarantine wrong-Origin, missing-Origin, or unintended non-local exposure cases.

## Packet 3 — Roots and path-confinement fixtures
- Artifact type: file-operation fixtures with canonical, relative, and reshaped path targets.
- Intended assertion: roots only count as a control when canonical path resolution stays inside the approved boundary and ambiguous resolution fails closed.
- Minimal success check: the golden outcomes allow one canonical in-root operation and deny or approval-gate `..` escapes, alias/symlink-style reshaping, wildcard expansion, and out-of-root write attempts.

## Packet 4 — Elicitation abuse fixtures
- Artifact type: elicitation request corpus with expected trust and consent outcomes.
- Intended assertion: sensitive collection is not handled as ordinary form input, and the user-facing path must disclose destination and purpose before any approval-worthy secret flow.
- Minimal success check: form-mode secret requests are always blocked, URL-mode secret collection is only marked acceptable when disclosure and consent fields are present, and misleading consent wording is not auto-allowed.

## Packet 5 — Provenance tampering fixtures
- Artifact type: response-envelope fixtures covering intact, stripped, replayed, and forged provenance states.
- Intended assertion: downstream trust decisions change when provenance is missing, altered, or untrusted.
- Minimal success check: the golden outcomes allow trusted follow-on handling only for the intact trusted envelope, and downgrade, deny, or approval-gate stripped, replayed, or forged variants.

## Packet 6 — Cross-server trust-chain fixtures
- Artifact type: multi-hop workflow traces spanning trusted, semi-trusted, and adversarial servers.
- Intended assertion: low-trust output cannot silently trigger a privileged action on a higher-trust server without an explicit trust upgrade step such as verification or approval.
- Minimal success check: tainted cross-server handoffs are blocked or approval-gated, claimed trusted identity from an untrusted server is rejected, and one explicitly verified benign handoff remains allowed.

## Packet 7 — First-wave assembly pass
- Artifact type: short coverage matrix linking packets to the first-wave control tracks.
- Intended assertion: the fixture wave is sufficient to exercise the next engineering round without expanding into later tracks.
- Minimal success check: the matrix shows direct coverage for auth-focused cases, Streamable HTTP/origin cases, roots/path cases, elicitation abuse, provenance tampering, and cross-server trust chains, with Packet 1 feeding policy gating, Packet 5 feeding provenance handling, and Packet 6 feeding trust-chain control.

## Recommended build order
1. Packet 0
2. Packet 1
3. Packet 2
4. Packet 3
5. Packet 4
6. Packet 5
7. Packet 6
8. Packet 7

## Done definition for this wave
- Each packet has a written fixture spec and golden expected outcomes.
- Every required abuse family has at least one block/gate case and one benign comparison case.
- No packet depends on implementation code to be reviewed and accepted.
