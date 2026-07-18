from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOTS = [
    ROOT / "README.md",
    ROOT / "conf",
    ROOT / "data",
    ROOT / "docs",
    ROOT / "rules",
    ROOT / "research",
    ROOT / "design",
    ROOT / "scripts",
    ROOT / "tests",
    ROOT / "artifacts",
    ROOT / "demo_rules",
]
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".sh", ".toml", ".war"}
CAST_SUFFIXES = {".cast"}

DISALLOWED_SHAPES = [
    "http" + "://",
    "https" + "://",
    "cu" + "rl ",
    "wg" + "et ",
    "power" + "shell",
    "api" + "_" + "key",
    "access" + "_" + "token",
    "bear" + "er ",
    "/etc/" + "passwd",
    "rm " + "-rf",
    "-----begin " + "private key-----",
    "-----begin " + "open" + "ssh private key-----",
]

SKIP_DIR_NAMES = {".git", ".pytest_cache", ".venv", "__pycache__"}


def iter_public_files() -> list[Path]:
    files: list[Path] = []
    for root in PUBLIC_ROOTS:
        if not root.exists():
            continue
        if root.is_file():
            files.append(root)
            continue
        for path in root.rglob("*"):
            if any(part in SKIP_DIR_NAMES for part in path.parts):
                continue
            if path.is_file() and path.suffix in TEXT_SUFFIXES | CAST_SUFFIXES:
                files.append(path)
    return sorted(files)


def read_public_text(path: Path) -> str:
    if path.suffix not in CAST_SUFFIXES:
        return path.read_text(encoding="utf-8", errors="ignore")

    output_events: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        if isinstance(item, dict):
            if line_number != 1:
                raise ValueError(f"unexpected cast header at line {line_number}")
            continue
        if not isinstance(item, list) or len(item) < 3:
            raise ValueError(f"invalid cast event at line {line_number}")
        if item[1] == "o" and isinstance(item[2], str):
            output_events.append(item[2])
    return "\n".join(output_events)


def main() -> int:
    failures: list[str] = []
    for path in iter_public_files():
        try:
            text = read_public_text(path).lower()
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            rel = path.relative_to(ROOT)
            failures.append(f"{rel}: invalid public artifact: {exc}")
            continue
        hits = [shape for shape in DISALLOWED_SHAPES if shape in text]
        if hits:
            rel = path.relative_to(ROOT)
            failures.append(f"{rel}: {', '.join(hits)}")
    if failures:
        print("public artifact safety check failed")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("public artifact safety ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
