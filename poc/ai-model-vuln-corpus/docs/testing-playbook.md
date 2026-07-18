# Testing Playbook

## Purpose
This playbook explains how to use the AI Model Vulnerability Corpus in a later controlled lab. It is written for operators who need to turn the project outputs into a safe, repeatable evaluation workflow without overstating what the corpus proves.

This project is research-first. The corpus is intended to help teams choose and stage candidate model artifacts for later product testing against Microsoft Defender for Cloud model security features. It is not a license to broadly collect, execute, or redistribute unsafe artifacts.

## Who this is for
- Security engineers building isolated test workflows
- Product evaluators validating model security detections and handling
- Red-team or adversary-simulation staff working inside approved lab conditions
- Program managers and reviewers who need a common operating model for later test phases

## What the corpus is and is not
The corpus is:
- a source-backed inventory of candidate artifacts
- a decision framework for selecting useful fixtures
- a way to map candidate artifacts to later test coverage by format and risk type
- a planning aid for controlled-lab evaluation

The corpus is not:
- proof that every listed candidate is malicious
- a downloader, scanner, or execution harness
- a production control recommendation by itself
- an approval to move risky artifacts into shared environments

## Intended use in a controlled lab
Use the corpus to answer four practical questions before testing begins:
1. Which candidate artifacts have credible provenance?
2. Which candidates fit the model or model-adjacent formats the product is expected to inspect?
3. Which candidates can be handled legally and safely in an isolated environment?
4. Which gaps should be filled with reconstructed or synthetic fixtures instead of real-world samples?

The right outcome is a small, justified test set with clear provenance and handling rules, not the largest possible collection.

## How to interpret candidate classes
Candidate classes are screening categories, not verdicts. They help operators decide how much trust to place in a sample, what controls are needed, and whether a real artifact or a synthetic stand-in is more appropriate.

### 1. Intentionally vulnerable demonstration models or model packages
Interpretation:
- Usually strong for repeatable testing because they are designed to illustrate a known weakness.
- Often safer and easier to justify than opaque internet samples.
- Best used to validate whether the test pipeline can recognize and process known-bad or known-unsafe patterns.

Operational note:
- Prefer these first when building a baseline test suite.

### 2. Malicious pickle/joblib/dill/torch artifacts used in security demonstrations
Interpretation:
- High-interest because they represent realistic unsafe deserialization and embedded-code risk.
- High-handling sensitivity because serialization behavior may cross into code execution if treated carelessly.
- Require the strictest containment and the clearest provenance review.

Operational note:
- Do not treat “publicly discussed” as equivalent to “safe to obtain or run.”

### 3. Unsafe checkpoint or config packaging patterns discussed by researchers
Interpretation:
- Useful for format and packaging-path coverage even when the artifact is not a confirmed malicious sample.
- Good for testing whether inspection logic catches risky structure, metadata, or packaging combinations.
- May be better represented as reconstructed fixtures than as live third-party artifacts.

Operational note:
- These are often best used to test policy and inspection breadth, not only maliciousness.

### 4. Model-adjacent artifacts Defender should inspect
Interpretation:
- Includes weights, configs, serialized preprocessing pipelines, tokenizers, and metadata bundles.
- Important because real model risk can live outside the primary weight file.
- Strong candidates improve ecosystem coverage even if they are not standalone models.

Operational note:
- Keep these attached to a clear scenario so operators know what part of the supply chain is being tested.

### 5. Reconstructed or synthetic fixtures
Interpretation:
- Preferred when real samples are unavailable, legally unclear, unsafe to redistribute, or too operationally risky.
- Good for repeatability, documentation, and controlled coverage.
- Should be labeled clearly so later readers do not mistake them for in-the-wild artifacts.

Operational note:
- Synthetic does not mean low value. In many cases it is the most responsible way to test a class of behavior.

## What not to do
Do not:
- mass-download random model artifacts from the internet
- execute untrusted artifacts on a workstation, shared server, or production-connected environment
- redistribute harmful payloads or unclear third-party samples
- label a candidate as confirmed malicious without source-backed evidence
- bypass legal, licensing, or terms-of-use review
- assume a format match alone makes a candidate worth testing
- collapse research confidence, operational safety, and product severity into one score

