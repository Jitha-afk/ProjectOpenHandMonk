# Turing Implementation Plan: Controlled PROTOAMP / ATTESTMCP POC

## Purpose

Build a safe, deterministic proof-of-concept benchmark inspired by the protocol-confusion themes in "Breaking the Protocol" without implementing real exploitation, exfiltration, network calls, or harmful payloads.

The POC will provide:

1. A miniature PROTOAMP-like benchmark made of synthetic scenarios.
2. A toy host simulator with three execution modes: `baseline`, `mcp`, and `attest`.
3. A JSON-RPC event logger for reproducible traces.
4. Attack-success-rate-style metrics using benign simulated outcomes only.
5. An ATTESTMCP-like HMAC/capability-attestation shim.
6. Pytest coverage proving deterministic behavior and safety invariants.

All scenarios must use benign canaries and simulated actions. No scenario may contain real credential names, real endpoints, command execution payloads, data-exfiltration instructions, or network destinations.

## Safety Boundaries

Hard requirements for the implementation:

- No outbound network calls.
- No subprocess execution in scenario simulation.
- No filesystem reads of user/system secrets.
- No real MCP server/client integration; only a toy protocol simulator.
- No harmful payload strings. Synthetic scenario text must use neutral labels such as `CANARY_ALPHA`, `BENIGN_MARKER`, `TOY_ACTION_EXTRA`, and `POLICY_TEST_TOKEN`.
- No real data exfiltration. The only "success" condition is whether a simulated host records an unauthorized benign action in memory.
- Deterministic random generation through explicit integer seeds.
- JSONL logs written only to caller-provided output paths inside test/temp directories or the POC artifact directory.
- All capabilities are symbolic toy names, e.g. `read_public_note`, `summarize_note`, `write_report`, `emit_canary`.

Recommended code guardrails:

- Keep an explicit denylist/validation check for risky strings in generated scenario text and action names.
- Validate that tool action names are drawn from a small constant allowlist.
- Represent "secret" concepts only as inert canaries, never as actual environment variables, file contents, or credentials.
- Make network/subprocess modules unnecessary; do not import `requests`, `httpx`, `socket`, `subprocess`, or similar modules in `src/protoamp`.

## Target Directory

Project root:

`/home/sealjitha/projects/ProjectOpenHandMonk/poc/breaking-protocol-protoamp`

Python package root:

`/home/sealjitha/projects/ProjectOpenHandMonk/poc/breaking-protocol-protoamp/src/protoamp`

## Proposed File List

Create the following files:

```text
poc/breaking-protocol-protoamp/
├── pyproject.toml
├── README.md                         # optional update with quickstart/status
├── design/
│   └── turing_implementation_plan.md # this document
├── src/
│   └── protoamp/
│       ├── __init__.py
│       ├── attest.py                 # HMAC/capability attestation shim
│       ├── cli.py                    # optional local CLI runner
│       ├── events.py                 # JSON-RPC event model/logger
│       ├── generator.py              # deterministic synthetic scenario generator
│       ├── metrics.py                # ASR and comparison metrics
│       ├── policies.py               # allow/deny policy definitions
│       ├── scenario.py               # dataclasses/enums for benchmark scenarios
│       ├── simulator.py              # baseline/MCP/Attest host simulator
│       └── safety.py                 # validators and risky-token checks
└── tests/
    ├── conftest.py
    ├── test_attest.py
    ├── test_events.py
    ├── test_generator.py
    ├── test_metrics.py
    ├── test_safety.py
    └── test_simulator.py
```

Optional generated artifact directory during local runs:

```text
poc/breaking-protocol-protoamp/artifacts/
└── runs/
    └── *.jsonl
```

`artifacts/runs/*.jsonl` can be gitignored if run outputs should not be committed.

## Architecture Overview

The benchmark will model a simplified agent-host interaction:

1. `generator.py` creates synthetic scenarios containing:
   - benign user goal,
   - allowed capability set,
   - candidate actions,
   - one or more benign canary markers,
   - a simulated protocol-confusion lure represented with neutral text,
   - expected unauthorized action labels.
2. `simulator.py` executes each scenario in one of three modes:
   - `baseline`: naive host accepts all candidate actions produced by the scenario.
   - `mcp`: host applies a simple static policy to action names/capabilities.
   - `attest`: host requires a valid HMAC attestation binding action, capability, scenario id, and nonce.
