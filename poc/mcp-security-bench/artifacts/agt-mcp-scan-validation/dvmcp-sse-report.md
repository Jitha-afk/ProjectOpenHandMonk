# MCP Security Scan Report

**Summary**

- Servers scanned: 10
- MCP metadata entries scanned: 20
- Warnings: 0
- Critical: 4

| Primitive | Server | Severity | Finding |
|---|---|---|---|
| execute_command | dvmcp-challenge-02-tool-poisoning | critical | Suspicious required field: 'command' |
| remote_access | dvmcp-challenge-09-remote-access-control | critical | Instruction-like pattern in tool description: \bsystem\s*: |
| remote_access | dvmcp-challenge-09-remote-access-control | critical | Suspicious required field: 'command' |
| resource:system://info | dvmcp-challenge-10-multi-vector | critical | Instruction-like pattern in tool description: \bsystem\s*: |

## Limitations

This report is scan evidence, not a certification. It inspects MCP primitive metadata and selected launch/endpoint configuration; it does not execute tools, read resources, render prompts, or prove that a server is benign.
