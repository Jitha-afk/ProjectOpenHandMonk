# Client Setup

Use this document to connect an MCP client to the evil MCP server.

If you only need to confirm the server is alive, use docs/CLIENT_SANITY_CHECKLIST.md.
If you want a live presentation flow, use docs/LIVE_DEMO.md.

## SSE setup

Start the server first:

```bash
PYTHONPATH=src .venv/bin/python -m evil_server.server \
  --transport sse \
  --host 127.0.0.1 \
  --port 9000
# Windows PowerShell:
#   $env:PYTHONPATH='src'; .\.venv\Scripts\python.exe -m evil_server.server --transport sse --host 127.0.0.1 --port 9000
```

Connect your client to:

```text
http://127.0.0.1:9000/sse
```

The callback logger starts automatically on:

```text
http://127.0.0.1:8080/callback
```

## stdio setup

For clients that launch MCP servers as subprocesses, use:

Command:
```text
.venv/bin/python
Windows: .venv\Scripts\python.exe
```

Args:
```text
-m evil_server.server
```

Env:
```text
PYTHONPATH=src
```

Working directory:
```text
/path/to/ProjectOpenHandMonk/poc/mcp-security-bench
```

Include `cwd` in copy-paste client configs when the client supports it.

## VS Code / GitHub Copilot

Example shape:

```json
{
  "mcp": {
    "servers": {
      "evil-mcp-security-bench": {
        "type": "stdio",
        "command": ".venv/bin/python",
        "args": ["-m", "evil_server.server"],
        "cwd": "/absolute/path/to/ProjectOpenHandMonk/poc/mcp-security-bench",
        "env": {
          "PYTHONPATH": "src"
        }
      }
    }
  }
}
```

Notes:
- If you are on Windows, point command to `.venv\\Scripts\\python.exe`.
- Always set `cwd` to the project root so `PYTHONPATH=src` resolves correctly.
- If you are using SSE instead of stdio, connect directly to the SSE URL rather than launching the process from VS Code.

## Cursor

Example `.cursor/mcp.json` shape:

```json
{
  "mcpServers": {
    "evil-mcp-security-bench": {
      "command": ".venv/bin/python",
      "args": ["-m", "evil_server.server"],
      "cwd": "/absolute/path/to/ProjectOpenHandMonk/poc/mcp-security-bench",
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```

## Claude Desktop

Example config shape:

```json
{
  "mcpServers": {
    "evil-mcp-security-bench": {
      "command": ".venv/bin/python",
      "args": ["-m", "evil_server.server"],
      "cwd": "/absolute/path/to/ProjectOpenHandMonk/poc/mcp-security-bench",
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```

## Expected visible tools for a healthy connection

At minimum, you should see tools like:
- server_info
- record_analytics
- sync_telemetry
- get_weather
- check_service_status
- read_file
- execute_shell_command
- run_command
- ping_host
- traceroute
- dns_lookup

If these are missing, do the sanity checklist before attempting a live demo.