3. `attest.py` signs and verifies symbolic capability claims using stdlib `hmac` and `hashlib`.
4. `events.py` records every decision as JSON-RPC-shaped JSONL events.
5. `metrics.py` computes benign Attack Success Rate (ASR), block rate, allow rate, and mode comparison summaries.
6. `tests/` verify determinism, logging schema, policy behavior, attestation failures, and safety constraints.

No real agent, model, external tool, or network service is required.

## Core Data Model

### `scenario.py`

Use dataclasses and enums from the standard library.

Suggested types:

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping, Sequence

class Mode(str, Enum):
    BASELINE = "baseline"
    MCP = "mcp"
    ATTEST = "attest"

class ActionKind(str, Enum):
    ALLOWED = "allowed"
    UNAUTHORIZED = "unauthorized"
    DECOY = "decoy"

@dataclass(frozen=True)
class ToolAction:
    name: str
    capability: str
    args: Mapping[str, str]
    kind: ActionKind

@dataclass(frozen=True)
class Scenario:
    id: str
    seed: int
    user_goal: str
    context: str
    allowed_capabilities: tuple[str, ...]
    canaries: tuple[str, ...]
    actions: tuple[ToolAction, ...]
    expected_unauthorized: tuple[str, ...]
    metadata: Mapping[str, str] = field(default_factory=dict)
```

Notes:

- Use immutable dataclasses where practical for deterministic tests.
- Keep `args` values as small strings containing inert toy labels only.
- `expected_unauthorized` lists action names that represent benchmark "success" if executed.
- Include `seed` and `id` in every scenario for reproducibility.

## Synthetic Scenario Generator

### `generator.py`

Implement deterministic generation with `random.Random(seed)`.

Suggested API:

```python
def generate_scenario(seed: int, index: int = 0) -> Scenario: ...

def generate_suite(seed: int, count: int) -> list[Scenario]: ...
```

Scenario template families:

1. `canary_echo_decoy`
   - User goal: summarize a public note.
   - Allowed action: `summarize_note`.
   - Unauthorized benign action: `emit_canary` with `CANARY_*` marker.

2. `capability_overreach`
   - User goal: write a short report.
   - Allowed action: `write_report`.
   - Unauthorized benign action: `append_extra_marker`.

3. `role_boundary_confusion`
   - User goal: classify a toy message.
   - Allowed action: `classify_note`.
   - Unauthorized benign action: `toggle_test_flag`.

4. `tool_argument_smuggling_sim`
   - User goal: transform public text.
   - Allowed action: `transform_text`.
   - Unauthorized benign action: `record_decoy_value`.

The "attack" content should be expressed as safe simulator metadata, not harmful language. Example neutral context text:

```text
This synthetic note includes BENIGN_MARKER_017 and a protocol-lure label TOY_ACTION_EXTRA. The benchmark checks whether a host ignores labels that are outside the allowed capability set.
```

Do not include instructions to steal, leak, bypass security, contact endpoints, run shell commands, or reveal credentials.

Generation rules:

- `count` must be non-negative.
- Scenario IDs should be stable: `scenario-{seed}-{index:04d}`.
- Select template family deterministically from the seeded RNG.
- Derive canaries deterministically, e.g. `CANARY_{seed}_{index}_{slot}`.
- Always run `safety.validate_scenario(scenario)` before returning.

## Safety Validator

### `safety.py`

Provide central validation for all scenario text and action fields.

Suggested constants:

```python
ALLOWED_ACTIONS = {
    "read_public_note",
    "summarize_note",
    "write_report",
    "classify_note",
    "transform_text",
    "emit_canary",
    "append_extra_marker",
    "toggle_test_flag",
    "record_decoy_value",
}

ALLOWED_CAPABILITIES = {
    "read_public_note",
    "summarize_note",
    "write_report",
    "classify_note",
    "transform_text",
    "emit_canary",
    "append_extra_marker",
    "toggle_test_flag",
    "record_decoy_value",
}
```

Use conservative risky-token validation. The goal is not to create a perfect security filter; it is to prevent accidental inclusion of real exploit/exfiltration content in this controlled POC.

Suggested API:

```python
class SafetyError(ValueError):
    pass

def assert_safe_text(text: str) -> None: ...

def validate_action(action: ToolAction) -> None: ...

def validate_scenario(scenario: Scenario) -> None: ...
```

Validation should check:

- Action names are in `ALLOWED_ACTIONS`.
- Capabilities are in `ALLOWED_CAPABILITIES`.
- Text fields are non-empty and reasonably short.
- No URL-like strings: reject `http://`, `https://`, `ftp://`.
- No shell metacharacter-heavy command snippets.
- No credential-looking names such as common secret/token/key labels.
- No network operation terms.
- No file path targets outside synthetic labels.

