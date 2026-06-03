from __future__ import annotations

import json

from canaryweave_fides.adapters import ASBAdapter, AdapterConfig
from canaryweave_fides.adapters.base import AdapterStatus
from canaryweave_fides.decisions import Decision, StackName
from canaryweave_fides.facts import NormalizedFacts
from canaryweave_fides.gate import evaluate_stack
from canaryweave_fides.reporting import build_public_report


def _load_asb_case(tmp_path, *, text: str, label: str = "attack", category: str = "dataset_native", surface: str = "api_message"):
    path = tmp_path / "records.jsonl"
    record = {
        "id": "local-fixture-001",
        "split": "dev",
        "label": label,
        "category": category,
        "surface": surface,
        "payload": text,
    }
    path.write_text(json.dumps(record) + "\n", encoding="utf-8")
    result = ASBAdapter(AdapterConfig(root=tmp_path, split="dev")).load()
    assert result.status is AdapterStatus.LOADED
    assert len(result.cases) == 1
    return result.cases[0]


def test_asb_adapter_attaches_public_safe_expected_rule_metadata(tmp_path):
    case = _load_asb_case(tmp_path, text="structural shell execution capability")

    assert case.attack_category == "mcp_execution/command_or_code_execution_request"
    assert case.ground_truth is not None
    assert case.ground_truth.expected_rule_ids == ("cwfr-0106",)
    assert case.ground_truth.labels["required_fields"] == [
        "features.command_execution_shape",
        "requested.capability",
    ]

    public_blob = json.dumps(case.to_dict(), sort_keys=True)
    assert "structural request" not in public_blob
    assert "local-fixture-001" not in public_blob
    assert "raw_ref" not in public_blob
    assert "private_data" not in public_blob
    assert "expected_rule_ids" in public_blob
    assert "required_fields" in public_blob


def test_asb_instruction_shape_can_reach_existing_instruction_rule(tmp_path):
    case = _load_asb_case(tmp_path, text="policy instruction hierarchy override structure")
    facts = NormalizedFacts.from_attack_case(case)

    assert case.attack_category == "mcp_prompt_boundary/instruction_hierarchy_violation"
    assert case.ground_truth is not None
    assert case.ground_truth.expected_rule_ids == ("cwfr-0003",)
    assert facts.origin_labels[0] in {"resource_content", "tool_output", "server_manifest", "server_sampling"}

    decision = evaluate_stack(facts, StackName.YARA_RULES)

    assert decision.decision is Decision.QUARANTINE
    assert "cwfr-0003" in decision.rule_ids


def test_asb_adapter_prioritizes_specific_secret_evidence_over_generic_api_terms(tmp_path):
    case = _load_asb_case(tmp_path, text="credential exposure api key structure")

    assert case.attack_category == "mcp_data_flow/credential_or_secret_exposure"
    assert case.ground_truth is not None
    assert case.ground_truth.expected_rule_ids == ("cwfr-0104",)


def test_asb_adapter_does_not_map_generic_request_text_to_network_evidence(tmp_path):
    case = _load_asb_case(tmp_path, text="benign structural request metadata", label="attack")

    assert case.safe_features["network_request_shape"] is False
    assert case.attack_category == "dataset_native"
    assert case.ground_truth is not None
    assert case.ground_truth.expected_rule_ids == ()


def test_asb_adapter_does_not_attach_credential_rule_to_exfiltration_only_shape(tmp_path):
    case = _load_asb_case(tmp_path, text="external upload structure", label="attack")

    assert case.safe_features["exfiltration_shape"] is True
    assert case.safe_features["credential_or_secret_shape"] is False
    assert case.ground_truth is not None
    assert case.ground_truth.expected_rule_ids == ()
    assert "required_fields" not in case.ground_truth.labels


