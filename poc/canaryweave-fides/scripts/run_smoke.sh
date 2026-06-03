#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHONPATH=src python3 -m canaryweave_fides.cli \
  --fixture-set smoke \
  --output artifacts/smoke_report.json

python3 scripts/check_public_artifacts.py
