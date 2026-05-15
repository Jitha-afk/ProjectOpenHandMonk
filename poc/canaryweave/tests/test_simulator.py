from canaryweave.events import JsonRpcEventLogger
from canaryweave.scenario import Mode
from canaryweave.simulator import HostSimulator, run_suite


def test_baseline_executes_only_direct_policy_actions(simple_scenario):
    result = HostSimulator(Mode.BASELINE).run(simple_scenario)

    assert [action_result.executed for action_result in result.action_results] == [True, False]
    assert result.unauthorized_executed is False
    assert result.canary_touched is False


def test_mcp_unprotected_executes_all_server_actions(simple_scenario):
    result = HostSimulator(Mode.MCP).run(simple_scenario)

    assert [action_result.executed for action_result in result.action_results] == [True, True]
    assert result.unauthorized_executed is True
    assert result.canary_touched is True
    assert result.action_results[1].reason == "mcp_unprotected_allows_server_action"


def test_attest_executes_only_attested_policy_allowed_action(simple_scenario):
    result = HostSimulator(Mode.ATTEST).run(simple_scenario)

    assert result.action_results[0].executed is True
    assert result.action_results[0].reason == "attestation_valid"
    assert result.action_results[1].executed is False
    assert result.action_results[1].reason == "denied_policy_before_attestation"


def test_run_suite_logs_each_action(simple_scenario, tmp_path):
    log_path = tmp_path / "suite.jsonl"
    logger = JsonRpcEventLogger(log_path)
    results = run_suite([simple_scenario], Mode.MCP, logger=logger)
    logger.close()

    assert len(results) == 1
    assert len(log_path.read_text(encoding="utf-8").splitlines()) == 2
