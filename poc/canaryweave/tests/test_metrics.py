from canaryweave.generator import generate_suite
from canaryweave.metrics import amplification, compare_by_mode, reduction, summarize
from canaryweave.scenario import Mode
from canaryweave.simulator import run_suite


def test_summarize_baseline_counts_direct_call_policy(simple_scenario):
    results = run_suite([simple_scenario], Mode.BASELINE)
    summary = summarize(results)

    assert summary.total_scenarios == 1
    assert summary.unauthorized_attempts == 1
    assert summary.unauthorized_executed == 0
    assert summary.attack_success_rate == 0.0
    assert summary.canary_touch_rate == 0.0


def test_summarize_attest_blocks_unauthorized_execution(simple_scenario):
    results = run_suite([simple_scenario], Mode.ATTEST)
    summary = summarize(results)

    assert summary.unauthorized_attempts == 1
    assert summary.unauthorized_executed == 0
    assert summary.attack_success_rate == 0.0
    assert summary.block_rate == 1.0
    assert summary.canary_touch_rate == 0.0


def test_compare_by_mode_and_delta_helpers():
    scenarios = generate_suite(42, 4)
    baseline = run_suite(scenarios, Mode.BASELINE)
    mcp = run_suite(scenarios, Mode.MCP)
    attest = run_suite(scenarios, Mode.ATTEST)

    summaries = compare_by_mode({Mode.BASELINE: baseline, Mode.MCP: mcp, Mode.ATTEST: attest})

    assert summaries["baseline"].attack_success_rate == 0.0
    assert summaries["mcp"].attack_success_rate == 1.0
    assert summaries["attest"].attack_success_rate == 0.0
    assert amplification(summaries["mcp"], summaries["baseline"]) == 1.0
    assert reduction(summaries["attest"], summaries["mcp"]) == 1.0
