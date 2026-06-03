# Initial Research Report Draft: Controlled Multi-Dataset Evidence for CanaryWeave FIDES

Date: 2026-06-03
Status: initial academic-style draft outline and results narrative
Scope: `poc/canaryweave-fides`
Primary public artifact: `artifacts/evals/public_gate_eval_report_50.json`

## Safety and claim boundary

This draft is intentionally public-safe. It does not include raw dataset examples, raw attack text, raw model outputs, judge transcripts, raw-to-case mappings, external links, or live sink details. All dataset discussion is limited to opaque case counts, adapter status, aggregate metrics, rule identifiers, and category-level summaries already present in the public-safe report.

The current evidence supports a narrow claim: within the present controlled harness, structured WARDEN rules can be evaluated against a common normalized case envelope across synthetic fixtures and local private dataset adapters, and the current WARDEN rule set improves over the simple regex baseline on the available mixed run. It does not yet support a broad claim of general agent security, comprehensive ASB or AgentDefenseBench coverage, production readiness, or real-provider FIDES effectiveness.

## Working title

Controlled Evaluation of Structured Policy Rules and Information-Flow Judging for Pre-Context Agent Defense

## Draft paper outline

### Abstract

Summarize the problem of evaluating pre-context defenses for agent and MCP-style inputs without publishing unsafe source material. State the proposed harness: dataset adapters normalize synthetic fixtures and controlled local datasets into public-safe facts; a regex baseline, the WARDEN structured rule layer, and WARDEN plus FIDES are compared on the same cases. Report the current mixed-run result conservatively: WARDEN improves aggregate ASR over regex in the available public report, while FIDES adds no measured incremental catches in the current provider-disabled run. Emphasize limitations: sparse benign controls, incomplete ASB coverage, local private dataset dependence, and no real-provider FIDES evaluation.

### 1. Introduction

Motivate the need for repeatable, leakage-safe security evaluation for agent inputs before those inputs enter an agent context or influence tool use. Explain why raw adversarial examples and provider transcripts should not appear in public artifacts. Introduce the central research question:

Can a structured, defender-reviewable policy layer reduce attack success relative to a regex baseline on redacted multi-dataset facts, and can a later FIDES layer add incremental coverage for policy-relevant misses without exposing raw source material?

### 2. Threat model and public-safety model

Define the evaluated boundary as a pre-context gate over untrusted or dataset-local content. The harness assumes that adapters may inspect local source material under controlled custody, but public artifacts expose only structural facts, labels, opaque identifiers, rule IDs, and aggregate metrics. The current public report excludes case-level rows, source material, judge transcripts, and model outputs.

### 3. System overview

Describe the current harness components:

- Dataset adapters: synthetic fixtures are always available; ASB and AgentDefenseBench are optional controlled local datasets that require local roots and export only redacted facts.
- Normalized case envelope: each case carries dataset ID, split, attack or benign label, surface, category, safe features, policy context, and expected behavior.
- Regex baseline: a simple deterministic baseline over safe visible markers and redacted structural indicators.
- WARDEN: deterministic `.cwfr.yaml` structured rules over normalized facts and policy context.
- FIDES: a separate judge boundary with disabled, test-double, and provider-placeholder modes. Provider calls are disabled in the current public run.
- Public reporting: aggregate metrics only, with no raw source or transcript content.

### 4. Experimental setup

The current report is a controlled local multi-dataset run with 50 iterations per loaded case. The public artifact reports:

| Dataset adapter | Status in artifact | Unique cases | Case-iterations | Public interpretation |
|---|---:|---:|---:|---|
| synthetic | loaded | 4 | 200 | Public-safe structural fixtures for CI and rule regression. |
| ASB | loaded | 878 | 43,900 | Controlled local ASB-derived facts; raw source remains private. |
| AgentDefenseBench | loaded | 16,089 | 804,450 | Controlled local AgentDefenseBench-derived facts; raw source remains private. |
| total | loaded | 16,971 | 848,550 | Mixed controlled run, not a public raw dataset release. |

The artifact also reports zero provider calls. Therefore, any WARDEN-plus-FIDES metrics in this run should be read as WARDEN-equivalent unless future runs explicitly enable and validate a non-disabled FIDES mode.

### 5. Metrics

Use the public report definitions:

- Attack success rate, ASR: attack cases allowed divided by all attack cases.
- Recall: attack cases blocked or quarantined divided by all attack cases.
- Benign refusal rate: benign cases blocked or quarantined divided by all benign cases.
- Safe pass-through rate: benign cases allowed divided by all benign cases.
- Incremental WARDEN catches versus regex: attack case-iterations allowed by regex but blocked by WARDEN.
- Incremental FIDES catches versus WARDEN: attack case-iterations allowed by WARDEN but blocked by WARDEN plus FIDES.