## Safe evaluation workflow
The workflow below is the minimum safe path from research output to usable lab fixture.

### Phase 1: Intake and triage
1. Start from Alan’s source-backed candidate inventory.
2. Record provenance, claimed risk type, artifact references, and confidence notes.
3. Reject any item that lacks enough detail to support later review.
4. Flag items with legal, licensing, or redistribution uncertainty for separate review.

Exit criterion:
- Candidate list is evidence-backed and ready for format and handling assessment.

### Phase 2: Format and testability review
1. Use Turing’s format matrix to determine whether the candidate maps directly or indirectly to the supported artifact classes under evaluation.
2. Identify whether the candidate tests a primary model artifact, a packaging pattern, or a model-adjacent component.
3. Mark whether a real sample is necessary or whether a reconstructed fixture would satisfy the same objective.
4. Remove duplicates that do not improve coverage.

Exit criterion:
- Each retained candidate has a clear reason for inclusion and a defined coverage objective.

### Phase 3: Safety and legality gate
1. Review handling risk, redistribution limits, and environment requirements.
2. Decide one of three dispositions:
   - approved for isolated lab acquisition
   - use synthetic/reconstructed fixture instead
   - reject from scope
3. Document why the decision was made.

Exit criterion:
- No sample moves forward without an explicit handling decision.

### Phase 4: Fixture preparation
1. Prepare the smallest artifact set needed to exercise the scenario.
2. Store artifacts only in an approved isolated location.
3. Label each item with provenance, candidate class, intended test, and containment notes.
4. Keep synthetic fixtures separate from third-party artifacts.

Exit criterion:
- Fixtures are staged, labeled, and traceable.

### Phase 5: Controlled execution planning
1. Define what the product is expected to inspect, block, flag, or log.
2. Run only inside isolated lab conditions with approved rollback and cleanup steps.
3. Observe handling behavior, inspection coverage, and operational usability.
4. Capture evidence without exporting risky artifacts into normal collaboration channels.

Exit criterion:
- Test evidence is collected safely and can be reviewed without re-handling the original sample.

### Phase 6: Review and decision support
1. Compare outcomes against the original objective for each candidate.
2. Separate these questions in reporting:
   - Was the candidate well supported by evidence?
   - Was it safe and practical to stage?
   - Did it improve test coverage?
   - Did it produce a meaningful product signal?
3. Retire low-value fixtures and keep only those that add repeatable coverage.

Exit criterion:
- The retained corpus supports future testing without uncontrolled growth.

## Decision guidance for operators
Prefer a candidate when it has most of the following:
- credible provenance
- concrete artifact or reproducible package reference
- a clear unsafe behavior or supply-chain risk pattern
- fit to a supported model or model-adjacent format
- a practical handling path that stays within law, policy, and lab rules

Prefer a reconstructed fixture when:
- the original artifact is unavailable
- the legal status is unclear
- redistribution would be irresponsible
- the same behavior can be tested safely without the real sample

Reject a candidate when:
- its provenance is weak
- the handling path is not supportable
- it duplicates existing coverage
- it would create more operational risk than evaluation value

## How to read later findings from Alan and Turing
Use Alan’s work to answer: “Why do we believe this candidate matters?”
Use Turing’s work to answer: “Can we test it safely and does it improve format coverage?”

Do not use either stream alone to approve a sample. A strong candidate needs both:
- evidence that the artifact class is relevant
- an operationally sound path to controlled testing

## Recommended reporting language
When describing results, use careful wording such as:
- “candidate suitable for controlled evaluation”
- “source-backed unsafe pattern”
- “reconstructed fixture recommended for coverage”
- “not approved for acquisition due to handling or legality constraints”

Avoid wording that implies certainty without support, such as:
- “confirmed malicious”
- “safe to run”
- “representative of all model threats”

## Bottom line
The corpus should be used as a governed intake and selection mechanism for later lab testing. Success is not collecting the most dangerous artifacts. Success is selecting a defensible, traceable, and safe set of fixtures that meaningfully exercises model security inspection pathways.