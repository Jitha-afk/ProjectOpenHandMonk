# AGT mcp-scan Sandbox Validation for Mira

Document type: internal Mira handoff / PR artifact
Project: ProjectOpenHandMonk `poc/mcp-security-bench`
Scope: AGT repaired `mcp-scan` CLI against intentionally vulnerable MCP sandbox labs
Status: validation handoff, not benchmark certification

## One clear claim

The repaired Agent Governance Toolkit `mcp-scan` CLI demonstrated metadata-level visibility against two intentionally vulnerable MCP labs over SSE: ProjectOpenHandMonk EvilBench and Damn Vulnerable MCP Server (DVMCP). In both runs, the scanner successfully inspected advertised MCP primitives and surfaced expected critical signals from static MCP metadata.

This validates scanner visibility and reporting behavior for the tested sandbox configurations. It does not certify either benchmark, prove runtime prevention, establish exploit blocking, or measure production detection coverage.

## Evidence map

Paths are relative to `poc/mcp-security-bench`.

| Evidence question | Artifact(s) |
| --- | --- |
| What SSE endpoints were scanned? | `artifacts/agt-mcp-scan-validation/evilbench-sse-mcp.json`; `artifacts/agt-mcp-scan-validation/dvmcp-sse-mcp.json` |
| What did the scanner report in raw JSON? | `artifacts/agt-mcp-scan-validation/evilbench-sse-scan.json`; `artifacts/agt-mcp-scan-validation/dvmcp-sse-scan.json` |
| What are the normalized findings summaries? | `artifacts/agt-mcp-scan-validation/evilbench-sse-findings-summary.md`; `artifacts/agt-mcp-scan-validation/dvmcp-sse-findings-summary.md` |
| Was there independent review of the scan artifacts? | `artifacts/agt-mcp-scan-validation/klive-evilbench-scan-review.md`; `artifacts/agt-mcp-scan-validation/klive-dvmcp-scan-review.md` |

## Test scope

### EvilBench

Observed setup:
- Target: ProjectOpenHandMonk EvilBench MCP server.
- Transport: SSE.
- Endpoint: `http://127.0.0.1:19000/sse`.
- Evidence: `artifacts/agt-mcp-scan-validation/evilbench-sse-mcp.json`.

Observed scan facts:
- `mcp-scan` exit code: `2`.
- Exit code interpretation: expected because critical findings were present.
- Inspection status: `ok=true`.
- Transport reported by inspection: `sse`.
- Protocol reported by inspection: `2025-11-25`.
- Servers scanned: 1.
- Primitives discovered/scanned: 38 total.
  - Tools: 32.
  - Resources: 5.
  - Resource templates: 1.
  - Prompts: 0.
- Primitives flagged: 9.
  - Critical findings: 8.
  - Warnings: 1.

Observed finding categories:
- Hidden-instruction findings on metadata containing instruction-like `system:` patterns.
- Tool-poisoning findings on command-shaped required fields.
- One warning for an overly permissive object schema.

Klive review result:
- `PASS`, per `artifacts/agt-mcp-scan-validation/klive-evilbench-scan-review.md`.
- Klive assessed the findings as expected for an intentionally vulnerable benchmark server.
- Klive explicitly bounded the evidence to metadata/static inspection and scanner reporting behavior, not runtime prevention.

### DVMCP

Observed setup:
- Target: Damn Vulnerable MCP Server.
- Source repository: `https://github.com/harishsg993010/damn-vulnerable-MCP-server`.
- Commit observed locally: `79734c19f5104cd11486c90926d245560f53befa`.
- Transport: SSE.
- Challenge servers: 10 local SSE endpoints on ports `9001` through `9010`.
- Evidence: `artifacts/agt-mcp-scan-validation/dvmcp-sse-mcp.json`.

