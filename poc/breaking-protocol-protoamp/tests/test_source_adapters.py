from pathlib import Path

from protoamp.scenario import SourceFamily
from protoamp.source_adapters import (
    load_source_summary,
    summarize_agentdojo,
    summarize_injecagent,
    synthetic_source_summary,
)


def test_synthetic_source_summary_is_safe_and_deterministic():
    first = synthetic_source_summary()
    second = synthetic_source_summary()

    assert first == second
    assert first.source_family is SourceFamily.SYNTHETIC_SAFE
    assert first.digest == "synthetic:default-safe"
    assert first.record_count == 0


def test_missing_source_root_returns_safe_zero_summary(tmp_path):
    summary = summarize_agentdojo(tmp_path / "missing")

    assert summary.source_family is SourceFamily.AGENTDOJO_STRUCTURAL
    assert summary.record_count == 0
    assert summary.digest.startswith("synthetic:missing-")


def test_agentdojo_adapter_returns_counts_hashes_and_no_payload_text():
    root = Path("/tmp/protoamp-source-repos/agentdojo")
    summary = summarize_agentdojo(root)

    assert summary.source_family is SourceFamily.AGENTDOJO_STRUCTURAL
    if root.exists():
        assert summary.record_count > 0
        assert summary.digest.startswith("sha256:")
        assert summary.file_summaries
        assert all(len(file_summary.sha256) == 64 for file_summary in summary.file_summaries)
        assert "class_count" in summary.schema_keys


def test_injecagent_adapter_returns_category_counts_and_no_payload_text():
    root = Path("/tmp/protoamp-source-repos/InjecAgent")
    summary = summarize_injecagent(root)

    assert summary.source_family is SourceFamily.INJECAGENT_STRUCTURAL
    if root.exists():
        assert summary.record_count >= 1054
        assert summary.digest.startswith("sha256:")
        assert "Attack Type" in summary.schema_keys
        assert "Financial Data" in summary.category_counts


def test_source_summary_to_safe_dict_is_json_serializable():
    summary = synthetic_source_summary()
    safe_dict = summary.to_safe_dict()

    assert safe_dict["source_family"] == SourceFamily.SYNTHETIC_SAFE.value
    assert safe_dict["category_counts"] == {"synthetic_safe": 1}


def test_load_source_summary_dispatches_by_family():
    assert load_source_summary(SourceFamily.SYNTHETIC_SAFE).source_family is SourceFamily.SYNTHETIC_SAFE
