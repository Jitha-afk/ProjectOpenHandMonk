# Peer Review Report: CanaryWeave FIDES / WARDEN Harness

Date: 2026-06-03
Branch: `poc/canaryweave-asr`
Scope: `poc/canaryweave-fides`

Terminology:

- **WARDEN**: deterministic YARA/OPA/Vigil-style rule engine.
- **FIDES**: separate LLM-as-judge layer for WARDEN misses.

## Reviewers

Three independent reviewer routines were run:

1. Code reviewer: architecture, tests, serialization, CLI, adapters, reporting, safety bugs.
2. Thesis/accuracy reviewer: alignment with the intended research goal and what claims are currently defensible.
3. Security detection reviewer: whether detections, attacks, mappings, and metrics make sense from a security-engineering / MITRE ATT&CK / D3FEND perspective.

A project-level cybersecurity skill was installed successfully:

- `analyzing-threat-actor-ttps-with-mitre-attack`

The requested `copyleftdev/sk1llz@mitre-attack-framework` skill could not be installed because the GitHub repository was inaccessible through the skills CLI / git clone path.

## Executive summary

Verdict across reviewers: **REQUEST_CHANGES before making research/effectiveness claims**.

The implementation is a useful scaffold and harness milestone. It has good structure, public artifact safety discipline, tests, adapters, schemas, a gate runner, reports, and safe simulators. However, it is not yet ready to support the thesis that defender-authored YARA-style WARDEN rules plus FIDES LLM-as-judge improve agent security posture across multiple datasets.

The biggest blockers are:

1. The public eval path does not execute the declared `.cwfr.yaml` WARDEN rule files.
2. FIDES LLM-as-judge is not implemented or exercised in the public eval path.
3. Current results are synthetic-only; ASB and AgentDefenseBench are not yet used in metrics.
4. Metrics currently measure gate decisions/proxy outcomes, not real attack success.
5. Dataset adapters risk label-driven/circular evaluation if used as-is.
6. Detection/rule mappings lack MITRE/D3FEND or equivalent detection-engineering metadata and expected-rule mappings.

## Code review findings

Verdict: **REQUEST_CHANGES**

### Critical

None requiring immediate rollback.

### Important

1. **Main eval path does not use authored WARDEN rule files.**
   - The smoke/query paths load `.cwfr.yaml` through `RuleEngine`.
   - The public eval path uses hard-coded checks in `gate.py` with rule IDs like `warden.untrusted_tool_plan`.
   - Changing `rules/*.cwfr.yaml` does not affect public eval output.
   - Required fix: wire public eval to actual `.cwfr.yaml` rules or generate the executable checks from those rule files.

2. **`run_multi_dataset_eval.sh` and CLI eval are synthetic-only by default.**
   - Config files are parsed, but dataset configs are not used to instantiate ASB / AgentDefenseBench adapters.
   - Required fix: add config loading and adapter creation from `conf/datasets.yaml` / eval specs.

3. **FIDES abstractions are split and confusing.**
   - `FidesIFCLayer` is deterministic IFC-style logic in smoke/query paths.
   - `StaticFidesJudge` is a test double for the FIDES LLM-as-judge contract in gate eval.
   - Default public eval FIDES behavior returns safe and adds no protection.
   - Required fix: make FIDES judge mode explicit: disabled, deterministic test double, or provider-backed LLM judge.

4. **Public reporting under-counts incremental catches when category/iteration collide.**
   - Internal keys omit `case_id`, so multiple cases in the same dataset/category/iteration can collapse.
   - Required fix: use stable internal case keys for computation, then redact in the public report.

5. **Legacy smoke ASR denominator is wrong.**
   - `metrics.py` divides ASR by total cases instead of attack cases.
   - Required fix: divide by attack-case denominator and add regression tests.

6. **`QueryResult.to_dict()` can leak raw model output.**
   - Public serialization includes `output_text` verbatim.
   - Required fix: add `to_public_dict()` redacting/hashing model output and keep raw output only in private artifacts.

7. **ASB adapter emits unsalted hashes of private text/native IDs.**
   - Public unsalted SHA-256 may be dictionary-attacked for known benchmark payloads.
   - Required fix: use HMAC for public correlation or keep raw SHA-256 only in private manifests.

### Minor

- `RuleEngine` uses constrained `eval()` for boolean conditions; replace with a small AST/boolean parser later.
- CLI lacks `--config`, `--dataset`, `--rules-dir`, and public/private output split.
- Tests need more regression coverage for config-driven adapters, `.cwfr` eval, duplicate categories, QueryResult public serialization, and HMAC behavior.

## Thesis / accuracy review findings

Verdict: **Not ready for thesis claims**

Current implementation can accurately claim:

- A public-safe harness scaffold exists.
- It defines pre-context gate stacks: no guard, regex baseline, WARDEN-like deterministic rules, and WARDEN+FIDES.
- It has synthetic cases, optional adapter scaffolding, public-safe reports, and aggregate metrics.
- It demonstrates hard-coded WARDEN-like checks outperforming a weak regex baseline on a tiny synthetic fixture set.
- It defines a FIDES LLM-as-judge contract.

It cannot yet claim:

- Defender-authored `.cwfr` / YARA-style rules improve security posture.
- FIDES LLM-as-judge improves outcomes over WARDEN.
- Multi-dataset portability across ASB, AgentDefenseBench, and other corpora.
- Real ASR reduction on agent attacks.

### Critical blockers

1. **FIDES LLM-as-judge is not implemented or exercised.**
   - Public eval reports `provider_calls: 0` and no FIDES incremental catches.
   - FIDES is currently a contract/test double in gate eval.

