# Running Evaluations

Milestone 1 adds Vigil-style configuration, dataset specs, manifests, docs, and helper scripts. It does not implement the multi-dataset runner yet.

## Smoke verification

From `poc/canaryweave-fides`:

```bash
scripts/run_smoke.sh
```

The script runs the existing CLI smoke path and then checks public artifacts.

## Multi-dataset placeholder

From `poc/canaryweave-fides`:

```bash
scripts/run_multi_dataset_eval.sh
```

In Milestone 1 this script validates configuration files and reports that the executable multi-dataset runner is not implemented yet. Later milestones will connect it to adapters and the gate runner.

## Required verification

Before committing this milestone, run:

```bash
python3 scripts/check_markdown_fences.py
uv run --with pytest --with PyYAML pytest -q
```

## Public artifact safety

Run:

```bash
python3 scripts/check_public_artifacts.py
```

The safety scanner rejects common raw payload shapes, credential-like strings, and provider transcript markers in public roots.
