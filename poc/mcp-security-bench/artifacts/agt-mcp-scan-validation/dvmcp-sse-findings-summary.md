# dvmcp-sse AGT mcp-scan findings summary

- Config: `/home/sealjitha/projects/ProjectOpenHandMonk/poc/mcp-security-bench/artifacts/agt-mcp-scan-validation/dvmcp-sse-mcp.json`
- Raw JSON: `/home/sealjitha/projects/ProjectOpenHandMonk/poc/mcp-security-bench/artifacts/agt-mcp-scan-validation/dvmcp-sse-scan.json`
- Exit code: `2`
- Servers scanned: 10
- Primitives scanned: 20
- Primitives flagged: 3
- Critical findings: 4
- Warnings: 0

## Inspection status
- dvmcp-challenge-01-basic-prompt-injection: ok=True, transport=sse, protocol=2025-11-25, primitives=3, tools=1, resources=1, templates=1, prompts=0
- dvmcp-challenge-02-tool-poisoning: ok=True, transport=sse, protocol=2025-11-25, primitives=2, tools=2, resources=0, templates=0, prompts=0
- dvmcp-challenge-03-excessive-permissions: ok=True, transport=sse, protocol=2025-11-25, primitives=2, tools=1, resources=0, templates=1, prompts=0
- dvmcp-challenge-04-rug-pull: ok=True, transport=sse, protocol=2025-11-25, primitives=1, tools=1, resources=0, templates=0, prompts=0
- dvmcp-challenge-05-tool-shadowing: ok=True, transport=sse, protocol=2025-11-25, primitives=2, tools=2, resources=0, templates=0, prompts=0
- dvmcp-challenge-06-indirect-prompt-injection: ok=True, transport=sse, protocol=2025-11-25, primitives=1, tools=1, resources=0, templates=0, prompts=0
- dvmcp-challenge-07-token-theft: ok=True, transport=sse, protocol=2025-11-25, primitives=2, tools=2, resources=0, templates=0, prompts=0
- dvmcp-challenge-08-malicious-code-execution: ok=True, transport=sse, protocol=2025-11-25, primitives=2, tools=2, resources=0, templates=0, prompts=0
- dvmcp-challenge-09-remote-access-control: ok=True, transport=sse, protocol=2025-11-25, primitives=2, tools=2, resources=0, templates=0, prompts=0
- dvmcp-challenge-10-multi-vector: ok=True, transport=sse, protocol=2025-11-25, primitives=3, tools=2, resources=1, templates=0, prompts=0

## Findings
- dvmcp-challenge-02-tool-poisoning / execute_command: critical tool_poisoning — Suspicious required field: 'command'
- dvmcp-challenge-09-remote-access-control / remote_access: critical hidden_instruction — Instruction-like pattern in tool description: \bsystem\s*:
- dvmcp-challenge-09-remote-access-control / remote_access: critical tool_poisoning — Suspicious required field: 'command'
- dvmcp-challenge-10-multi-vector / resource:system://info: critical hidden_instruction — Instruction-like pattern in tool description: \bsystem\s*:

## Evidence boundary
- This is MCP metadata inspection. The scan does not call tools, exploit servers, read resources, or prove runtime prevention.
- Exit code 2 is expected when critical findings are present.
- These servers are intentionally vulnerable labs; findings indicate scanner visibility over advertised primitive metadata, not real-world prevalence or a calibrated false-positive rate.