2. **The reported `yara_rules` stack is not executing `.cwfr.yaml` rules.**
   - Public metrics are driven by hard-coded WARDEN-like heuristics.

3. **Multi-dataset evidence is absent.**
   - Current reports show only `synthetic` data.
   - ASB/AgentDefenseBench are optional adapters but not exercised in public metrics.

4. **ASR is currently a gate-level proxy.**
   - No-guard ASR is assumed by labels.
   - There is no actual agent/tool compromise measurement yet.

### Important gaps

- OPA/Rego/Vigil-like transferability is partially implemented structurally but not proven.
- Rule portability/quality metrics are superficial until real datasets and real rules are used.
- FIDES terminology should separate legacy deterministic IFC smoke behavior from the FIDES LLM judge.
- Public reports should label current results as synthetic CI/proxy results, not benchmark evidence.

## Security detection review findings

Verdict: **Not ready for detection-effectiveness claims**

### Critical findings

1. **Declared `.cwfr` WARDEN rules and public metric rules are different.**
   - Public reports list hard-coded `warden.*` IDs, not `.cwfr` IDs such as `cwfr-0001`.
   - This makes attack-to-rule mapping unsound.

2. **Dataset adapters risk circular measurement.**
   - `ASBAdapter` derives trust labels and expected behavior from dataset labels.
   - That can make the detector measure labels/adapters rather than adversarial behavior.

3. **Detection causality is insufficient.**
   - Current `RuleEngine` uses “any event in trace” signal semantics, which can combine unrelated events.
   - `NormalizedFacts` collapses cases into booleans and loses event order/causality.
   - Need same-event/window/causal-chain semantics for claims like “untrusted content caused a consequential action.”

4. **Metrics measure guard decisions, not real attack success.**
   - Current attack success is effectively “attack case was allowed.”
   - This is fine for proxy tests, not for real security claims.

### Important findings

1. **MITRE ATT&CK / D3FEND alignment is missing.**
   - Current categories are internal AI-agent policy labels, not ATT&CK/D3FEND mappings.
   - Prompt injection itself should not be forced into ATT&CK. Instead, map downstream effects:
     - unauthorized tool/code execution → Execution / command or tool invocation techniques when applicable;
     - data leakage to unauthorized sink → Exfiltration;
     - credential leakage → Credential Access / Unsecured Credentials;
     - hidden Unicode/encoding → Defense Evasion / obfuscation analog only when hiding behavior;
     - path traversal/resource boundary escape → protected resource access and boundary violation; exact mapping depends on target system.
   - D3FEND-style mappings should include content normalization, content analysis, access mediation, execution isolation, DLP/permitted-flow enforcement, and canary/decoy patterns.

2. **HiddenUnicodeStructure is too broad.**
   - It should require untrusted origin/surface and careful normalization semantics.
   - Generic control characters may cause false positives.

3. **Attack taxonomy is incomplete.**
   Missing dimensions include:
   - instruction hierarchy violation;
   - tool misuse / unauthorized capability;
   - data exfiltration / unapproved sink;
   - credential/secret handling;
   - file access/path traversal/resource boundary escape;
   - command/code execution;
   - network/SSRF/API abuse;
   - memory/RAG/context poisoning;
   - persistence/config tampering;
   - DoS/resource exhaustion;
   - approval/consent bypass;
   - obfuscation/evasion;
   - supply-chain/plugin/MCP server trust abuse;
   - benign near-miss controls per category.

4. **Attack-to-rule mapping is not explicit enough.**
   - Cases need `expected_policy_violation`, `expected_rule_ids`, `expected_fides_checks`, required telemetry, and should-not-fire controls.

## Recommended remediation plan

Priority order:

1. **Unify WARDEN execution.**
   - Public eval must execute declared `.cwfr.yaml` rules or generate executable checks from them.
   - Report `.cwfr` IDs and metadata.

2. **Separate labels from detection features.**
   - Dataset adapters must not derive trust/untrusted or expected behavior directly into detector features.
   - Ground truth should be stored separately from facts given to WARDEN/FIDES.

3. **Add rule/case mapping schema.**
   - Add expected policy violation, expected rule IDs, expected FIDES checks, surface, data source, and optional ATT&CK/D3FEND mappings.

4. **Add causal/event semantics.**
   - Support same-event, same-window, and source→action/source→sink correlation.

5. **Implement actual FIDES LLM judge path.**
   - Redacted facts in; strict JSON verdict out; provider disabled by default but explicit opt-in.
   - Track FIDES-only catches and FIDES false positives.

6. **Run real datasets.**
   - Use ASB and AgentDefenseBench via controlled paths.
   - Report synthetic CI separately from controlled local benchmark results.

7. **Improve safety/public serialization.**
   - Add public/private serializer separation for QueryResult and FIDES outputs.
   - Replace public raw SHA-256 payload hashes with HMAC or private-only hashes.

8. **Add benign near-miss fixtures.**
   - Especially for Unicode, policy/system words, path-like text, authorized sinks, trusted tool plans, and docs that mention security terms benignly.

## Skill registration status

Installed:

- `analyzing-threat-actor-ttps-with-mitre-attack`

Failed:

- `copyleftdev/sk1llz@mitre-attack-framework`
  - skills CLI and direct git lookup could not access the copyleftdev/sk1llz GitHub repository URL.
  - `skills find mitre` lists it, but installation fails with repository authentication/not-found errors.

## Bottom line

The harness is a good scaffold and engineering base. The peer review found no immediate rollback-level security flaw, but it found multiple blockers to the intended research claim. The next implementation round should focus on making WARDEN truly rule-file-driven, making FIDES a real judge layer, separating ground truth from detection features, and adding explicit security detection mappings before running ASB/AgentDefenseBench claims.
