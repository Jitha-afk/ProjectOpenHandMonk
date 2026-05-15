# CanaryWeave Hermes-GSD Autonomous Plan

> **For Hermes:** Use subagent-driven-development and autonomous-continuation references to execute this plan task-by-task. This is a Hermes-native GSD-style plan; do not use OpenCode/GSD wrappers.

**Goal:** Complete CanaryWeave as an original, public-safe MCP sampling-abuse ASR research harness, with no remaining legacy-name references, a concrete research finding, and validated artifacts.

**Architecture:** CanaryWeave is a safe deterministic benchmark under `poc/canaryweave`. It uses typed scenario families, structural-only source adapters, benign canaries, inert local symbolic actions, grouped metrics, and dry-run model planning. Overnight execution should proceed through bounded phases with verification gates and durable status updates.

**Tech Stack:** Python 3.10+, pytest via `uv run --with pytest pytest`, local JSON/JSONL/CSV/Markdown artifacts, no live provider calls unless explicitly authorized later.

---

## Safety invariants

- No raw adversarial payloads from AgentDojo, InjecAgent, or the source paper.
- No real MCP exploitation, external network sinks, credentials, shell actions, account actions, or real data access.
- Model evaluation remains dry-run unless a later explicit instruction authorizes provider-backed execution.
- Public docs use the original name `CanaryWeave`, not legacy project names.
- Each phase must pass tests, CLI smokes, stale-term scan, and secret scan before advancing.

## Phase order

### Phase 1: Rename completion and identity hardening

**Objective:** Ensure the project is consistently named CanaryWeave and has no stale project-name or folder-name references.

**Files:** all files under `poc/canaryweave/`

**Steps:**
1. Run stale-name scan:
   `rg -n "<legacy-name-regex>" poc/canaryweave || true`
2. Fix any hits unless they are explicitly justified in a private local-only note. Committed docs should avoid stale branding.
3. Run `uv run --with pytest pytest -q` from `poc/canaryweave`.
4. Commit rename work before deeper research loops.

### Phase 2: Research finding loop runner

**Objective:** Build a deterministic loop runner that executes 50 safe improvement/evaluation loops and writes machine-readable results.

**Files:**
- Create: `poc/canaryweave/scripts/autonomous_research_loops.py`
- Create: `poc/canaryweave/tests/test_autonomous_research_loops.py`
- Output: `poc/canaryweave/artifacts/research/loop_results.json`

**Required behavior:**
- Run 50 loops by default.
- Each loop varies seed, attack-type mix, source-family condition, and mode comparisons.
- Record metrics for baseline, mcp, and attest modes.
- Compute grouped ASR, block rate, canary touch rate, amplification, reduction, and top scenario-family observations.
- Use deterministic local simulator only.
- Include a `finding` section summarizing the strongest supported local finding.

**TDD tests:**
- `test_loop_runner_default_count_is_50`
- `test_loop_runner_is_deterministic`
- `test_loop_runner_outputs_required_metric_fields`
- `test_loop_runner_finding_mentions_sampling_abuse_without_raw_payloads`

### Phase 3: Scenario enrichment

**Objective:** Add more safe scenario-family variety around sampling abuse while preserving secondary coverage.

**Files:**
- Modify: `src/canaryweave/registry.py`
- Modify: `tests/test_registry.py`
- Modify: `tests/test_sampling_abuse_generation.py`

**Required additions:**
- Add at least 3 additional sampling-focused families, such as:
  - `sampling_role_relabel_consensus`
  - `sampling_context_window_shadowing`
  - `sampling_candidate_replay_gap`
- Keep sampling total weight greater than all secondary classes combined.
- Tests must assert deterministic generation and metadata safety.

### Phase 4: Paper finding and figures/tables

**Objective:** Convert loop results into a paper-style finding.

**Files:**
- Create: `docs/canaryweave_findings.md`
- Create: `artifacts/research/summary_table.md`
- Modify: `docs/research_paper_draft.md`

**Required content:**
- Clear finding framed as local simulator evidence, not real-world exploitation.
- Table of mean ASR and reduction across 50 loops by attack type and mode.
- Discuss sampling abuse as the primary focus and compare with capability-attestation absence and implicit trust propagation.
- State limitations and safety boundaries.

### Phase 5: Dry-run model protocol polish

**Objective:** Improve the Hermes/Klive model dry-run scaffold without making live provider calls.

**Files:**
- Modify: `scripts/model_asr_dry_run.py`
- Modify: `docs/model_asr_scaffold.md`
- Tests as needed.

**Required behavior:**
- Add a `--model-set smoke_core|smoke_frontier` option.
- Ensure emitted plans include scenario-family diversity and redacted canaries only.
- Smoke command must succeed with no provider credentials.

### Phase 6: Final verification and handoff

**Objective:** Produce a clean, pushed branch ready for user review.

**Commands:**
```bash
cd /home/sealjitha/projects/ProjectOpenHandMonk/poc/canaryweave
uv run --with pytest pytest -q
PYTHONPATH=src python3 -m canaryweave.cli --seed 1337 --count 20 --attack-type sampling_abuse --mode mcp > /tmp/canaryweave_sampling.json
PYTHONPATH=src python3 scripts/model_asr_dry_run.py --seed 1337 --count 4 --output /tmp/canaryweave_model_dry_run.json
PYTHONPATH=src python3 scripts/autonomous_research_loops.py --loops 50 --output artifacts/research/loop_results.json
rg -n "<legacy-name-regex>" . && exit 1 || true
```

Run a secret scan for common token patterns. Remove `.venv`, `.pytest_cache`, `__pycache__`, `uv.lock`, and generated transient logs before commit, except intentional `artifacts/research/*.json` and `.md` research outputs.

## Commit strategy

- Commit after Phase 1 rename hardening.
- Commit after loop runner + scenario enrichment.
- Commit after research paper/finding docs.
- Final verification commit if needed.
- Push branch `poc/canaryweave-asr`.

## Autonomous loop definition

The requested "50 autonomous research improvement loops" are implemented as 50 deterministic safe local research loops plus code/doc refinement phases. Each loop must be logged in `artifacts/research/loop_results.json`. Do not simulate fake live model calls.
