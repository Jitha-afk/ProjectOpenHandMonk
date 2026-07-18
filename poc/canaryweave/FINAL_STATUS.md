# Final Status — CanaryWeave ASR Research Harness

Date closed: 2026-07-18
Disposition: validated controlled research POC, archived in place

## Completed scope

- Safe deterministic MCP protocol-confusion and sampling-abuse scenarios.
- Benign canaries, inert local sinks, and JSON-RPC-shaped evidence.
- Baseline, permissive MCP, and attested policy conditions.
- Real local MCP stdio client/server sampling demonstration.
- Source-structure adapters that do not copy raw upstream adversarial payloads.
- Research findings and paper draft with explicit evidence boundaries.

## Closure validation

- 60 project tests passed from a clean worktree based on current `main`.
- Source and wheel distributions built successfully.
- The reconstructed project tree matches the protected combined PR #9 snapshot, excluding only a FIDES-owned planning note that was relocated to the FIDES project.
- Both merge orders with the FIDES replacement branch were tested successfully.

## Claim boundaries

This artifact demonstrates controlled, deterministic policy behavior with synthetic canaries. It does not establish:

- attack success rates for production MCP hosts;
- live-model stochastic behavior;
- reproduction of an unavailable source benchmark or its reported numerical results;
- exploitability, secret theft, or outbound exfiltration;
- broad effectiveness of attestation across all MCP implementations.

Future work should start under a new, explicitly scoped issue rather than treating historical plans or handoffs as active commitments.
