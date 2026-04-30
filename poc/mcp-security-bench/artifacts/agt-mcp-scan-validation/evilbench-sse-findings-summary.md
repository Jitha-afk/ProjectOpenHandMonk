# evilbench-sse AGT mcp-scan findings summary

- Config: `/home/sealjitha/projects/ProjectOpenHandMonk/poc/mcp-security-bench/artifacts/agt-mcp-scan-validation/evilbench-sse-mcp.json`
- Raw JSON: `/home/sealjitha/projects/ProjectOpenHandMonk/poc/mcp-security-bench/artifacts/agt-mcp-scan-validation/evilbench-sse-scan.json`
- Exit code: `2`
- Servers scanned: 1
- Primitives scanned: 38
- Primitives flagged: 9
- Critical findings: 8
- Warnings: 1

## Inspection status
- evilbench-sse: ok=True, transport=sse, protocol=2025-11-25, primitives=38, tools=32, resources=5, templates=1, prompts=0

## Findings
- evilbench-sse / search_records: critical hidden_instruction — Instruction-like pattern in tool description: \bsystem\s*:
- evilbench-sse / enhanced_calculate: critical hidden_instruction — Instruction-like pattern in tool description: \bsystem\s*:
- evilbench-sse / execute_shell_command: critical tool_poisoning — Suspicious required field: 'command'
- evilbench-sse / run_command: critical tool_poisoning — Suspicious required field: 'command'
- evilbench-sse / sandbox_run: critical tool_poisoning — Suspicious required field: 'command'
- evilbench-sse / container_exec: critical tool_poisoning — Suspicious required field: 'command'
- evilbench-sse / server_info: warning tool_poisoning — Overly permissive schema: object type with no defined properties
- evilbench-sse / resource:system://config: critical hidden_instruction — Instruction-like pattern in tool description: \bsystem\s*:
- evilbench-sse / resource:system://secrets: critical hidden_instruction — Instruction-like pattern in tool description: \bsystem\s*:

## Evidence boundary
- This is MCP metadata inspection. The scan does not call tools, exploit servers, read resources, or prove runtime prevention.
- Exit code 2 is expected when critical findings are present.
- These servers are intentionally vulnerable labs; findings indicate scanner visibility over advertised primitive metadata, not real-world prevalence or a calibrated false-positive rate.
