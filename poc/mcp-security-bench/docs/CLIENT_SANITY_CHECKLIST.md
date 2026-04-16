# Client Sanity Checklist

Purpose: verify that the local `mcp-security-bench` server is real, reachable, and usable by an MCP client without doing broad end-to-end attack validation.

Use this checklist when the server is already running in SSE mode:

- SSE endpoint: `http://127.0.0.1:9000/sse`
- Callback endpoint: `http://127.0.0.1:8080/callback`

## Preconditions

- Start the server from the project root:

```bash
PYTHONPATH=src .venv/bin/python -m evil_server.server \
  --transport sse \
  --host 127.0.0.1 \
  --port 9000
```

- The callback logger now starts automatically on port `8080` by default.
- To change the callback port, add `--callback-port <port>`.
- To disable callback startup entirely, add `--no-callback`.

- Confirm startup logs include:
  - `Listening on http://0.0.0.0:8080/callback`
  - `Callback server on port 8080`
  - `Starting with transport=sse`

## Minimal client validation

For each client under test, perform only these checks.

### 1. Connect to the server

Expected result:
- The client connects to `http://127.0.0.1:9000/sse` successfully.
- No manual restart or protocol workaround is needed.

Record:
- PASS / FAIL
- Any connection error shown by the client

### 2. Enumerate tools

Expected result:
- The client shows tools from the evil server.
- `server_info` is visible.
- `record_analytics` and `sync_telemetry` are visible.

Minimum expected evidence:
- Tool list is non-empty.
- Tool metadata loads without crashing the client.

Record:
- PASS / FAIL
- Number of visible tools, if the client exposes the count

### 3. Enumerate resources

Expected result:
- The client can see that the server exposes resources.
- At minimum, the client does not break when resources exist.

Known resources:
- `internal://credentials`
- `system://config`
- `system://secrets`
- `tokens://active`
- `company://confidential`

Record:
- PASS / FAIL
- Whether resources are visible, hidden, or unsupported by the client

### 4. Call `server_info`

Prompt the client to call `server_info` and show the output.

Expected result:
- The tool call succeeds.
- The response includes the server name and enabled module summary.

Record:
- PASS / FAIL
- Returned text or screenshot

### 5. Optional benign callback verification

Use an explicit, benign invocation only. Do not perform broad attack testing here.

Call `record_analytics` with dummy values such as:
- `toolName=local_sanity_check`
- `toolArgs={"kind":"benign","value":1}`
- `toolResult=ok`
- `customerData=dummy`

Expected result:
- Tool returns success text.
- `securitytest.txt` is created in the project root.
- Callback log receives a POST with dummy values only.

Check callback log locally:

```bash
curl -sS http://127.0.0.1:8080/callback/log
```

Record:
- PASS / FAIL
- Whether callback entry appears
- Whether the logged payload matches the dummy invocation

## What not to do in this checklist

- Do not attempt broad offensive end-to-end attack validation.
- Do not try to measure jailbreak success here.
- Do not treat this checklist as a benchmark of attack success rate.
- Do not use real credentials, personal data, or sensitive files.

## Suggested result template

```text
Client:
Version:
Transport: SSE

1. Connect: PASS/FAIL
2. Tool enumeration: PASS/FAIL
3. Resource handling: PASS/FAIL
4. server_info call: PASS/FAIL
5. Benign callback verification: PASS/FAIL/NOT RUN

Notes:
- 
- 
- 
```

## Local known-good baseline

The following local checks have already been validated in this repo:

- SSE server starts successfully
- Callback server starts successfully
- Harness can connect to the live server
- Tool enumeration works
- Resource enumeration works
- `server_info` works
- Benign `record_analytics` invocation logs to the callback endpoint
- `securitytest.txt` is created by the local callback verification path
