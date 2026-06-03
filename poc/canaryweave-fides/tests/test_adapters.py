from __future__ import annotations

import hashlib
import json

from canaryweave_fides.adapters import (
    AdapterConfig,
    AgentDefenseBenchAdapter,
    ASBAdapter,
    SyntheticAdapter,
    create_adapter,
    get_adapter_class,
    registered_adapters,
)
from canaryweave_fides.adapters.base import AdapterStatus
from canaryweave_fides.cases import AttackCase


def test_adapter_registry_exposes_expected_adapters():
    names = registered_adapters()

    assert names == ("agentdefensebench", "asb", "synthetic")
    assert get_adapter_class("synthetic") is SyntheticAdapter
    assert get_adapter_class("asb") is ASBAdapter
    assert get_adapter_class("agentdefensebench") is AgentDefenseBenchAdapter
    assert isinstance(create_adapter("synthetic"), SyntheticAdapter)


def test_synthetic_adapter_returns_public_safe_attack_cases():
    result = SyntheticAdapter().load()

    assert result.status is AdapterStatus.LOADED
    assert len(result.cases) >= 4
    assert all(isinstance(case, AttackCase) for case in result.cases)
    assert {case.dataset_id for case in result.cases} == {"synthetic"}
    assert {case.split for case in result.cases} == {"ci"}
    assert {case.case_kind.value for case in result.cases} >= {"attack", "benign"}

    public_blob = json.dumps([case.to_dict() for case in result.cases], sort_keys=True)
    assert "raw_ref" not in public_blob
    assert "private_data" not in public_blob
    assert "local-only" not in public_blob


def test_asb_adapter_maps_tiny_synthetic_fixture_to_safe_features_only(tmp_path):
    fixture_text = "fixture structural sample with tool shaped markers"
    fixture_path = tmp_path / "records.jsonl"
    fixture_record = {
        "id": "fixture-record-001",
        "split": "dev",
        "label": "attack",
        "category": "tool_misuse",
        "surface": "api_message",
        "payload": fixture_text,
        "metadata": {"origin": "synthetic-fixture"},
    }
    fixture_path.write_text(json.dumps(fixture_record) + "\n", encoding="utf-8")

    result = ASBAdapter(AdapterConfig(root=tmp_path, split="dev")).load()

    assert result.status is AdapterStatus.LOADED
    assert len(result.cases) == 1
    case = result.cases[0]
    assert isinstance(case, AttackCase)
    assert case.dataset_id == "asb"
    assert case.split == "dev"
    assert case.attack_category == "tool_misuse"
    assert case.surface == "api_message"
    assert case.raw_ref is not None

    safe = case.safe_features
    assert safe["length"] == len(fixture_text)
    assert safe["sha256"] == "sha256:" + hashlib.sha256(fixture_text.encode("utf-8")).hexdigest()
    assert safe["schema_shape"] == "json_object"
    assert safe["source_format"] == "jsonl"
    assert safe["payload_field_count"] == 1
    assert "payload" in safe["payload_field_paths"]

    public_blob = json.dumps(case.to_dict(), sort_keys=True)
    assert fixture_text not in public_blob
    assert "fixture-record-001" not in public_blob
    assert "raw_ref" not in public_blob
    assert "private_data" not in public_blob


def test_agentdefensebench_adapter_auto_skips_missing_path(tmp_path):
    missing_root = tmp_path / "absent-agentdefensebench"

    result = AgentDefenseBenchAdapter(AdapterConfig(root=missing_root)).load()

    assert result.status is AdapterStatus.SKIPPED_MISSING_LOCAL_PATH
    assert result.cases == ()
    assert result.dataset_id == "agentdefensebench"
    assert "missing" in result.message.lower()
