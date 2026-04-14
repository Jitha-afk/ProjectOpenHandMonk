"""
Pytest configuration and fixtures for MCP Security Benchmark tests.

Provides:
  - MCPBenchHarness instance fixture
  - Scenario loading fixtures
  - BenchmarkEvaluator instance fixture
  - Custom marks for benchmark and attack category tests
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bench.harness import MCPBenchHarness, Scenario, ScenarioResult
from bench.evaluator import BenchmarkEvaluator

SCENARIOS_DIR = Path(__file__).parent.parent / "src" / "bench" / "scenarios"

# ---------------------------------------------------------------------------
# Custom markers
# ---------------------------------------------------------------------------

def pytest_configure(config: Any) -> None:
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "benchmark: mark test as a benchmark test"
    )
    config.addinivalue_line(
        "markers",
        "attack(category): mark test with an attack category "
        "(e.g., @pytest.mark.attack(category='tool_poisoning'))",
    )
    config.addinivalue_line(
        "markers", "requires_server: test requires a running evil MCP server"
    )
    config.addinivalue_line(
        "markers", "requires_docker: test requires Docker"
    )
    config.addinivalue_line(
        "markers", "requires_network: test requires network access"
    )


# ---------------------------------------------------------------------------
# Server availability check
# ---------------------------------------------------------------------------

def _server_available() -> bool:
    """Check if the evil MCP server is reachable."""
    url = os.environ.get("MCP_SERVER_URL", "http://localhost:9000")
    try:
        import urllib.request
        req = urllib.request.Request(url, method="HEAD")
        urllib.request.urlopen(req, timeout=2)
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def server_url() -> str:
    """MCP evil server URL (configurable via MCP_SERVER_URL env var)."""
    return os.environ.get("MCP_SERVER_URL", "http://localhost:9000")


@pytest.fixture(scope="session")
def scenarios_dir() -> Path:
    """Path to the YAML scenarios directory."""
    return SCENARIOS_DIR


@pytest.fixture
def harness(server_url: str) -> MCPBenchHarness:
    """Create an MCPBenchHarness instance (not connected)."""
    return MCPBenchHarness(
        server_url=server_url,
        scenarios_dir=SCENARIOS_DIR,
    )


@pytest.fixture
def evaluator() -> BenchmarkEvaluator:
    """Create a BenchmarkEvaluator instance."""
    return BenchmarkEvaluator()


@pytest.fixture
def evaluator_with_protection() -> BenchmarkEvaluator:
    """Create a BenchmarkEvaluator with security product scoring."""
    return BenchmarkEvaluator(security_product_active=True)


@pytest.fixture(scope="session")
def all_scenario_files(scenarios_dir: Path) -> list[Path]:
    """List all YAML scenario files."""
    return sorted(scenarios_dir.glob("*.yaml"))


@pytest.fixture(scope="session")
def all_scenarios(all_scenario_files: list[Path]) -> list[Scenario]:
    """Load all scenarios from YAML files."""
    scenarios = []
    for yaml_file in all_scenario_files:
        with open(yaml_file) as f:
            data = yaml.safe_load(f)
        category = data.get("attack_category", "unknown")
        for s in data.get("scenarios", []):
            scenarios.append(Scenario.from_dict(s, category))
    return scenarios


@pytest.fixture
def scenario_by_category(all_scenarios: list[Scenario]):
    """Return a function that filters scenarios by attack category."""
    def _filter(category: str) -> list[Scenario]:
        return [s for s in all_scenarios if s.attack_category == category]
    return _filter


def _load_scenario_ids() -> list[str]:
    """Load all scenario IDs for parametrization (called at collection time)."""
    ids = []
    if SCENARIOS_DIR.exists():
        for yaml_file in sorted(SCENARIOS_DIR.glob("*.yaml")):
            try:
                with open(yaml_file) as f:
                    data = yaml.safe_load(f)
                for s in data.get("scenarios", []):
                    ids.append(s["id"])
            except Exception:
                pass
    return ids


def _load_scenario_by_id(scenario_id: str) -> Scenario | None:
    """Load a specific scenario by ID."""
    for yaml_file in sorted(SCENARIOS_DIR.glob("*.yaml")):
        try:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
            category = data.get("attack_category", "unknown")
            for s in data.get("scenarios", []):
                if s["id"] == scenario_id:
                    return Scenario.from_dict(s, category)
        except Exception:
            pass
    return None


@pytest.fixture
def load_scenario():
    """Return a function that loads a scenario by ID."""
    return _load_scenario_by_id


@pytest.fixture
def sample_results() -> list[ScenarioResult]:
    """Provide sample ScenarioResult objects for evaluator testing."""
    return [
        ScenarioResult(
            scenario_id="tp-001",
            scenario_name="Hidden instructions",
            attack_category="tool_poisoning",
            severity="high",
            prompt="test prompt",
            target_tool="fetch_data",
            iteration=1,
            total_iterations=1,
            attack_succeeded=True,
            detection_indicators_found=["credentials", "admin"],
        ),
        ScenarioResult(
            scenario_id="tp-001",
            scenario_name="Hidden instructions",
            attack_category="tool_poisoning",
            severity="high",
            prompt="test prompt",
            target_tool="fetch_data",
            iteration=2,
            total_iterations=2,
            attack_detected=True,
        ),
        ScenarioResult(
            scenario_id="de-001",
            scenario_name="Data exfil",
            attack_category="data_exfiltration",
            severity="critical",
            prompt="test prompt",
            target_tool="summarize",
            iteration=1,
            total_iterations=1,
            attack_succeeded=True,
        ),
    ]