Because the current report has only 50 benign case-iterations, benign impact metrics are preliminary and should not be generalized.

### 6. Current aggregate results

The public-safe report gives the following aggregate security metrics:

| Stack | ASR | Recall | F1 | TP | FN | FP | TN | Benign refusal rate | Safe pass-through rate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| no guard | 1.0000 | 0.0000 | 0.0000 | 0 | 848,500 | 0 | 50 | 0.0000 | 1.0000 |
| regex baseline | 0.9968 | 0.0032 | 0.0065 | 2,750 | 845,750 | 0 | 50 | 0.0000 | 1.0000 |
| WARDEN structured rules | 0.9549 | 0.0451 | 0.0863 | 38,250 | 810,250 | 0 | 50 | 0.0000 | 1.0000 |
| WARDEN plus FIDES | 0.9549 | 0.0451 | 0.0863 | 38,250 | 810,250 | 0 | 50 | 0.0000 | 1.0000 |

The report also gives:

| Incremental metric | Count |
|---|---:|
| WARDEN incremental catches versus regex | 35,500 |
| FIDES incremental catches versus WARDEN | 0 |
| Provider calls | 0 |
| Current WARDEN rule count | 8 |

### 7. Results narrative

#### 7.1 Aggregate pattern

The controlled mixed run shows a measurable difference between the regex baseline and WARDEN. The regex baseline blocks 2,750 attack case-iterations, while WARDEN blocks 38,250. In the same aggregate denominator, ASR decreases from 0.9968 under regex to 0.9549 under WARDEN, and the public report attributes 35,500 additional attack case-iterations to WARDEN catches over regex.

This is encouraging harness evidence for structured rules, but it is not yet strong thesis evidence. The remaining ASR is high at 0.9549, which means the majority of attack-labeled case-iterations are still allowed. The current WARDEN result demonstrates that the structured rule engine is connected to the multi-dataset runner and can catch mapped structural categories; it does not demonstrate broad dataset coverage.

#### 7.2 Synthetic tier

The synthetic tier is the strongest current regression signal because it is hand-authored to exercise known structural policy shapes and contains no raw external dataset material. In the current run, synthetic contributes 200 case-iterations, with 150 blocked or quarantined under WARDEN plus FIDES. This is consistent with three attack-like synthetic fixtures and one benign control repeated 50 times.

Allowed claim: the schema, adapters, WARDEN rule execution, public report generation, and safety boundaries work on deterministic public-safe fixtures.

Disallowed claim: synthetic results do not establish real-world effectiveness or coverage against ASB or AgentDefenseBench distributions.

#### 7.3 Controlled local ASB tier

The ASB adapter loaded 878 controlled local cases, producing 43,900 case-iterations. WARDEN plus FIDES blocked or quarantined 50 of those case-iterations. The maintainability section reports ASB coverage by one current rule ID. This indicates that ASB is mostly a coverage gap in the present harness.

Allowed claim: ASB-derived facts can be loaded through the controlled adapter and evaluated without exposing raw source material in the public artifact.

Disallowed claim: current ASB coverage is not sufficient to claim that WARDEN meaningfully secures ASB as a dataset. The current result is better characterized as a controlled gap analysis showing that ASB fact extraction and attack-to-rule mappings need further work.

#### 7.4 Controlled local AgentDefenseBench tier

The AgentDefenseBench adapter loaded 16,089 controlled local cases, producing 804,450 case-iterations. WARDEN plus FIDES blocked or quarantined 38,050 of those case-iterations. The public report shows rule coverage across several WARDEN rule IDs for this dataset.

Allowed claim: the adapter and normalized fact model can drive WARDEN decisions on a larger controlled local dataset, and some structural categories align with existing WARDEN rules.

Disallowed claim: the current artifact does not prove broad AgentDefenseBench robustness. The run is dominated by attack-labeled records, has very limited benign denominator, and should be repeated on frozen splits with richer benign near-miss controls before drawing paper-level conclusions.

#### 7.5 WARDEN interpretation

WARDEN is the deterministic structured rule layer. The current public report lists eight unique rule IDs and dataset-level rule coverage. The main current result is that WARDEN catches more attack case-iterations than the regex baseline while preserving the small available benign control set.

The more important scientific question is not raw block count alone, but whether WARDEN catches cases for defensible policy reasons that generalize across datasets. The current artifact begins to answer that question through rule IDs and aggregate category counts, but it still needs stronger attack-to-rule mapping evidence, richer ASB normalization, and larger benign controls.

#### 7.6 FIDES interpretation

The current public run does not measure real FIDES effectiveness. Provider calls are zero, transcripts are absent, and WARDEN plus FIDES has identical aggregate metrics to WARDEN. The report also shows zero FIDES incremental catches versus WARDEN.

