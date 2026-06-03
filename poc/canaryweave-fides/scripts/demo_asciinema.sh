#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DEMO_FAST="${CANARYWEAVE_DEMO_FAST:-0}"
OUT="${CANARYWEAVE_DEMO_OUT:-/tmp/canaryweave-fides-demo}"
mkdir -p "$OUT"

pause() {
  if [ "$DEMO_FAST" = "1" ]; then
    return 0
  fi
  sleep "${1:-1}"
}

say() {
  printf '\n\033[1;36m%s\033[0m\n' "$1"
}

note() {
  printf '\033[0;37m%s\033[0m\n' "$1"
}

run_cmd() {
  printf '\n\033[1;33m$ %s\033[0m\n' "$*"
  "$@"
}

run_shell() {
  printf '\n\033[1;33m$ %s\033[0m\n' "$*"
  bash -lc "$*"
}

banner() {
  if command -v toilet >/dev/null 2>&1; then
    toilet -f term -F border "WARDEN"
  elif command -v pyfiglet >/dev/null 2>&1; then
    pyfiglet "WARDEN"
  else
    printf '%s\n' ' __        ___    ____  ____  _____ _   _ '
    printf '%s\n' ' \ \      / / \  |  _ \|  _ \| ____| \ | |'
    printf '%s\n' '  \ \ /\ / / _ \ | |_) | | | |  _| |  \| |'
    printf '%s\n' '   \ V  V / ___ \|  _ <| |_| | |___| |\  |'
    printf '%s\n' '    \_/\_/_/   \_\_| \_\____/|_____|_| \_|'
  fi
  printf '\nCanaryWeave FIDES public-safe terminal demo\n'
}

flow_animation() {
  local frames=(
    '[ private custody ]'
    '[ private custody ] -> [ redacted features ]'
    '[ private custody ] -> [ redacted features ] -> [ WARDEN rules ]'
    '[ private custody ] -> [ redacted features ] -> [ WARDEN rules ] -> [ FIDES flow check ]'
    '[ private custody ] -> [ redacted features ] -> [ WARDEN rules ] -> [ FIDES flow check ] -> [ aggregate report ]'
  )
  for frame in "${frames[@]}"; do
    printf '\r%-120s' "$frame"
    pause 0.45
  done
  printf '\n'
}

python_summary() {
  local report="$1"
  uv run python - "$report" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
report = json.loads(path.read_text(encoding="utf-8"))
print(f"report={path}")
print(f"schema={report.get('schema_version')} total_cases={report.get('total_cases')} total_iterations={report.get('total_iterations')}")
print(f"provider_calls={report.get('provider_calls')}")

safety = report.get("safety") or {}
if safety:
    print("safety=" + ", ".join(f"{k}={v}" for k, v in sorted(safety.items())))

for item in report.get("adapter_results", []):
    print(
        "adapter="
        + str(item.get("dataset_id"))
        + f" status={item.get('status')} cases={item.get('case_count')} public_export={item.get('safe_metadata', {}).get('public_export', 'n/a')}"
    )

metrics = report.get("security_metrics") or {}
for stack in ("no_guard", "regex_baseline", "yara_rules", "rules_plus_fides"):
    values = metrics.get(stack)
    if not values:
        continue
    print(
        f"{stack:18s} asr={values.get('asr')} recall={values.get('recall')} "
        f"safe_pass={values.get('safe_pass_through_rate')} benign_refusal={values.get('benign_refusal_rate')}"
    )

incremental = report.get("incremental_metrics") or {}
if incremental:
    print(
        "incremental="
        + f"warden_vs_regex={incremental.get('warden_incremental_catches_vs_regex')} "
        + f"fides_vs_warden={incremental.get('fides_incremental_catches_vs_warden')} "
        + f"remaining_misses={incremental.get('remaining_misses_after_rules_plus_fides')}"
    )

maint = report.get("maintainability_metrics") or {}
if maint:
    print(
        "rules="
        + f"covered={maint.get('covered_rule_count')} total={maint.get('total_rule_count')} "
        + f"codename={maint.get('rule_engine_codename')}"
    )

evidence = report.get("expected_rule_evidence") or {}
if evidence:
    print(
        "expected_rule_evidence="
        + f"available={evidence.get('available')} "
        + f"cases={evidence.get('cases_with_expected_rules')} "
        + f"hit_rate={evidence.get('expected_rule_hit_rate')}"
    )
PY
}

