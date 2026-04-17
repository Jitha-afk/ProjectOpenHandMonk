# mcp-security-bench

> A benchmark suite and live demo corpus for evaluating LLM and security tool resilience against MCP (Model Context Protocol) attacks.

## Status
`building`

## Overview

mcp-security-bench is a structured project for testing how well LLMs, AI agents, and security products defend against attacks delivered through the Model Context Protocol. It includes:

- Evil MCP Server — A FastMCP server implementing 11 attack categories as MCP tools/resources
- Benchmark Harness — Automated test runner for scenario execution
- Evaluator — Scoring engine for Attack Success Rate, Refusal Rate, and Protection Success Rate
- Demo Artifacts — visible proof files and logs for live demonstrations
- Scenario Library — attack scenarios across 11 categories, defined in YAML

## Choose your path

If you want to...

- Run a short, panel-friendly demonstration:
  - read `docs/LIVE_DEMO.md`
- Verify a client can connect and see the server correctly:
  - read `docs/CLIENT_SANITY_CHECKLIST.md`
- Configure VS Code, Cursor, Claude Desktop, or generic clients:
  - read `docs/CLIENT_SETUP.md`
- Study the full attack taxonomy and OWASP mappings:
  - read `docs/ATTACKS.md`
- Run the automated benchmark harness:
  - continue below in this README

## Quick Start

### Prerequisites
```bash
python 3.11+
python -m venv .venv
. .venv/bin/activate
pip install -e .[dev]
# Windows PowerShell:
#   py -m venv .venv
#   .\.venv\Scripts\Activate.ps1
#   pip install -e .[dev]
```

### 1. Start the Evil MCP Server
```bash
PYTHONPATH=src .venv/bin/python -m evil_server.server --transport sse --host 127.0.0.1 --port 9000
# Windows PowerShell example:
#   $env:PYTHONPATH='src'; .\.venv\Scripts\python.exe -m evil_server.server --transport sse --host 127.0.0.1 --port 9000
# SSE endpoint: http://127.0.0.1:9000/sse
# Callback endpoint: http://127.0.0.1:8080/callback
# Demo artifacts: ./artifacts/
```

### 2. Run the Benchmark
```bash
# Run unit tests (no server needed)
PYTHONPATH=src .venv/bin/python -m pytest tests/test_attacks.py -m "not requires_server" -v

# Run feature/demo regression tests
PYTHONPATH=src .venv/bin/python -m pytest tests/test_demo_features.py tests/test_server_startup.py -v

# Run full benchmark (server must be running)
PYTHONPATH=src .venv/bin/python -m pytest tests/test_attacks.py -m requires_server -v

# Run specific attack category
PYTHONPATH=src .venv/bin/python -m pytest tests/test_attacks.py -k "tool_poisoning" -v
```

### 3. Run Programmatically
```python
import asyncio
from src.bench import MCPBenchHarness, BenchmarkEvaluator

async def main():
    harness = MCPBenchHarness(server_url="http://127.0.0.1:9000/sse")
    await harness.connect()

    results = await harness.run_all()
    await harness.disconnect()

    evaluator = BenchmarkEvaluator()
    report = evaluator.generate_report(results)
    print(report.to_text())

asyncio.run(main())
```

## Attack Categories

| # | Category             | ID Prefix | Severity | Scenarios | OWASP MCP      | Description                                        |
|---|----------------------|-----------|----------|-----------|----------------|---------------------------------------------------|
| 1 | Tool Poisoning       | tp-       | high     | 3         | MCP03:2025, MCP06:2025 | Malicious instructions hidden in tool metadata      |
| 2 | Tool Shadowing       | ts-       | high     | 2         | MCP03:2025, MCP09:2025 | Impersonating legitimate tools                      |
| 3 | Rug Pull             | rp-       | critical | 2         | MCP03:2025, MCP04:2025 | Behavior change after trust establishment           |
| 4 | Data Exfiltration    | de-       | critical | 3         | MCP01:2025, MCP10:2025 | Stealing data via tools                             |
| 5 | Prompt Injection     | pi-       | high     | 2         | MCP06:2025       | Indirect injection via tool responses               |
| 6 | Credential Theft     | ct-       | critical | 2         | MCP01:2025, MCP07:2025 | Stealing auth tokens and credentials                |
| 7 | Excessive Permissions| ep-       | high     | 2         | MCP02:2025, MCP07:2025 | Tools exceeding their stated access scope           |
| 8 | Code Execution       | ce-       | critical | 2         | MCP05:2025       | Arbitrary code execution via tools                  |
| 9 | Command Injection    | ci-       | critical | 2         | MCP05:2025       | OS command injection through tool parameters        |
|10 | Sandbox Escape       | se-       | critical | 2         | MCP05:2025, MCP02:2025 | Breaking out of container/sandbox isolation         |
|11 | Cross-Server Attack  | cs-       | critical | 2         | MCP09:2025, MCP06:2025, MCP10:2025 | Exploiting multi-server LLM configurations     |

