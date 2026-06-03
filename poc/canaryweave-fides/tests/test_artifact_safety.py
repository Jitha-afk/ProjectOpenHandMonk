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