say "Scene 1/6: WARDEN identity"
banner
pause 1
flow_animation
note "Public demo boundary: no raw payloads, no raw prompts, no judge transcripts, no private CSV rows."
pause 1

say "Scene 2/6: Reviewable .war rule inventory"
run_shell "uv run python - <<'PY'
from pathlib import Path
root = Path('rules')
rows = []
for path in sorted(root.rglob('*.war')):
    fields = {}
    for line in path.read_text(encoding='utf-8', errors='ignore').splitlines():
        for key in ('id', 'name', 'category', 'severity'):
            prefix = key + ':'
            if line.startswith(prefix) and key not in fields:
                fields[key] = line.split(':', 1)[1].strip()
    rows.append((str(path), fields.get('id', '?'), fields.get('name', '?'), fields.get('category', '?'), fields.get('severity', '?')))
print(f'WARDEN rule files: {len(rows)}')
for path, rule_id, name, category, severity in rows:
    print(f'- {path} :: {rule_id} :: {name} :: {category} :: {severity}')
PY"
pause 1

say "Scene 3/6: Tests and public smoke eval"
TEST_TARGETS="tests/test_warden_rule_style.py tests/test_artifact_safety.py tests/test_asb_evidence_reporting.py"
run_shell "uv run --with pytest --with PyYAML pytest -q $TEST_TARGETS"

SMOKE_REPORT="$OUT/smoke_public_report.json"
SMOKE_STDOUT="$OUT/smoke_stdout.json"
run_shell "uv run python -m canaryweave_fides.cli eval --config data/evals/smoke.yaml --public-report --output '$SMOKE_REPORT' > '$SMOKE_STDOUT'"
python_summary "$SMOKE_REPORT"
pause 1

say "Scene 4/6: ASB public aggregate metrics only"
ASB_REPORT="$OUT/asb_public_report.json"
if [ -n "${CANARYWEAVE_ASB_ROOT:-}" ] && [ -e "${CANARYWEAVE_ASB_ROOT:-}" ]; then
  note "Private ASB root detected through CANARYWEAVE_ASB_ROOT; running public aggregate export only."
  run_shell "uv run python -m canaryweave_fides.cli eval --config data/evals/multi_dataset_gate.yaml --dataset asb --iterations 1 --public-report --output '$ASB_REPORT' > '$OUT/asb_stdout.json'"
else
  if [ -f artifacts/evals/asb_controlled_public_report_1.json ]; then
    note "No private ASB root configured; summarizing checked-in public aggregate report."
    cp artifacts/evals/asb_controlled_public_report_1.json "$ASB_REPORT"
  else
    note "No ASB aggregate report available; running multi-dataset public eval to show optional skip status."
    run_shell "uv run python -m canaryweave_fides.cli eval --config data/evals/multi_dataset_gate.yaml --dataset asb --iterations 1 --public-report --output '$ASB_REPORT' > '$OUT/asb_stdout.json'"
  fi
fi
python_summary "$ASB_REPORT"
note "ASB source rows and private payload fields remain withheld."
pause 1

say "Scene 5/6: Private reviewer CSV path warning"
run_shell "uv run python - <<'PY'
from pathlib import Path
from canaryweave_fides.runner import _validate_private_review_csv_path

public_target = Path('artifacts/private_review.csv')
controlled_target = Path('/tmp/canaryweave-fides-private-review/review.csv')
try:
    _validate_private_review_csv_path(public_target)
except ValueError as exc:
    print(f'blocked public CSV target: {public_target} -> {exc}')
else:
    raise SystemExit('expected public CSV target to be blocked')
_validate_private_review_csv_path(controlled_target)
print(f'controlled CSV target allowed: {controlled_target}')
print('CSV contents are private custody material and are not printed in this recording.')
PY"
pause 1

say "Scene 6/6: Public artifact safety check"
run_cmd uv run python scripts/check_public_artifacts.py

say "Demo complete"
note "Outputs written under $OUT"
note "Record with: asciinema rec --overwrite -c 'bash scripts/demo_asciinema.sh' docs/canaryweave-fides-demo.cast"