def test_public_report_includes_expected_rule_evidence_without_case_rows():
    raw = {
        "schema_version": "canaryweave_fides.gate_eval.v1",
        "iterations": 1,
        "total_cases": 3,
        "total_iterations": 3,
        "provider_calls": 0,
        "case_results": [
            {
                "case_id": "mapped.hit",
                "dataset_id": "asb",
                "case_kind": "attack",
                "attack_category": "mcp_execution/command_or_code_execution_request",
                "surface": "api_message",
                "iteration": 0,
                "ground_truth": {"expected_rule_ids": ["cwfr-0106"], "labels": {"required_fields": []}},
                "safe_features": {"command_execution_shape": True, "requested_capability": "execute_code"},
                "policy_context": {},
                "decisions": [{"stack": "yara_rules", "decision": "block", "rule_ids": ["cwfr-0106"]}],
            },
            {
                "case_id": "mapped.miss",
                "dataset_id": "asb",
                "case_kind": "attack",
                "attack_category": "mcp_network/unapproved_network_request",
                "surface": "api_message",
                "iteration": 0,
                "ground_truth": {"expected_rule_ids": ["cwfr-0107"], "labels": {"required_fields": []}},
                "safe_features": {"network_request_shape": True},
                "policy_context": {},
                "decisions": [{"stack": "yara_rules", "decision": "allow", "rule_ids": []}],
            },
            {
                "case_id": "unmapped",
                "dataset_id": "asb",
                "case_kind": "attack",
                "attack_category": "dataset_native",
                "surface": "api_message",
                "iteration": 0,
                "ground_truth": {"expected_rule_ids": [], "labels": {}},
                "safe_features": {},
                "policy_context": {},
                "decisions": [{"stack": "yara_rules", "decision": "allow", "rule_ids": []}],
            },
        ],
    }

    report = build_public_report(raw)
    evidence = report["expected_rule_evidence"]

    assert evidence["available"] is True
    assert evidence["cases_with_expected_rules"] == 2
    assert evidence["expected_rule_hits"] == 1
    assert evidence["expected_rule_misses"] == 1
    assert evidence["expected_rule_hit_rate"] == 0.5
    assert evidence["by_dataset"]["asb"]["cases_with_expected_rules"] == 2
    assert evidence["by_category"]["mcp_network/unapproved_network_request"]["expected_rule_misses"] == 1
    assert evidence["case_level_rows_included"] is False
    assert "mapped.hit" not in str(evidence)


def test_public_report_filters_non_public_expected_rule_ids():
    raw = {
        "schema_version": "canaryweave_fides.gate_eval.v1",
        "iterations": 1,
        "total_cases": 1,
        "total_iterations": 1,
        "provider_calls": 0,
        "case_results": [
            {
                "case_id": "mapped.hit",
                "dataset_id": "asb",
                "case_kind": "attack",
                "attack_category": "mcp_execution/command_or_code_execution_request",
                "surface": "api_message",
                "iteration": 0,
                "ground_truth": {"expected_rule_ids": ["cwfr-0106", "native-private-rule"], "labels": {}},
                "safe_features": {"command_execution_shape": True},
                "policy_context": {},
                "decisions": [{"stack": "yara_rules", "decision": "block", "rule_ids": ["cwfr-0106"]}],
            },
        ],
    }

    evidence = build_public_report(raw)["expected_rule_evidence"]

    assert evidence["unique_expected_rule_ids"] == ["cwfr-0106"]
    assert "native-private-rule" not in str(evidence)


def test_public_report_includes_safe_fact_completeness_without_case_rows():
    raw = {
        "schema_version": "canaryweave_fides.gate_eval.v1",
        "iterations": 1,
        "total_cases": 2,
        "total_iterations": 2,
        "provider_calls": 0,
        "case_results": [
            {
                "case_id": "facts.one",
                "dataset_id": "asb",
                "case_kind": "attack",
                "attack_category": "mcp_execution/command_or_code_execution_request",
                "surface": "api_message",
                "iteration": 0,
                "safe_features": {
                    "command_execution_shape": True,
                    "credential_or_secret_shape": True,
                    "exfiltration_shape": True,
                    "tool_plan_shape": True,
                    "requested_capability": "execute_code",
                    "requested_sink": "external_sink",
                },
                "policy_context": {},
                "ground_truth": {"expected_rule_ids": ["cwfr-0106"], "labels": {}},
                "decisions": [],
            },
            {
                "case_id": "facts.two",
                "dataset_id": "asb",
                "case_kind": "attack",
                "attack_category": "dataset_native",
                "surface": "api_message",
                "safe_features": {},
                "policy_context": {},
                "ground_truth": {"expected_rule_ids": [], "labels": {}},
                "decisions": [],
            },
        ],
    }

    report = build_public_report(raw)
    completeness = report["safe_fact_completeness"]
    asb = completeness["by_dataset"]["asb"]

    assert asb["total_cases"] == 2
    assert asb["command_execution_shape_count"] == 1
    assert asb["command_execution_shape_ratio"] == 0.5
    assert asb["credential_or_secret_shape_count"] == 1
    assert asb["exfiltration_shape_count"] == 1
    assert asb["tool_plan_shape_count"] == 1
    assert asb["requested_capability_present_count"] == 1
    assert asb["requested_sink_present_count"] == 1
    assert asb["mapped_category_count"] == 1
    assert asb["dataset_native_fallback_count"] == 1
    assert completeness["case_level_rows_included"] is False
    assert "facts.one" not in str(completeness)