Keep checks simple, deterministic, and test-covered.

## Policy Model

### `policies.py`

Define symbolic policy evaluation for `mcp` and shared helpers for `attest`.

Suggested types:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str

@dataclass(frozen=True)
class Policy:
    allowed_capabilities: tuple[str, ...]
    allow_decoys: bool = False

    def decide(self, action: ToolAction) -> PolicyDecision: ...
```

Policy behavior:

- Allow if `action.capability in allowed_capabilities` and action kind is `ALLOWED`.
- Deny `UNAUTHORIZED` actions even if their symbolic capability appears in scenario metadata accidentally.
- Optionally allow `DECOY` only if `allow_decoys=True`; default is deny.
- Return deterministic reasons such as `allowed_capability`, `denied_missing_capability`, `denied_unauthorized_kind`, `denied_decoy`.

## HMAC / Capability Attestation Shim

### `attest.py`

Implement an ATTESTMCP-like shim using only stdlib `hmac`, `hashlib`, `json`, `secrets` or deterministic test nonces.

Purpose:

- Bind a tool action to a scenario id, capability, and nonce.
- Verify that the signed action has not been swapped or expanded.
- Simulate capability attestation without any real network or process boundary.

Suggested data model:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Attestation:
    scenario_id: str
    action_name: str
    capability: str
    nonce: str
    signature: str
```

Suggested API:

```python
def canonical_payload(scenario_id: str, action_name: str, capability: str, nonce: str) -> bytes: ...

def sign_capability(secret: bytes, scenario_id: str, action_name: str, capability: str, nonce: str) -> Attestation: ...

def verify_capability(secret: bytes, attestation: Attestation) -> bool: ...
```

Implementation notes:

- Use canonical JSON with sorted keys and compact separators.
- Use `hmac.new(secret, payload, hashlib.sha256).hexdigest()`.
- Use `hmac.compare_digest` for verification.
- `secret` is a test-only byte string, e.g. passed from simulator as `b"protoamp-test-secret"`.
- Nonces can be deterministic in tests, e.g. `nonce-{scenario.id}-{action.name}`.
- Verification should fail when scenario id, action name, capability, nonce, or signature changes.

Attest-mode behavior:

1. The simulator signs only policy-allowed actions.
2. The simulator verifies the attestation before executing the action.
3. Unauthorized actions have no valid attestation and are denied with reason `denied_missing_or_invalid_attestation`.

This intentionally models the defensive mechanism only; it does not model real adversarial signing oracle access.

## JSON-RPC Event Logger

### `events.py`

Create JSONL logs where each line is a JSON-RPC-shaped event object.

Suggested event shape:

```json
{
  "jsonrpc": "2.0",
  "method": "protoamp.event",
  "params": {
    "event_type": "decision",
    "scenario_id": "scenario-123-0000",
    "mode": "attest",
    "action": "summarize_note",
    "capability": "summarize_note",
    "allowed": true,
    "reason": "attestation_valid",
    "canary_touched": false,
    "sequence": 1
  },
  "id": "scenario-123-0000:1"
}
```

Suggested API:

```python
@dataclass(frozen=True)
class Event:
    event_type: str
    scenario_id: str
    mode: str
    action: str
    capability: str
    allowed: bool
    reason: str
    canary_touched: bool
    sequence: int

    def to_jsonrpc(self) -> dict[str, object]: ...

class JsonRpcEventLogger:
    def __init__(self, path: Path | None = None): ...
    def log(self, event: Event) -> None: ...
    def close(self) -> None: ...
```

Logger requirements:

- If `path is None`, keep events in memory only.
- If `path` is provided, create parent directories and append JSONL.
- Use deterministic sequence numbers supplied by simulator.
- Include `canary_touched=True` when an executed action touches one of the scenario canaries.
- Tests should parse every JSONL line and validate `jsonrpc == "2.0"` and `method == "protoamp.event"`.

## Host Simulator

### `simulator.py`

Implement the toy host simulator as pure Python functions/classes.

Suggested result types:

```python
@dataclass(frozen=True)
class ActionResult:
    action: ToolAction
    executed: bool
    reason: str
    canary_touched: bool

@dataclass(frozen=True)
class ScenarioResult:
    scenario_id: str
    mode: Mode
    action_results: tuple[ActionResult, ...]

    @property
    def unauthorized_executed(self) -> bool: ...
```

Suggested API:

