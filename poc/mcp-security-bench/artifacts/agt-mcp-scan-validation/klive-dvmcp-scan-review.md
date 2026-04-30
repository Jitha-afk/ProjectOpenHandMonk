# Klive review: DVMCP AGT mcp-scan validation

Status: PASS

Scope reviewed:
- Config: `/home/sealjitha/projects/ProjectOpenHandMonk/poc/mcp-security-bench/artifacts/agt-mcp-scan-validation/dvmcp-sse-mcp.json`
- Raw JSON: `/home/sealjitha/projects/ProjectOpenHandMonk/poc/mcp-security-bench/artifacts/agt-mcp-scan-validation/dvmcp-sse-scan.json`
- stderr: `/home/sealjitha/projects/ProjectOpenHandMonk/poc/mcp-security-bench/artifacts/agt-mcp-scan-validation/dvmcp-sse-scan.stderr`
- exit code: `/home/sealjitha/projects/ProjectOpenHandMonk/poc/mcp-security-bench/artifacts/agt-mcp-scan-validation/dvmcp-sse-scan.exit_code`
- summary: `/home/sealjitha/projects/ProjectOpenHandMonk/poc/mcp-security-bench/artifacts/agt-mcp-scan-validation/dvmcp-sse-findings-summary.md`
- DVMCP repo commit observed locally: `79734c19f5104cd11486c90926d245560f53befa`

Review result:
- AGT mcp-scan appears to have worked as intended for this validation pass.
- The config enumerates 10 SSE DVMCP challenge servers on `127.0.0.1:9001-9010`.
- The raw scan reports 10 servers scanned and 10 successful inspections.
- All inspections are `ok=true`, transport is `sse`, protocol is `2025-11-25`, and there are no inspection errors.
- Summary counts are internally consistent: `servers_scanned=10`, `primitives_scanned=20`, `primitives_flagged=3`, `critical=4`, `warnings=0`.
- Exit code is `2`, which is expected when critical findings are present.

Findings observed:
- `dvmcp-challenge-02-tool-poisoning / execute_command`: critical `tool_poisoning` for suspicious required field `command`.
- `dvmcp-challenge-09-remote-access-control / remote_access`: critical `hidden_instruction` for `system:`-like instruction pattern.
- `dvmcp-challenge-09-remote-access-control / remote_access`: critical `tool_poisoning` for suspicious required field `command`.
- `dvmcp-challenge-10-multi-vector / resource:system://info`: critical `hidden_instruction` for `system:`-like instruction pattern.

Interpretation:
- These findings are expected and appropriate for an intentionally vulnerable lab such as DVMCP.
- The scan demonstrates metadata-level visibility into several advertised malicious or suspicious MCP primitives.
- The absence of findings on the other DVMCP challenges should not be interpreted as proof that those challenge servers are safe.

Evidence boundaries and caveats:
- This validation is metadata scanning only; it inspected exposed MCP primitive metadata.
- The scan did not execute exploits, call tools for runtime behavior, read resources for exploit confirmation, or validate runtime prevention.
- This pass does not establish a false-positive rate or production detection coverage.
- Scanner stderr notes that built-in sample rules may not cover all MCP tool poisoning or prompt injection techniques.
- Only metadata-exposed signals are detected by this default scan path, so DVMCP vulnerabilities that require runtime interaction, hidden state changes, tool invocation, resource reads, or non-advertised behavior may not be surfaced.

Klive conclusion:
- PASS for Mira handoff: the repaired AGT mcp-scan CLI successfully connected to all 10 DVMCP SSE servers, completed metadata inspection without inspection errors, surfaced expected critical findings for exposed vulnerable metadata, and returned the expected non-zero critical-finding exit code.