Observed scan facts:
- `mcp-scan` exit code: `2`.
- Exit code interpretation: expected because critical findings were present.
- Servers scanned: 10.
- Successful inspections: 10/10.
- Inspection errors: none.
- Transport reported by inspections: `sse`.
- Protocol reported by inspections: `2025-11-25`.
- Primitives scanned: 20.
- Primitives flagged: 3.
- Total critical findings: 4.
- Warnings: 0.

Flagged DVMCP surfaces:
- Challenge 2, `execute_command`: critical tool-poisoning finding for suspicious required field `command`.
- Challenge 9, `remote_access`: critical hidden-instruction finding for instruction-like metadata and critical tool-poisoning finding for suspicious required field `command`.
- Challenge 10, `resource:system://info`: critical hidden-instruction finding for instruction-like metadata.

Klive review result:
- `PASS`, per `artifacts/agt-mcp-scan-validation/klive-dvmcp-scan-review.md`.
- Klive assessed the findings as expected for an intentionally vulnerable lab.
- Klive emphasized that metadata-only scanning may miss DVMCP vulnerabilities that require runtime interaction, hidden state changes, tool invocation, resource reads, or other non-advertised behavior.

## Observed facts vs. interpretation

Observed facts:
- The AGT `mcp-scan` CLI connected to the configured SSE endpoints and completed metadata inspection for EvilBench and all 10 DVMCP challenge servers.
- Both runs returned exit code `2`, consistent with completed scans that found critical findings.
- EvilBench produced 9 flagged primitives from 38 discovered/scanned primitives.
- DVMCP produced 3 flagged primitives and 4 critical findings from 20 scanned primitives.
- The scanner reported `transport=sse` and `protocol=2025-11-25` in the successful inspections.
- Klive reviewed both artifact sets and marked both validations `PASS`.

Interpretation:
- The repaired `mcp-scan` CLI is functioning for the tested SSE metadata-inspection workflow.
- The scanner can see and report several expected metadata-exposed MCP risk patterns in intentionally vulnerable labs.
- The EvilBench result is a strong visibility signal because a broad advertised primitive surface was enumerated and multiple expected suspicious metadata patterns were flagged.
- The DVMCP result is a narrower but still useful visibility signal: the scanner successfully inspected all 10 servers, but only flagged vulnerabilities represented in advertised metadata patterns covered by the default rules.
- Absence of findings on other DVMCP challenges must not be read as evidence that those challenges are safe.

## Important limits

This validation is deliberately narrow.

- Scanner visibility validation only: this is not benchmark certification.
- Metadata-only behavior: the default scan enumerated advertised MCP primitive metadata.
- No MCP tools were invoked by the scanner.
- No exploits were executed.
- No resources were read for exploit confirmation.
- No runtime prevention, exploit blocking, sandbox enforcement, or safe-execution behavior was tested.
- No false-positive or false-negative rate is established.
- These are intentionally vulnerable sandbox labs, not evidence of real-world prevalence.
- Built-in/default metadata rules may miss runtime-only, stateful, output-mediated, or non-advertised MCP vulnerabilities.

## Mira-facing narrative posture

Recommended framing:

The AGT repair should be described as making `mcp-scan` useful for live MCP metadata inspection, with clear evidence that it can enumerate SSE MCP primitive surfaces and flag suspicious metadata in known-hostile labs. The strongest claim is operational and bounded: the scanner saw what the servers advertised and produced expected findings without needing to execute tools or exploits.

Avoid framing this as:
- proof that AGT detects all MCP attacks;
- proof that EvilBench or DVMCP are fully covered;
- proof that unflagged DVMCP challenges are benign;
- runtime safety validation;
- benchmark certification.

## Bottom line

For the `mcp-security-bench` POC, these artifacts support a concise validation statement:

AGT's repaired `mcp-scan` CLI passed sandbox visibility checks against EvilBench and DVMCP over SSE. It completed metadata inspection, returned expected critical-finding exit codes, surfaced expected suspicious advertised metadata, and was independently reviewed as `PASS` by Klive. The result is suitable for a PR evidence artifact if kept within the stated boundary: metadata scanner visibility, not comprehensive MCP security certification.