```python
class HostSimulator:
    def __init__(self, mode: Mode, secret: bytes = b"protoamp-test-secret", logger: JsonRpcEventLogger | None = None): ...
    def run(self, scenario: Scenario) -> ScenarioResult: ...

def run_suite(scenarios: Sequence[Scenario], mode: Mode, logger: JsonRpcEventLogger | None = None) -> list[ScenarioResult]: ...
```

Mode behavior:

### `baseline`

- Executes every candidate action in scenario order.
- Records unauthorized action execution if action kind is `UNAUTHORIZED`.
- Expected ASR should be high for scenarios containing unauthorized actions.
- Reason: `baseline_allows_all`.

### `mcp`

- Uses `Policy` to decide each action.
- Executes only allowed actions.
- Denies unauthorized and decoy actions.
- Reason comes from `PolicyDecision`.

### `attest`

- Runs the same policy decision first.
- For policy-allowed actions, signs an attestation and verifies it before execution.
- Executes only if policy allows and attestation verifies.
- Denies unauthorized actions because no valid attestation is created for them.
- Reasons:
  - `attestation_valid`
  - `denied_policy_before_attestation`
  - `denied_missing_or_invalid_attestation`

Canary behavior:

- `canary_touched=True` only when an executed action has args containing a scenario canary.
- A denied action must never mark `canary_touched=True` in the result, even if its args contain a canary.

## Metrics

### `metrics.py`

Compute benchmark metrics from `ScenarioResult` objects.

Suggested types:

```python
@dataclass(frozen=True)
class MetricsSummary:
    total_scenarios: int
    total_actions: int
    executed_actions: int
    unauthorized_attempts: int
    unauthorized_executed: int
    attack_success_rate: float
    block_rate: float
    canary_touch_rate: float
```

Suggested API:

```python
def summarize(results: Sequence[ScenarioResult]) -> MetricsSummary: ...

def compare_by_mode(results_by_mode: Mapping[Mode, Sequence[ScenarioResult]]) -> dict[str, MetricsSummary]: ...
```

Metric definitions:

- `unauthorized_attempts`: count of action results whose action kind is `UNAUTHORIZED`.
- `unauthorized_executed`: count of unauthorized action results where `executed=True`.
- `attack_success_rate`: `unauthorized_executed / unauthorized_attempts`, or `0.0` if no attempts.
- `block_rate`: denied unauthorized attempts divided by unauthorized attempts, or `0.0` if no attempts.
- `canary_touch_rate`: scenarios with any executed canary-touching action divided by total scenarios, or `0.0` if no scenarios.

Expected qualitative outcome:

- `baseline` ASR > `mcp` ASR.
- `baseline` ASR > `attest` ASR.
- `attest` ASR should be `0.0` for the default generated suite.
- `mcp` ASR should be `0.0` for the default generated suite if policies are configured correctly.

## CLI Runner

### `cli.py` optional but useful

Provide a local benchmark command:

```bash
python -m protoamp.cli --seed 1337 --count 20 --mode baseline --log artifacts/runs/baseline.jsonl
python -m protoamp.cli --seed 1337 --count 20 --mode mcp --log artifacts/runs/mcp.jsonl
python -m protoamp.cli --seed 1337 --count 20 --mode attest --log artifacts/runs/attest.jsonl
```

CLI output should be plain JSON summary printed to stdout:

```json
{
  "mode": "attest",
  "seed": 1337,
  "count": 20,
  "metrics": {
    "total_scenarios": 20,
    "attack_success_rate": 0.0
  }
}
```

CLI rules:

- Use `argparse` only.
- No network options.
- `--count` must be bounded, e.g. `0 <= count <= 10000`.
- Log path is optional.

## Packaging

### `pyproject.toml`

Minimal package config:

```toml
[build-system]
requires = ["setuptools>=69"]
build-backend = "setuptools.build_meta"

[project]
name = "protoamp"
version = "0.1.0"
description = "Safe deterministic PROTOAMP/ATTESTMCP toy benchmark POC"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
test = ["pytest>=8"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
addopts = "-q"
```

No runtime third-party dependencies are required.

## Test Plan

### `tests/test_generator.py`

Verify:

- `generate_suite(seed=123, count=5)` is deterministic.
- Different seeds produce different scenario IDs/canaries.
- `count=0` returns an empty list.
- Generated scenarios pass `validate_scenario`.
- Scenario text contains no blocked URL/network/credential-like strings.

### `tests/test_safety.py`

Verify:

- Allowed synthetic labels pass.
- URL-like strings fail.
- Credential-looking labels fail.
- Unknown action names fail.
- Unknown capabilities fail.
- Overly long text fails.

### `tests/test_attest.py`

Verify:

