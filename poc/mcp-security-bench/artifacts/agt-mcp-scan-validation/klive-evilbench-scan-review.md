# Klive review: EvilBench AGT mcp-scan validation

Status: PASS

Reviewed artifacts:
- Config: `evilbench-sse-mcp.json`
- Raw JSON: `evilbench-sse-scan.json`
- stderr: `evilbench-sse-scan.stderr`
- Exit code: `evilbench-sse-scan.exit_code`
- Summary: `evilbench-sse-findings-summary.md`

Findings:
- The scan targeted the expected SSE endpoint: `http://127.0.0.1:19000/sse`.
- AGT mcp-scan completed inspection successfully for `evilbench-sse`:
  - `ok=True`
  - `transport=sse`
  - `protocol_version=2025-11-25`
  - `error=null`
- Discovery counts match the handoff: 38 primitives discovered/scanned, consisting of 32 tools, 5 resources, 1 resource template, and 0 prompts.
- The scanner marked the server unsafe and reported 9 flagged primitives: 8 critical and 1 warning.
- The recorded exit code is 2, which is consistent with a scan that completed and found threats rather than a clean/no-finding result.
- stderr contains 9 `MCP scan found` lines, matching the 9 threats in the JSON output and summary.

Flagged primitives:
- `search_records` — critical hidden_instruction
- `enhanced_calculate` — critical hidden_instruction
- `execute_shell_command` — critical tool_poisoning
- `run_command` — critical tool_poisoning
- `sandbox_run` — critical tool_poisoning
- `container_exec` — critical tool_poisoning
- `server_info` — warning tool_poisoning
- `resource:system://config` — critical hidden_instruction
- `resource:system://secrets` — critical hidden_instruction

Assessment:
- PASS: the repaired AGT mcp-scan CLI appears to have worked as intended against the EvilBench SSE MCP server.
- The findings are expected for an intentionally vulnerable benchmark server. The detected hidden-instruction patterns, command-like required fields, permissive schema warning, and sensitive-looking system resources are aligned with EvilBench's purpose as a hostile/security-test target.

Evidence boundaries:
- This evidence validates metadata/static MCP primitive inspection and scanner reporting behavior.
- It does not prove runtime prevention, exploit blocking, sandbox enforcement, or safe execution behavior.
- It does not establish a false-positive or false-negative rate; the result is a single benchmark validation against an intentionally vulnerable server.
