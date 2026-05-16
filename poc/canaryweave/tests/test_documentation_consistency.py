from pathlib import Path


def test_public_docs_have_current_validation_and_canonical_model_dry_run():
    paper = Path("docs/research_paper_draft.md").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    status = Path("artifacts/research/autonomous_status.json").read_text(encoding="utf-8")
    handoff = Path("artifacts/research/AUTONOMOUS_HANDOFF.md").read_text(encoding="utf-8")

    assert "43 passed" in paper
    assert "32 passed" not in paper
    assert "--model-set smoke_core" in paper
    assert "total_trials: 16" in paper
    assert "simulated unauthorized-action execution rate" in paper
    assert "deterministic simulator invariant" in paper
    assert "Claim Boundary" in paper
    assert "References" in paper
    assert "pending final gate" not in status
    assert "final verification in progress" not in handoff.lower()
    assert "--model-set smoke_core" in readme
