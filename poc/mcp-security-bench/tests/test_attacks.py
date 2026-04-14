"""
Test suite for MCP Security Benchmark attacks.

Tests are organized in two tiers:
  1. Unit tests — validate scenario loading, scoring, and report generation
     (run without a server).
  2. Integration tests — run actual attack scenarios against a live evil
     MCP server (require @pytest.mark.requires_server).

Run all unit tests:
    pytest tests/test_attacks.py -m "not requires_server"

Run integration tests (server must be running):
    pytest tests/test_attacks.py -m requires_server
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from bench.harness import MCPBenchHarness, Scenario, ScenarioResult
from bench.evaluator import (
    BenchmarkEvaluator,
    SCORE_ATTACK_SUCCESS,
    SCORE_ATTACK_FAIL,
    SCORE_DETECTED,
    SCORE_PROTECTED,
)


# ===================================================================
# Tier 1: Unit Tests — no server required
# ===================================================================


class TestScenarioLoading:
    """Verify YAML scenario files load correctly."""

    def test_scenarios_directory_exists(self, scenarios_dir: Path):
        assert scenarios_dir.exists(), f"Scenarios dir not found: {scenarios_dir}"

    def test_all_yaml_files_loadable(self, all_scenario_files: list[Path]):
        """Every YAML file in scenarios/ must parse without error."""
        assert len(all_scenario_files) > 0, "No YAML scenario files found"
        for yaml_file in all_scenario_files:
            import yaml
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
            assert "attack_category" in data, f"{yaml_file.name}: missing attack_category"
            assert "scenarios" in data, f"{yaml_file.name}: missing scenarios list"
            assert len(data["scenarios"]) > 0, f"{yaml_file.name}: empty scenarios list"

    def test_scenario_required_fields(self, all_scenarios: list[Scenario]):
        """Every scenario must have required fields populated."""
        for s in all_scenarios:
            assert s.id, f"Scenario missing id: {s}"
            assert s.name, f"Scenario {s.id} missing name"
            assert s.description, f"Scenario {s.id} missing description"
            assert s.prompt, f"Scenario {s.id} missing prompt"
            assert s.attack_category, f"Scenario {s.id} missing attack_category"
            assert s.severity in ("low", "medium", "high", "critical"), (
                f"Scenario {s.id} has invalid severity: {s.severity}"
            )
            assert s.iterations > 0, f"Scenario {s.id} has non-positive iterations"

    def test_scenario_ids_unique(self, all_scenarios: list[Scenario]):
        """All scenario IDs must be unique."""
        ids = [s.id for s in all_scenarios]
        assert len(ids) == len(set(ids)), f"Duplicate scenario IDs: {ids}"

    def test_all_attack_categories_covered(self, all_scenarios: list[Scenario]):
        """All 11 attack categories should have at least one scenario."""
        expected_categories = {
            "tool_poisoning",
            "tool_shadowing",
            "rug_pull",
            "data_exfiltration",
            "prompt_injection",
            "credential_theft",
            "excessive_permissions",
            "code_execution",
            "command_injection",
            "sandbox_escape",
            "cross_server_attack",
        }
        found_categories = {s.attack_category for s in all_scenarios}
        missing = expected_categories - found_categories
        assert not missing, f"Missing attack categories: {missing}"

    def test_detection_indicators_present(self, all_scenarios: list[Scenario]):
        """Every scenario should have at least one detection indicator."""
        for s in all_scenarios:
            assert len(s.detection_indicators) > 0, (
                f"Scenario {s.id} has no detection indicators"
            )


class TestHarnessUnit:
    """Unit tests for MCPBenchHarness (no server connection)."""

    def test_harness_creation(self, harness: MCPBenchHarness):
        assert harness is not None
        assert not harness.connected

    def test_harness_load_scenarios(self, harness: MCPBenchHarness):
        scenarios = harness.load_all_scenarios()
        assert len(scenarios) > 0
        assert all(isinstance(s, Scenario) for s in scenarios)

    def test_harness_load_single_file(
        self, harness: MCPBenchHarness, scenarios_dir: Path
    ):
        yaml_file = scenarios_dir / "tool_poisoning.yaml"
        scenarios = harness.load_scenario(yaml_file)
        assert len(scenarios) >= 1
        assert all(s.attack_category == "tool_poisoning" for s in scenarios)

    @pytest.mark.asyncio
    async def test_harness_dry_run(self, harness: MCPBenchHarness):
        """Harness should execute in dry-run mode without server."""
        scenarios = harness.load_all_scenarios()
        scenario = scenarios[0]
        # Override iterations for fast test
        scenario.iterations = 1

        results = await harness.run_scenario(scenario)
        assert len(results) == 1
        assert results[0].error == "dry_run"

    @pytest.mark.asyncio
    async def test_list_tools_without_connection(self, harness: MCPBenchHarness):
        tools = await harness.list_tools()
        assert tools == []

    @pytest.mark.asyncio
    async def test_list_resources_without_connection(self, harness: MCPBenchHarness):
        resources = await harness.list_resources()
        assert resources == []


class TestEvaluatorUnit:
    """Unit tests for BenchmarkEvaluator."""

    def test_score_attack_success(self, evaluator: BenchmarkEvaluator):
        result = ScenarioResult(
            scenario_id="test-001",
            scenario_name="Test",
            attack_category="test",
            severity="high",
            prompt="test",
            target_tool="test",
            iteration=1,
            total_iterations=1,
            attack_succeeded=True,
        )
        scored = evaluator.score_result(result)
        assert scored.score == SCORE_ATTACK_SUCCESS
        assert scored.score_label == "attack_success"

    def test_score_attack_fail(self, evaluator: BenchmarkEvaluator):
        result = ScenarioResult(
            scenario_id="test-002",
            scenario_name="Test",
            attack_category="test",
            severity="medium",
            prompt="test",
            target_tool="test",
            iteration=1,
            total_iterations=1,
            attack_succeeded=False,
            attack_detected=False,
        )
        scored = evaluator.score_result(result)
        assert scored.score == SCORE_ATTACK_FAIL
        assert scored.score_label == "attack_fail"

    def test_score_detected(self, evaluator: BenchmarkEvaluator):
        result = ScenarioResult(
            scenario_id="test-003",
            scenario_name="Test",
            attack_category="test",
            severity="high",
            prompt="test",
            target_tool="test",
            iteration=1,
            total_iterations=1,
            attack_detected=True,
        )
        scored = evaluator.score_result(result)
        assert scored.score == SCORE_DETECTED
        assert scored.score_label == "detected"

    def test_score_protected(self, evaluator_with_protection: BenchmarkEvaluator):
        result = ScenarioResult(
            scenario_id="test-004",
            scenario_name="Test",
            attack_category="test",
            severity="critical",
            prompt="test",
            target_tool="test",
            iteration=1,
            total_iterations=1,
            attack_blocked=True,
        )
        scored = evaluator_with_protection.score_result(result)
        assert scored.score == SCORE_PROTECTED
        assert scored.score_label == "protected"

    def test_detection_overrides_success(self, evaluator: BenchmarkEvaluator):
        """If both succeeded and detected, detected should win."""
        result = ScenarioResult(
            scenario_id="test-005",
            scenario_name="Test",
            attack_category="test",
            severity="high",
            prompt="test",
            target_tool="test",
            iteration=1,
            total_iterations=1,
            attack_succeeded=True,
            attack_detected=True,
        )
        scored = evaluator.score_result(result)
        assert scored.score == SCORE_DETECTED

    def test_compute_metrics(
        self,
        evaluator: BenchmarkEvaluator,
        sample_results: list[ScenarioResult],
    ):
        metrics = evaluator.compute_metrics(sample_results)
        assert "tool_poisoning" in metrics
        assert "data_exfiltration" in metrics

        tp = metrics["tool_poisoning"]
        assert tp.total == 2
        assert tp.attack_success == 1
        assert tp.detected == 1

    def test_generate_report(
        self,
        evaluator: BenchmarkEvaluator,
        sample_results: list[ScenarioResult],
    ):
        report = evaluator.generate_report(sample_results)
        assert report.total_iterations == 3
        assert report.total_scenarios == 2  # tp-001 and de-001
        assert 0.0 <= report.overall_asr <= 1.0
        assert 0.0 <= report.overall_rr <= 1.0

    def test_report_text_output(
        self,
        evaluator: BenchmarkEvaluator,
        sample_results: list[ScenarioResult],
    ):
        report = evaluator.generate_report(sample_results)
        text = report.to_text()
        assert "MCP SECURITY BENCHMARK REPORT" in text
        assert "Attack Success Rate" in text

    def test_report_json_output(
        self,
        evaluator: BenchmarkEvaluator,
        sample_results: list[ScenarioResult],
    ):
        report = evaluator.generate_report(sample_results)
        import json
        data = json.loads(report.to_json())
        assert "overall_metrics" in data
        assert "categories" in data
        assert "timestamp" in data

    def test_score_from_dict(self, evaluator: BenchmarkEvaluator):
        """Evaluator should accept dict input as well as dataclass."""
        result_dict = {
            "scenario_id": "dict-001",
            "scenario_name": "Dict Test",
            "attack_category": "test",
            "severity": "low",
            "iteration": 1,
            "duration": 0.5,
            "attack_succeeded": True,
            "attack_detected": False,
            "attack_blocked": False,
        }
        scored = evaluator.score_result(result_dict)
        assert scored.score == SCORE_ATTACK_SUCCESS

    def test_asr_calculation(self):
        """Verify ASR = successes / (total - errors)."""
        from bench.evaluator import CategoryMetrics
        m = CategoryMetrics(
            category="test",
            total=10,
            attack_success=3,
            attack_fail=4,
            detected=2,
            protected=0,
            errors=1,
        )
        assert abs(m.asr - 3 / 9) < 1e-9
        assert abs(m.rr - 2 / 9) < 1e-9

    def test_empty_results(self, evaluator: BenchmarkEvaluator):
        """Evaluator should handle empty results gracefully."""
        report = evaluator.generate_report([])
        assert report.total_iterations == 0
        assert report.overall_asr == 0.0


# ===================================================================
# Tier 2: Integration Tests — require running evil MCP server
# ===================================================================


ATTACK_CATEGORIES = [
    "tool_poisoning",
    "tool_shadowing",
    "rug_pull",
    "data_exfiltration",
    "prompt_injection",
    "credential_theft",
    "excessive_permissions",
    "code_execution",
    "command_injection",
    "sandbox_escape",
    "cross_server_attack",
]


@pytest.mark.requires_server
@pytest.mark.benchmark
class TestLiveAttacks:
    """Integration tests that run against a live evil MCP server."""

    @pytest.fixture(autouse=True)
    def _skip_if_no_server(self):
        from tests.conftest import _server_available
        if not _server_available():
            pytest.skip("Evil MCP server not available")

    @pytest.mark.asyncio
    async def test_server_connection(self, harness: MCPBenchHarness):
        """Verify we can connect to the evil MCP server."""
        await harness.connect()
        assert harness.connected
        tools = await harness.list_tools()
        assert len(tools) > 0
        await harness.disconnect()

    @pytest.mark.asyncio
    async def test_tool_enumeration(self, harness: MCPBenchHarness):
        """List all attack tools from the evil server."""
        await harness.connect()
        tools = await harness.list_tools()
        resources = await harness.list_resources()
        assert len(tools) > 0, "Evil server should expose at least one tool"
        await harness.disconnect()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("category", ATTACK_CATEGORIES)
    @pytest.mark.attack(category="parametrized")
    async def test_attack_category(
        self,
        harness: MCPBenchHarness,
        scenario_by_category: Any,
        evaluator: BenchmarkEvaluator,
        category: str,
    ):
        """Run all scenarios for a given attack category."""
        scenarios = scenario_by_category(category)
        if not scenarios:
            pytest.skip(f"No scenarios for category: {category}")

        await harness.connect()
        all_results = []

        for scenario in scenarios:
            # Reduce iterations for CI
            scenario.iterations = 3
            results = await harness.run_scenario(scenario)
            all_results.extend(results)

        await harness.disconnect()

        # Evaluate
        report = evaluator.generate_report(all_results)
        assert report.total_iterations > 0
        # Log the results (visible in pytest output with -v)
        print(f"\n{category}: ASR={report.overall_asr:.2%} RR={report.overall_rr:.2%}")

    @pytest.mark.asyncio
    async def test_full_benchmark_run(
        self,
        harness: MCPBenchHarness,
        evaluator: BenchmarkEvaluator,
    ):
        """Run the complete benchmark suite."""
        await harness.connect()
        results = await harness.run_all()
        await harness.disconnect()

        report = evaluator.generate_report(results)
        print("\n" + report.to_text())
        assert report.total_iterations > 0


@pytest.mark.requires_server
@pytest.mark.requires_docker
@pytest.mark.benchmark
class TestSandboxAttacks:
    """Tests that require Docker for sandbox escape scenarios."""

    @pytest.fixture(autouse=True)
    def _skip_if_no_docker(self):
        import shutil
        if not shutil.which("docker"):
            pytest.skip("Docker not available")

    @pytest.mark.asyncio
    async def test_container_escape_scenario(
        self,
        harness: MCPBenchHarness,
        load_scenario: Any,
        evaluator: BenchmarkEvaluator,
    ):
        scenario = load_scenario("se-001")
        if not scenario:
            pytest.skip("Scenario se-001 not found")

        scenario.iterations = 3
        await harness.connect()
        results = await harness.run_scenario(scenario)
        await harness.disconnect()

        for r in results:
            scored = evaluator.score_result(r)
            assert scored.score in (
                SCORE_ATTACK_SUCCESS,
                SCORE_ATTACK_FAIL,
                SCORE_DETECTED,
                SCORE_PROTECTED,
            )