This is the correct conservative interpretation: FIDES is present as a guarded interface and evaluation stack, but the current empirical result is provider-disabled. The local test-double mode can exercise interface behavior and public-safe reporting, but it should not be presented as an external judge result. The provider-placeholder mode marks the future integration boundary and does not perform provider calls. Future paper claims about FIDES require an explicitly configured, transcript-private, provider-enabled or otherwise validated judge run.

### 8. Limitations

1. Dataset custody and reproducibility: ASB and AgentDefenseBench are controlled local sources. The public report is reproducible only for users with equivalent local roots and configuration; raw source material is intentionally not committed.
2. Sparse benign evidence: the current aggregate has only 50 benign case-iterations. The zero false-positive count is therefore a smoke signal, not a reliable benign-disruption estimate.
3. High remaining ASR: WARDEN improves over regex in the mixed run but still allows most attack-labeled case-iterations.
4. ASB coverage gap: ASB currently contributes many attack iterations but almost no WARDEN catches.
5. Category heterogeneity: AgentDefenseBench-derived categories include broad safety and agent-security classes; current aggregate metrics should not be collapsed into a single universal security claim.
6. FIDES not empirically evaluated: disabled/test-double/provider-placeholder modes are useful for safety and interface testing, but they do not establish real judge performance.
7. No full agent runtime validation: the current gate evaluates normalized pre-context facts; it does not yet measure downstream agent task completion, tool execution, or recovery behavior in a full runtime.
8. No statistical uncertainty yet: the current deterministic repeated-run report lacks confidence intervals, split variance, and holdout confirmation.

### 9. Next required experiments

1. Freeze evaluation splits before additional tuning, with separate synthetic CI, controlled local development, controlled local test, and holdout partitions.
2. Expand ASB fact extraction so ASB cases map into policy-relevant categories rather than mostly falling through as uncovered dataset-native cases.
3. Complete and validate attack-to-rule mappings for every evaluated rule family, including expected-fire and should-not-fire cases.
4. Add benign near-miss controls at scale for each rule family and each major dataset surface.
5. Report WARDEN results by dataset, category, surface, and rule ID, with denominators large enough for interpretation.
6. Run FIDES test-double experiments only as interface and reporting validation, clearly separated from empirical judge claims.
7. Add a transcript-private provider-enabled FIDES experiment after safety review, reporting only aggregate call counts, costs, latencies, verdict distributions, and incremental catches.
8. Add latency measurements for normalization, regex, WARDEN, and FIDES stages.
9. Add statistical summaries for frozen test and holdout runs, including confidence intervals or bootstrap intervals where appropriate.
10. Maintain public artifact scans and manual leakage review before any public report or paper draft is shared.

### 10. Candidate paper contribution statement

A defensible future contribution would be:

We present a leakage-safe controlled harness for comparing regex baselines, structured WARDEN rules, and a separately gated FIDES judge boundary on normalized multi-dataset agent-security cases. Initial controlled results show that WARDEN is connected end-to-end and improves over a simple regex baseline on the current mixed local run, while also revealing substantial ASB coverage gaps and no current empirical FIDES gain because provider calls are disabled. The method emphasizes explicit custody boundaries, public-safe aggregate reporting, and attack-to-rule mappings as prerequisites for stronger future claims.

### 11. Additional post-draft progress

After the initial mixed run, the harness gained evidence-grade public diagnostics and a CI-safe FIDES test-double evaluation mode.

The evidence diagnostics add disagreement matrices, per-dataset and per-category rule coverage, rules-with-no-coverage counts, FIDES call/catch counters, and missing-prerequisite summaries. These additions make the public reports more useful for paper-oriented analysis because they show not just whether a stack blocked a case, but where the current coverage is missing and which rules are actually responsible for catches.

A separate FIDES test-double report now demonstrates the FIDES boundary on a deterministic WARDEN miss without provider calls or transcripts. In that synthetic public-safe run, WARDEN misses one attack-like fixture and the FIDES test-double blocks it, producing one FIDES incremental catch with zero provider calls. This is interface evidence only; it should not be described as empirical LLM judge performance. It does, however, prove that the harness can measure WARDEN-miss / FIDES-catch behavior once a real transcript-private judge is connected.

### 12. Current bottom line

The current harness is ready for an initial report draft, not a final paper claim. The public artifact shows meaningful engineering progress: multi-dataset adapters load controlled local ASB and AgentDefenseBench data, WARDEN executes real structured rules, public reports remain source-free, and aggregate WARDEN metrics improve over regex. The same artifact also makes the next research gap clear: ASB coverage is weak, benign controls are too sparse, and FIDES has not yet been empirically evaluated with a real judge beyond disabled or test-double boundaries.
