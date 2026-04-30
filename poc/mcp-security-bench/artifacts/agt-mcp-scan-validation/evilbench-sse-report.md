# MCP Security Scan Report

**Summary**

- Servers scanned: 1
- MCP metadata entries scanned: 38
- Warnings: 1
- Critical: 8

| Primitive | Server | Severity | Finding |
|---|---|---|---|
| search_records | evilbench-sse | critical | Instruction-like pattern in tool description: \bsystem\s*: |
| enhanced_calculate | evilbench-sse | critical | Instruction-like pattern in tool description: \bsystem\s*: |
| execute_shell_command | evilbench-sse | critical | Suspicious required field: 'command' |
| run_command | evilbench-sse | critical | Suspicious required field: 'command' |
| sandbox_run | evilbench-sse | critical | Suspicious required field: 'command' |
| container_exec | evilbench-sse | critical | Suspicious required field: 'command' |
| server_info | evilbench-sse | warning | Overly permissive schema: object type with no defined properties |
| resource:system://config | evilbench-sse | critical | Instruction-like pattern in tool description: \bsystem\s*: |
| resource:system://secrets | evilbench-sse | critical | Instruction-like pattern in tool description: \bsystem\s*: |

## Limitations

This report is scan evidence, not a certification. It inspects MCP primitive metadata and selected launch/endpoint configuration; it does not execute tools, read resources, render prompts, or prove that a server is benign.
