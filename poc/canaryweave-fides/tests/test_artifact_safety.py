import json
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_artifacts_do_not_contain_disallowed_raw_shapes():
    bad = [
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
    ]
    scanned_roots = ["README.md", "conf", "data", "docs", "rules", "research", "design", "scripts", "artifacts"]
    for root in scanned_roots:
        root_path = ROOT / root
        paths = [root_path] if root_path.is_file() else root_path.rglob("*")
        for path in paths:
            if path.is_file() and path.suffix in {".py", ".yaml", ".yml", ".md", ".json", ".war"}:
                text = path.read_text(encoding="utf-8", errors="ignore").lower()
                hits = [needle for needle in bad if needle in text]
                assert hits == [], f"{path} contains disallowed public artifact shapes: {hits}"


def test_public_artifact_checker_decodes_cast_output_events(tmp_path):
    namespace = runpy.run_path(str(ROOT / "scripts" / "check_public_artifacts.py"), run_name="cast_checker_test")
    read_public_text = namespace["read_public_text"]
    cast_path = tmp_path / "demo.cast"
    cast_path.write_text(
        "\n".join(
            [
                json.dumps({"version": 2, "width": 80, "height": 24}),
                json.dumps([0.1, "o", "public-safe output"]),
                json.dumps([0.2, "i", "input is not published output"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    assert read_public_text(cast_path) == "public-safe output"