## Metrics

The evaluator computes three primary metrics:

- **ASR (Attack Success Rate)**: Proportion of iterations where the attack achieved its objective. Higher = more vulnerable.
- **RR (Refusal Rate)**: Proportion where the LLM detected the attack and refused. Higher = better LLM safety.
- **PSR (Protection Success Rate)**: Proportion where a security product blocked the attack. Higher = better security tool.

### Scoring
| Score | Label          | Meaning                                      |
|-------|----------------|----------------------------------------------|
|   1   | attack_success | Attack achieved its objective                |
|   0   | attack_fail    | Attack failed (not detected)                 |
|  -1   | detected       | LLM/agent detected and refused               |
|   2   | protected      | Security product blocked the attack          |

## Configuration

Set via environment variables:

| Variable         | Default              | Description                    |
|-----------------|----------------------|--------------------------------|
| MCP_SERVER_URL  | http://127.0.0.1:9000/sse | Evil MCP SSE endpoint      |
| LLM_BACKEND     | openai               | LLM provider to evaluate       |
| LLM_MODEL       | gpt-4o               | Model name                     |
| LLM_API_KEY     | (none)               | API key for LLM provider       |
| BENCH_TIMEOUT   | 30                   | Timeout per tool call (sec)    |

## Adding New Attacks

1. Create/edit a YAML scenario file in `src/bench/scenarios/`
2. Implement the attack tool in `src/evil_server/attacks/`
3. Register the tool in the evil server
4. Add documentation to `docs/ATTACKS.md`

See `design/ARCHITECTURE.md` for detailed extension guide.

## Project Structure

```
mcp-security-bench/
├── README.md                     # This file
├── design/
│   └── ARCHITECTURE.md           # System architecture and config reference
├── docs/
│   └── ATTACKS.md                # Full attack taxonomy documentation
├── src/
│   ├── bench/
│   │   ├── __init__.py
│   │   ├── harness.py            # MCPBenchHarness — test orchestrator
│   │   ├── evaluator.py          # BenchmarkEvaluator — scoring engine
│   │   └── scenarios/            # YAML attack scenario definitions
│   │       ├── tool_poisoning.yaml
│   │       ├── tool_shadowing.yaml
│   │       ├── rug_pull.yaml
│   │       ├── data_exfil.yaml
│   │       ├── prompt_injection.yaml
│   │       ├── credential_theft.yaml
│   │       ├── excessive_perms.yaml
│   │       ├── code_execution.yaml
│   │       ├── command_injection.yaml
│   │       ├── sandbox_escape.yaml
│   │       └── cross_server.yaml
│   └── evil_server/              # Evil MCP server (built separately)
│       └── ...
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Fixtures and markers
│   └── test_attacks.py           # Unit + integration test suite
└── research/
    └── ...
```

## References

- [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/) — Standardized risk classification for MCP deployments
- [MCP Specification](https://modelcontextprotocol.io/specification) — Official Model Context Protocol specification
- [MCPSecBench Paper](https://arxiv.org/abs/2508.13220) (arXiv:2508.13220) — Academic benchmark for MCP security evaluation
- [Awesome MCP Security](https://github.com/Puliczek/awesome-mcp-security) — Curated list of MCP security resources
- [MCP Injection Experiments](https://github.com/invariantlabs-ai/mcp-injection-experiments) — Invariant Labs prompt injection research
- [damn-vulnerable-MCP-server](https://github.com/harishsg993010/damn-vulnerable-MCP-server) — Intentionally vulnerable MCP server for testing
- [evil-mcp-server](https://github.com/promptfoo/evil-mcp-server) — Malicious MCP server demonstrating attack vectors
- [Invariant Labs Blog — MCP Security](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) — Tool poisoning attack analysis
- [Anthropic MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices) — Official MCP security guidance

## License

This project is for security research and educational purposes only. Use responsibly.
