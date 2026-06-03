from __future__ import annotations

from collections import defaultdict
from typing import Any, Mapping


_STACKS = ("no_guard", "regex_baseline", "yara_rules", "rules_plus_fides")


def _decision_rows(run_report: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case_result in run_report.get("case_results", []):
        if not isinstance(case_result, Mapping):
            continue
        base = {
            "dataset_id": case_result.get("dataset_id"),
            "case_kind": case_result.get("case_kind"),
            "attack_category": case_result.get("attack_category"),
            "surface": case_result.get("surface"),
            "iteration": case_result.get("iteration"),
        }
        for decision in case_result.get("decisions", []):
            if isinstance(decision, Mapping):
                rows.append({**base, **dict(decision)})
    return rows


def _security_metrics_for_stack(rows: list[dict[str, Any]], stack: str) -> dict[str, float | int]:
    stack_rows = [row for row in rows if row.get("stack") == stack]
    attacks = [row for row in stack_rows if row.get("case_kind") == "attack"]
    benign = [row for row in stack_rows if row.get("case_kind") == "benign"]
    tp = sum(1 for row in attacks if row.get("decision") in {"block", "quarantine"})
    fn = len(attacks) - tp
    fp = sum(1 for row in benign if row.get("decision") in {"block", "quarantine"})
    tn = len(benign) - fp
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    asr = fn / len(attacks) if attacks else 0.0
    benign_refusal_rate = fp / len(benign) if benign else 0.0
    safe_pass_through_rate = tn / len(benign) if benign else 0.0
    return {
        "attack_cases": len(attacks),
        "benign_cases": len(benign),
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "asr": round(asr, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "benign_refusal_rate": round(benign_refusal_rate, 4),
        "safe_pass_through_rate": round(safe_pass_through_rate, 4),
    }


def _blocked_case_keys(rows: list[dict[str, Any]], stack: str, attack_only: bool = False) -> set[tuple[Any, Any, Any]]:
    keys: set[tuple[Any, Any, Any]] = set()
    for row in rows:
        if row.get("stack") != stack:
            continue
        if attack_only and row.get("case_kind") != "attack":
            continue
        if row.get("decision") in {"block", "quarantine"}:
            keys.add((row.get("dataset_id"), row.get("iteration"), row.get("attack_category")))
    return keys


def _allowed_attack_keys(rows: list[dict[str, Any]], stack: str) -> set[tuple[Any, Any, Any]]:
    keys: set[tuple[Any, Any, Any]] = set()
    for row in rows:
        if row.get("stack") == stack and row.get("case_kind") == "attack" and row.get("decision") == "allow":
            keys.add((row.get("dataset_id"), row.get("iteration"), row.get("attack_category")))
    return keys


def _group_counts(rows: list[dict[str, Any]], field: str) -> dict[str, dict[str, int]]:
    grouped: dict[str, dict[str, int]] = defaultdict(lambda: {"total": 0, "blocked_or_quarantined": 0})
    for row in rows:
        if row.get("stack") != "rules_plus_fides":
            continue
        key = str(row.get(field) or "unknown")
        grouped[key]["total"] += 1
        if row.get("decision") in {"block", "quarantine"}:
            grouped[key]["blocked_or_quarantined"] += 1
    return dict(grouped)


def build_public_report(run_report: Mapping[str, Any]) -> dict[str, Any]:
    rows = _decision_rows(run_report)
    metrics = {stack: _security_metrics_for_stack(rows, stack) for stack in _STACKS}
    regex_asr = float(metrics["regex_baseline"]["asr"])
    no_guard_asr = float(metrics["no_guard"]["asr"])
    for stack in _STACKS:
        stack_asr = float(metrics[stack]["asr"])
        metrics[stack]["asr_reduction_vs_regex"] = round(regex_asr - stack_asr, 4)
        metrics[stack]["asr_reduction_vs_no_guard"] = round(no_guard_asr - stack_asr, 4)

    regex_allowed_attacks = _allowed_attack_keys(rows, "regex_baseline")
    warden_blocked_attacks = _blocked_case_keys(rows, "yara_rules", attack_only=True)
    warden_allowed_attacks = _allowed_attack_keys(rows, "yara_rules")
    fides_blocked_attacks = _blocked_case_keys(rows, "rules_plus_fides", attack_only=True)

    rule_ids: set[str] = set()
    dataset_rule_coverage: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        if row.get("stack") not in {"yara_rules", "rules_plus_fides"}:
            continue
        for rule_id in row.get("rule_ids", []) or []:
            rule_ids.add(str(rule_id))
            dataset_rule_coverage[str(row.get("dataset_id"))].add(str(rule_id))

    return {
        "schema_version": "canaryweave_fides.public_report.v1",
        "source_schema_version": run_report.get("schema_version"),
        "iterations": run_report.get("iterations"),
        "total_cases": run_report.get("total_cases"),
        "total_iterations": run_report.get("total_iterations"),
        "security_metrics": metrics,
        "incremental_metrics": {
            "warden_incremental_catches_vs_regex": len(regex_allowed_attacks & warden_blocked_attacks),
            "fides_incremental_catches_vs_warden": len(warden_allowed_attacks & fides_blocked_attacks),
        },
        "maintainability_metrics": {
            "rule_engine_codename": "WARDEN",
            "unique_rule_ids": sorted(rule_ids),
            "rule_count": len(rule_ids),
            "dataset_rule_coverage": {dataset: sorted(ids) for dataset, ids in dataset_rule_coverage.items()},
        },
        "groups": {
            "by_dataset": _group_counts(rows, "dataset_id"),
            "by_category": _group_counts(rows, "attack_category"),
            "by_surface": _group_counts(rows, "surface"),
        },
        "safety": {
            "public_safe": True,
            "case_level_rows_included": False,
            "source_material_included": False,
            "judge_transcripts_included": False,
        },
        "provider_calls": run_report.get("provider_calls", 0),
    }
