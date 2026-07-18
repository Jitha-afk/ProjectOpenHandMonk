# Safe Hermes/Klive model interaction scaffold

This scaffold supports the model-interaction research request without sending raw harmful payloads or calling provider APIs by default.

Primary focus: sampling-abuse ASR scenarios.
Secondary coverage: capability-attestation absence and implicit trust propagation.

## Files

- `configs/model_registry.safe.yaml`
  - Disabled-by-default model registry placeholders for GPT-4o, Claude Sonnet 4.6/Sonnet-family, and other Hermes-configured models.
  - Exact provider IDs must be verified in the local account before a live run.

- `scripts/model_asr_dry_run.py`
  - Builds dry-run trial plans from the safe scenario registry.
  - Redacts canaries in emitted trial JSON.
  - Does not call external model APIs.

- `research/klive_model_asr_protocol.md`
  - Full evaluation protocol: JSONL schema, grouping, ASR metrics, confidence intervals, retry/budget controls, and provider/Hermes execution paths.

## Dry-run command

From this POC directory:

```bash
PYTHONPATH=src python3 scripts/model_asr_dry_run.py --model-set smoke_core --seed 1337 --count 4 --output artifacts/runs/model_dry_run.json
```

Expected behavior:

- Creates a safe local JSON plan only.
- Includes trial rows for the `smoke_core` set by default when requested, or the broader `smoke_frontier` placeholder set when no set is specified.
- Includes `mcp` and `attest` modes by default.
- Uses only redacted canaries and neutral prompt template IDs.

## Live model execution boundary

Live provider/Hermes execution is intentionally not implemented in this patch. Before adding it:

1. Verify model IDs in the configured provider account.
2. Keep scenarios benign-canary-only.
3. Route tools to local inert mock sinks only.
4. Disable any real web, email, filesystem-secret, shell, or account-modifying tools.
5. Score primary ASR with deterministic trace parsing, not LLM judging.
6. Redact full canaries before sharing logs.

The dry-run plan is the review artifact that Klive/Hermes should use before enabling any provider-backed experiment.
