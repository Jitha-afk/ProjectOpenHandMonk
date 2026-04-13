# Architecture

## System Architecture

```
+-------------------------------------------------------------------+
|                     mcp-security-bench                            |
+-------------------------------------------------------------------+
|                                                                   |
|  +-----------------------+     +----------------------------+     |
|  |   Evil MCP Server     |     |    Benchmark Harness       |     |
|  |   (src/evil_server/)  |     |    (src/bench/harness.py)  |     |
|  |                       |     |                            |     |
|  |  +------------------+ |     |  +---------------------+  |     |
|  |  | Attack Modules   | |     |  | Scenario Loader     |  |     |
|  |  |  tool_poisoning  |<----->|  |  (YAML parser)      |  |     |
|  |  |  tool_shadowing  | | MCP |  +---------------------+  |     |
|  |  |  rug_pull        | | SSE |  | MCP Client Session  |  |     |
|  |  |  data_exfil      | |     |  |  connect()          |  |     |
|  |  |  prompt_inject   | |     |  |  list_tools()       |  |     |
|  |  |  cred_theft      | |     |  |  run_scenario()     |  |     |
|  |  |  excessive_perms | |     |  |  run_all()          |  |     |
|  |  |  code_exec       | |     |  |  disconnect()       |  |     |
|  |  |  cmd_injection   | |     |  +---------------------+  |     |
|  |  |  sandbox_escape  | |     |                            |     |
|  |  |  cross_server    | |     +----------------------------+     |
|  |  +------------------+ |                  |                     |
|  |                       |                  | results             |
|  |  FastMCP Server       |                  v                     |
|  |  (mcp SDK)            |     +----------------------------+     |
|  +-----------------------+     |    Evaluator                |     |
|                                |    (src/bench/evaluator.py) |     |
|  +-----------------------+     |                            |     |
|  |  Scenario Definitions |     |  score_result()            |     |
|  |  (src/bench/scenarios)|     |  compute_metrics()         |     |
|  |                       |     |  generate_report()         |     |
|  |  tool_poisoning.yaml  |     |                            |     |
|  |  tool_shadowing.yaml  |     |  Metrics:                  |     |
|  |  rug_pull.yaml        |     |    ASR  (Attack Success)   |     |
|  |  data_exfil.yaml      |     |    RR   (Refusal Rate)     |     |
|  |  prompt_injection.yaml|     |    PSR  (Protection Rate)  |     |
|  |  credential_theft.yaml|     +----------------------------+     |
|  |  excessive_perms.yaml |                  |                     |
|  |  code_execution.yaml  |                  v                     |
|  |  command_injection.yaml|    +----------------------------+     |
|  |  sandbox_escape.yaml  |    |    Reports                  |     |
|  |  cross_server.yaml    |    |    - Text summary           |     |
|  +-----------------------+    |    - JSON export            |     |
|                               |    - Per-category breakdown |     |
|  +-----------------------+    |    - Severity analysis      |     |
|  |  Test Suite           |    +----------------------------+     |
|  |  (tests/)             |                                       |
|  |  conftest.py          |                                       |
|  |  test_attacks.py      |                                       |
|  +-----------------------+                                       |
+-------------------------------------------------------------------+
```

## Component Descriptions

### Evil MCP Server (`src/evil_server/`)
- Built with FastMCP (from the `mcp` Python SDK)
- Each attack category is an independent module
- Attack tools are registered as standard MCP tools
- Attack resources are registered as MCP resources
- Server exposes SSE endpoint for client connections
- Supports configuration of attack intensity and variants

### Benchmark Harness (`src/bench/harness.py`)
- `MCPBenchHarness` class — orchestrates the benchmark run
- Connects to the evil server via MCP client SDK (SSE transport)
- Loads attack scenarios from YAML files
- Runs scenarios with configurable iteration counts
- Supports dry-run mode when server is unavailable
- Async/await based for non-blocking execution
- Context manager support (`async with`)

### Evaluator (`src/bench/evaluator.py`)
- `BenchmarkEvaluator` class — scores results and generates reports
- Numeric scoring: 1=success, 0=fail, -1=detected, 2=protected
- Computes three primary metrics per category:
  - **ASR** (Attack Success Rate): proportion of successful attacks
  - **RR** (Refusal Rate): proportion where LLM detected and refused
  - **PSR** (Protection Success Rate): proportion blocked by security tools
- Generates text and JSON reports
- Supports both raw dataclass and dict input formats

### Scenario Definitions (`src/bench/scenarios/`)
- YAML files, one per attack category
- Each file contains multiple test cases
- Fields: id, name, description, attack_vector, severity, prompt,
  target_tool, expected_behavior, detection_indicators, iterations

