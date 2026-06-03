# CanaryWeave FIDES demo plan

Public-safe terminal demo plan for recording CanaryWeave FIDES with asciinema.

## Goal

Show the viewer that CanaryWeave FIDES is a layered, reviewable guard demo:

1. WARDEN presents a deterministic rule layer with human-readable `.war` policies.
2. Tests and smoke evaluation run locally.
3. WARDEN improves aggregate attack blocking versus the regex baseline on public-safe synthetic cases.
4. ASB evidence is shown only as public aggregate metrics.
5. Private reviewer CSV custody is acknowledged without printing CSV contents or source payload text.

## Safety boundaries

- Do not print raw payload text, raw prompts, raw completions, judge transcripts, or private CSV rows.
- Only show public aggregate JSON fields such as totals, stack metrics, rule coverage, safety flags, and adapter status.
- Keep private dataset roots outside the repo and use environment variables for local custody paths.
- Treat reviewer CSV files as private custody artifacts. The demo shows the path policy and warning only.
- Provider calls remain disabled for the public demo.

## Recommended recording setup

Terminal size: 100 columns by 32 rows.

Suggested shell setup before recording:

```bash
cd /path/to/ProjectOpenHandMonk/poc/canaryweave-fides
export CANARYWEAVE_DEMO_FAST=0
export CANARYWEAVE_DEMO_OUT=/tmp/canaryweave-fides-demo
```

Optional ASB local dataset custody:

```bash
export CANARYWEAVE_ASB_ROOT=/path/to/private/asb
```

If `CANARYWEAVE_ASB_ROOT` is not set, the script summarizes the existing public aggregate ASB report when present. It does not load or print private source records.

## Storyboard

### Scene 1: WARDEN identity and safety boundary

- Display WARDEN ASCII banner.
- Show an ASCII flow animation:
  private custody -> redacted features -> WARDEN/FIDES -> aggregate report.
- State that source payloads and private CSV rows are not printed.

### Scene 2: Rule inventory

- List `.war` files from `rules/`.
- Print only path, rule id, name, category, and severity.
- Do not print fixtures or payload-like examples.

### Scene 3: Tests and smoke

- Run pytest through the local Python environment or `uv --no-project` fallback.
- Run public smoke eval:

```bash
uv run python -m canaryweave_fides.cli eval \
  --config data/evals/smoke.yaml \
  --public-report \
  --output /tmp/canaryweave-fides-demo/smoke_public_report.json
```

- Summarize only aggregate fields: safety flags, ASR, recall, safe pass-through, incremental WARDEN catches, provider call count, and rule coverage.

### Scene 4: ASB public aggregate metrics

- If a private ASB root is configured, run the ASB eval with `--public-report` and output to `/tmp`.
- Otherwise summarize `artifacts/evals/asb_controlled_public_report_1.json` if available.
- Print adapter status, total cases, public safety flags, security metrics, expected-rule evidence, and rule coverage.
- Do not print case-level rows or source material.

### Scene 5: Private CSV path warning

- Show the path validator rejecting a repo-public CSV target.
- Show a controlled example path under `/tmp` or `CANARYWEAVE_PRIVATE_REVIEW_CSV`.
- Explicitly state that CSV contents are withheld from the recording.

### Scene 6: Public artifact safety check

- Run `uv run python scripts/check_public_artifacts.py`.
- End on `public artifact safety ok`.

## Asciinema recording command

From the project directory:

```bash
asciinema rec --overwrite \
  -c 'bash scripts/demo_asciinema.sh' \
  docs/canaryweave-fides-demo.cast
```

Fast dry run without recording:

```bash
CANARYWEAVE_DEMO_FAST=1 bash scripts/demo_asciinema.sh
```

Replay locally:

```bash
asciinema play docs/canaryweave-fides-demo.cast
```

## GIF and MP4 conversion suggestions

If `agg` is installed:

```bash
agg docs/canaryweave-fides-demo.cast docs/canaryweave-fides-demo.gif
```

If `ffmpeg` is installed, convert the GIF to MP4:

```bash
ffmpeg -y -i docs/canaryweave-fides-demo.gif \
  -movflags faststart \
  -pix_fmt yuv420p \
  docs/canaryweave-fides-demo.mp4
```

If `agg` is unavailable, keep the `.cast` file as the primary terminal recording artifact and replay it with `asciinema play`.

## Notes for the presenter

- Keep narration focused on the narrow research claim: structured, reviewable policy facts improve over shallow regex matching in controlled MCP-style security cases, and FIDES/IFC is the optional flow layer for remaining semantic misses.
- Do not open private datasets, reviewer CSVs, or raw source files during the recording.
- If the ASB private root is unavailable, say the demo is using a previously generated public aggregate report.
- If a command fails because optional tooling is missing, show the fallback path rather than installing tools during the recording.
