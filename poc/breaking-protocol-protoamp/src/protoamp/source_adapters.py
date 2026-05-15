from __future__ import annotations

import ast
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from .scenario import SourceFamily


@dataclass(frozen=True)
class FileSummary:
    relative_path: str
    sha256: str
    byte_count: int
    record_count: int
    category_counts: Mapping[str, int] = field(default_factory=dict)
    schema_keys: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "category_counts", MappingProxyType(dict(self.category_counts)))
        object.__setattr__(self, "schema_keys", tuple(self.schema_keys))


@dataclass(frozen=True)
class SourceSummary:
    source_family: SourceFamily
    adapter_name: str
    source_root: str
    digest: str
    record_count: int
    category_counts: Mapping[str, int] = field(default_factory=dict)
    schema_keys: tuple[str, ...] = ()
    file_summaries: tuple[FileSummary, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_family", SourceFamily(self.source_family))
        object.__setattr__(self, "category_counts", MappingProxyType(dict(self.category_counts)))
        object.__setattr__(self, "schema_keys", tuple(self.schema_keys))
        object.__setattr__(self, "file_summaries", tuple(self.file_summaries))

    def to_safe_dict(self) -> dict[str, object]:
        return {
            "source_family": self.source_family.value,
            "adapter_name": self.adapter_name,
            "source_root": self.source_root,
            "digest": self.digest,
            "record_count": self.record_count,
            "category_counts": dict(self.category_counts),
            "schema_keys": list(self.schema_keys),
            "file_summaries": [_file_summary_to_dict(summary) for summary in self.file_summaries],
        }


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _file_summary(root: Path, path: Path, record_count: int = 0, category_counts: Mapping[str, int] | None = None, schema_keys: tuple[str, ...] = ()) -> FileSummary:
    data = path.read_bytes()
    return FileSummary(
        relative_path=str(path.relative_to(root)),
        sha256=_sha256_bytes(data),
        byte_count=len(data),
        record_count=record_count,
        category_counts=category_counts or {},
        schema_keys=schema_keys,
    )


def _file_summary_to_dict(summary: FileSummary) -> dict[str, object]:
    return {
        "relative_path": summary.relative_path,
        "sha256": summary.sha256,
        "byte_count": summary.byte_count,
        "record_count": summary.record_count,
        "category_counts": dict(summary.category_counts),
        "schema_keys": list(summary.schema_keys),
    }


def _source_digest(file_summaries: tuple[FileSummary, ...], extra: Mapping[str, object] | None = None) -> str:
    payload = {
        "files": [_file_summary_to_dict(summary) for summary in file_summaries],
        "extra": dict(extra or {}),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"sha256:{_sha256_bytes(encoded)}"


def synthetic_source_summary() -> SourceSummary:
    return SourceSummary(
        source_family=SourceFamily.SYNTHETIC_SAFE,
        adapter_name="synthetic_static",
        source_root="synthetic",
        digest="synthetic:default-safe",
        record_count=0,
        category_counts={"synthetic_safe": 1},
        schema_keys=("scenario_family", "attack_type", "source_family"),
        file_summaries=(),
    )


def _missing_summary(source_family: SourceFamily, adapter_name: str, root: Path) -> SourceSummary:
    return SourceSummary(
        source_family=source_family,
        adapter_name=adapter_name,
        source_root=str(root),
        digest=f"synthetic:missing-{source_family.value}",
        record_count=0,
        category_counts={"missing_source_root": 1},
        schema_keys=(),
        file_summaries=(),
    )


def _count_json_records(path: Path) -> tuple[int, tuple[str, ...], dict[str, int]]:
    if not path.exists():
        return 0, (), {}
    if path.suffix == ".jsonl":
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        parsed = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(parsed, list):
            records = parsed
        elif isinstance(parsed, dict):
            records = list(parsed.values())
        else:
            records = []
    keys: set[str] = set()
    categories: dict[str, int] = {}
    for record in records:
        if isinstance(record, dict):
            keys.update(str(k) for k in record.keys())
            for field in ("Attack Type", "category", "Level"):
                value = record.get(field)
                if isinstance(value, str):
                    categories[value] = categories.get(value, 0) + 1
    return len(records), tuple(sorted(keys)), categories


def _ast_counts(path: Path) -> tuple[int, int]:
    tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    class_count = sum(isinstance(node, ast.ClassDef) for node in ast.walk(tree))
    function_count = sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in ast.walk(tree))
    return class_count, function_count


def summarize_agentdojo(root: Path, strict: bool = False) -> SourceSummary:
    root = Path(root)
    if not root.exists():
        if strict:
            raise FileNotFoundError(root)
        return _missing_summary(SourceFamily.AGENTDOJO_STRUCTURAL, "agentdojo_structural_v1", root)

    rels = [
        "src/agentdojo/default_suites/v1/workspace/injection_tasks.py",
        "src/agentdojo/default_suites/v1/slack/injection_tasks.py",
        "src/agentdojo/default_suites/v1/banking/injection_tasks.py",
        "src/agentdojo/default_suites/v1/travel/injection_tasks.py",
        "src/agentdojo/attacks/baseline_attacks.py",
        "src/agentdojo/attacks/important_instructions_attacks.py",
    ]
    file_summaries: list[FileSummary] = []
    category_counts: dict[str, int] = {}
    total_records = 0
    for rel in rels:
        path = root / rel
        if not path.exists():
            continue
        class_count, function_count = _ast_counts(path)
        total_records += class_count
        suite = rel.split("/")[4] if "default_suites" in rel else "attack_module"
        category_counts[suite] = category_counts.get(suite, 0) + class_count
        file_summaries.append(
            _file_summary(
                root,
                path,
                record_count=class_count,
                category_counts={"classes": class_count, "functions": function_count},
                schema_keys=("class_count", "function_count", "module_path"),
            )
        )
    file_summaries_tuple = tuple(file_summaries)
    digest = _source_digest(file_summaries_tuple, {"adapter": "agentdojo_structural_v1"})
    return SourceSummary(
        source_family=SourceFamily.AGENTDOJO_STRUCTURAL,
        adapter_name="agentdojo_structural_v1",
        source_root=str(root),
        digest=digest,
        record_count=total_records,
        category_counts=category_counts,
        schema_keys=("class_count", "function_count", "suite", "module_path"),
        file_summaries=file_summaries_tuple,
    )


def summarize_injecagent(root: Path, strict: bool = False) -> SourceSummary:
    root = Path(root)
    if not root.exists():
        if strict:
            raise FileNotFoundError(root)
        return _missing_summary(SourceFamily.INJECAGENT_STRUCTURAL, "injecagent_structural_v1", root)

    rels = [
        "data/attacker_cases_dh.jsonl",
        "data/attacker_cases_ds.jsonl",
        "data/test_cases_dh_base.json",
        "data/test_cases_ds_base.json",
        "data/tools.json",
        "data/user_cases.jsonl",
    ]
    file_summaries: list[FileSummary] = []
    category_counts: dict[str, int] = {}
    schema_keys: set[str] = set()
    total_records = 0
    for rel in rels:
        path = root / rel
        if not path.exists():
            continue
        record_count, keys, categories = _count_json_records(path)
        total_records += record_count
        schema_keys.update(keys)
        for label, count in categories.items():
            category_counts[label] = category_counts.get(label, 0) + count
        file_summaries.append(
            _file_summary(
                root,
                path,
                record_count=record_count,
                category_counts=categories,
                schema_keys=keys,
            )
        )
    file_summaries_tuple = tuple(file_summaries)
    digest = _source_digest(file_summaries_tuple, {"adapter": "injecagent_structural_v1"})
    return SourceSummary(
        source_family=SourceFamily.INJECAGENT_STRUCTURAL,
        adapter_name="injecagent_structural_v1",
        source_root=str(root),
        digest=digest,
        record_count=total_records,
        category_counts=category_counts,
        schema_keys=tuple(sorted(schema_keys)),
        file_summaries=file_summaries_tuple,
    )


def load_source_summary(source_family: SourceFamily, root: Path | None = None) -> SourceSummary:
    source_family = SourceFamily(source_family)
    if source_family is SourceFamily.SYNTHETIC_SAFE:
        return synthetic_source_summary()
    if source_family is SourceFamily.AGENTDOJO_STRUCTURAL:
        return summarize_agentdojo(root or Path("/tmp/protoamp-source-repos/agentdojo"))
    if source_family is SourceFamily.INJECAGENT_STRUCTURAL:
        return summarize_injecagent(root or Path("/tmp/protoamp-source-repos/InjecAgent"))
    raise ValueError(f"unsupported source family: {source_family}")