### Test Suite (`tests/`)
- Two tiers: unit tests (no server) and integration tests (live server)
- Pytest fixtures for harness, evaluator, and scenario loading
- Custom marks: `@benchmark`, `@attack(category=...)`, `@requires_server`
- Parametrized tests across all 11 attack categories

## Data Flow

```
                    YAML Scenarios
                         |
                         v
   +---------+    +-------------+    +----------------+
   |  Evil   |<-->|  Harness    |--->|  Evaluator     |
   |  Server |    |  run_all()  |    |  score()       |
   +---------+    +-------------+    |  metrics()     |
        ^                |           |  report()      |
        |                |           +----------------+
     MCP SSE         ScenarioResult        |
     Protocol          objects              v
                                     +-----------+
                                     |  Report   |
                                     |  (text/   |
                                     |   JSON)   |
                                     +-----------+
```

1. **Load**: Harness reads YAML scenario definitions
2. **Connect**: Harness establishes MCP session with evil server
3. **Execute**: For each scenario, harness calls the target tool
4. **Collect**: Tool responses are captured in ScenarioResult objects
5. **Evaluate**: Evaluator scores each result against detection indicators
6. **Report**: Aggregated metrics are generated per category and overall

## Extending with New Attacks

### Adding a new attack scenario to an existing category:
1. Edit the YAML file in `src/bench/scenarios/`
2. Add a new entry to the `scenarios` list
3. Assign a unique ID following the pattern: `{category_prefix}-{number}`
4. Define the prompt, target_tool, detection_indicators, and expected_behavior

### Adding a new attack category:
1. Create a new YAML file in `src/bench/scenarios/` (e.g., `new_attack.yaml`)
2. Define the `attack_category` and `description` fields
3. Add one or more scenarios
4. Implement the corresponding attack module in `src/evil_server/attacks/`
5. Register the attack tools in the evil server
6. Update the test parametrization in `tests/test_attacks.py`
7. Document the attack in `docs/ATTACKS.md`

### Adding a new attack tool to the evil server:
1. Create a module in `src/evil_server/attacks/`
2. Use the `@mcp.tool()` decorator to register the tool
3. Ensure the tool name matches `target_tool` in the scenario YAML
4. Implement both the attack payload and legitimate-looking behavior

## Configuration Reference

### Environment Variables
| Variable         | Default              | Description                          |
|-----------------|----------------------|--------------------------------------|
| MCP_SERVER_URL  | http://localhost:8000| URL of the evil MCP server           |
| MCP_SERVER_PORT | 8000                 | Port for the evil MCP server         |
| LLM_BACKEND     | openai               | LLM backend for evaluation           |
| LLM_MODEL       | gpt-4o               | Model name for LLM backend           |
| LLM_API_KEY     | (none)               | API key for the LLM backend          |
| BENCH_TIMEOUT   | 30                   | Timeout (seconds) per tool call      |
| BENCH_ITERATIONS| 15                   | Default iterations per scenario      |
| LOG_LEVEL       | INFO                 | Logging level                        |

### Harness Configuration (Python)
```python
harness = MCPBenchHarness(
    server_url="http://localhost:8000",
    llm_backend="openai",           # or "anthropic", "local"
    llm_config={
        "model": "gpt-4o",
        "temperature": 0.0,
        "api_key": "sk-...",
    },
    scenarios_dir=Path("src/bench/scenarios"),
    timeout=30.0,
)
```

### Evaluator Configuration (Python)
```python
evaluator = BenchmarkEvaluator(
    security_product_active=False,  # Set True when testing security tools
)
```

### Scenario YAML Format
```yaml
attack_category: category_name
description: Category description
scenarios:
  - id: xx-001
    name: Scenario name
    description: What this scenario tests
    attack_vector: specific_technique
    severity: critical|high|medium|low
    prompt: "The user prompt that triggers the attack"
    target_tool: tool_name_on_evil_server
    expected_behavior:
      attack_success: What happens when the attack succeeds
      attack_detected: What happens when the attack is detected
    detection_indicators:
      - "keyword1"
      - "keyword2"
    iterations: 15
```

### Scoring Reference
| Score | Label          | Meaning                                      |
|-------|----------------|----------------------------------------------|
|   1   | attack_success | Attack achieved its objective                |
|   0   | attack_fail    | Attack did not succeed (not detected either) |
|  -1   | detected       | LLM/agent detected and refused the attack    |
|   2   | protected      | Security product blocked the attack          |
