from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_public_artifacts_do_not_contain_disallowed_raw_shapes():
    bad = [
        "http" + "://",
        "https" + "://",
        "curl ",
        "wget ",
        "powershell",
        "api" + "_" + "key",
        "access" + "_" + "token",
        "bearer ",
        "/etc/" + "passwd",
        "rm " + "-rf",
    ]
    scanned_roots = ["rules", "research", "design", "artifacts"]
    for root in scanned_roots:
        for path in (ROOT / root).rglob("*"):
            if path.is_file() and path.suffix in {".py", ".yaml", ".yml", ".md", ".json"}:
                text = path.read_text(encoding="utf-8", errors="ignore").lower()
                hits = [needle for needle in bad if needle in text]
                assert hits == [], f"{path} contains disallowed public artifact shapes: {hits}"