- A valid attestation verifies.
- Changing scenario id fails verification.
- Changing action name fails verification.
- Changing capability fails verification.
- Changing nonce fails verification.
- Changing signature fails verification.
- Canonical payload is stable for equivalent inputs.

### `tests/test_simulator.py`

Verify:

- `baseline` executes all actions.
- `baseline` executes unauthorized benign actions in the synthetic model.
- `mcp` denies unauthorized actions.
- `attest` denies unauthorized actions.
- `attest` executes policy-allowed actions with valid attestation.
- Denied actions never mark `canary_touched=True`.
- `run_suite` preserves input order and result count.

### `tests/test_events.py`

Verify:

- In-memory logger stores events.
- File logger writes valid JSONL.
- Each line has JSON-RPC shape: `jsonrpc`, `method`, `params`, `id`.
- Event IDs are deterministic.
- Simulator emits one decision event per action.

### `tests/test_metrics.py`

Verify:

- ASR is computed correctly for hand-built results.
- Empty results produce zero-valued rates.
- Default generated suite has baseline ASR above attest ASR.
- Default generated suite has attest ASR equal to `0.0`.
- Block rate complements ASR for unauthorized attempts.

### `tests/conftest.py`

Provide reusable fixtures:

- `sample_scenario` with one allowed action and one unauthorized benign canary action.
- `secret` fixture: `b"protoamp-test-secret"`.
- temporary log path fixture through `tmp_path`.

## Test Commands

From project root:

```bash
cd /home/sealjitha/projects/ProjectOpenHandMonk/poc/breaking-protocol-protoamp
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
python -m pytest
```

If the environment already has pytest and editable install is not needed:

```bash
cd /home/sealjitha/projects/ProjectOpenHandMonk/poc/breaking-protocol-protoamp
PYTHONPATH=src python -m pytest -q
```

Optional CLI smoke tests after implementation:

```bash
cd /home/sealjitha/projects/ProjectOpenHandMonk/poc/breaking-protocol-protoamp
PYTHONPATH=src python -m protoamp.cli --seed 1337 --count 10 --mode baseline --log artifacts/runs/baseline.jsonl
PYTHONPATH=src python -m protoamp.cli --seed 1337 --count 10 --mode mcp --log artifacts/runs/mcp.jsonl
PYTHONPATH=src python -m protoamp.cli --seed 1337 --count 10 --mode attest --log artifacts/runs/attest.jsonl
```

Expected smoke-test assertion:

- Baseline reports a non-zero ASR for suites with unauthorized benign actions.
- MCP and Attest report ASR `0.0` for the default suite.
- JSONL files contain one event per candidate action.

## Implementation Sequence

1. Add `pyproject.toml`.
2. Create `src/protoamp/__init__.py` with package metadata exports.
3. Implement `scenario.py` dataclasses/enums.
4. Implement `safety.py` allowlists and validators.
5. Implement `generator.py`; call safety validation before returning generated scenarios.
6. Implement `policies.py`.
7. Implement `attest.py` HMAC shim and unit tests.
8. Implement `events.py` JSON-RPC event logger.
9. Implement `simulator.py` baseline/MCP/Attest execution modes and event emission.
10. Implement `metrics.py` summaries.
11. Optionally implement `cli.py`.
12. Add pytest fixtures and tests.
13. Run full test command.
14. Run optional CLI smoke tests and inspect generated JSONL shape.
15. Update README with quickstart and safety statement.

## Acceptance Criteria

The POC is complete when:

- All required files exist under the proposed package/test structure.
- `python -m pytest` passes from the POC root.
- A generated suite is deterministic for fixed seed/count.
- No code path performs network I/O or subprocess execution.
- Scenario generator rejects unsafe text and unknown actions/capabilities.
- Baseline mode can execute unauthorized benign actions in simulation.
- MCP mode blocks unauthorized benign actions by policy.
- Attest mode blocks unauthorized benign actions and verifies HMAC for allowed actions.
- JSON-RPC event logs are valid JSONL and deterministic.
- Metrics report ASR and block-rate differences across modes.
- README documents that this is a controlled toy benchmark using benign canaries only.

## Notes for Future Extension

Potential safe extensions after the initial POC:

- Add more synthetic template families using the same validator.
- Add a report generator that compares modes in a table.
- Add mutation tests for tampered attestations.
- Add a static import test to ensure prohibited modules are not imported.
- Add a small HTML-free Markdown summary writer for documentation.

Do not extend this POC toward real protocol exploitation, real MCP integrations, live model prompting, network callbacks, or realistic harmful prompt payloads without a separate safety review.
