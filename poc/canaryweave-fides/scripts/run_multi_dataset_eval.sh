#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 - <<'PY'
from pathlib import Path
import sys
import yaml

required = [
    Path('conf/default.yaml'),
    Path('conf/datasets.yaml'),
    Path('conf/stacks.yaml'),
    Path('data/evals/multi_dataset_gate.yaml'),
]
for path in required:
    with path.open('r', encoding='utf-8') as handle:
        yaml.safe_load(handle)
print('multi-dataset config ok')
print('multi-dataset executable runner is not implemented in Milestone 1')
sys.exit(0)
PY

python3 scripts/check_public_artifacts.py
