# Executive Summary

## Purpose of this project
The AI Model Vulnerability Corpus is a research-first effort to build a source-backed set of candidate AI model artifacts and model-adjacent packages for later controlled-lab testing. The immediate objective is not to download or execute suspicious content at scale. The objective is to identify which artifact types and candidate samples are credible, practical, and safe enough to support future evaluation of Microsoft Defender for Cloud model security capabilities.

In short, this project creates a decision framework before any high-risk testing workflow is operationalized.

## What the project is expected to produce
The documented deliverables are:
- a candidate inventory with source support and confidence notes
- a format coverage matrix to show which artifact types can be exercised later
- a lab-safety and legality view to determine what can be handled directly versus reconstructed
- operator-facing documentation for safe evaluation and decision-making

These outputs are intended to reduce ambiguity in later test planning. They help decision-makers avoid two common failures:
- overcommitting to risky real-world samples when safer fixtures would be sufficient
- overstating the importance of weakly supported candidates just because they are publicly discussed

## What this project does not claim
This project does not claim that every listed candidate is malicious, available, or appropriate to acquire.
It does not by itself validate product efficacy.
It does not authorize execution of untrusted artifacts outside a controlled environment.
It does not replace legal, policy, or operational approvals.

## How Alan’s findings should be interpreted
Alan’s work is the evidence layer.

Decision-makers should read Alan’s output as a source-backed assessment of which candidate artifacts or artifact classes are worth considering. The key value is provenance, reproducibility, and confidence discipline. Alan’s findings should help answer questions such as:
- Is there a credible source for this candidate?
- Is the unsafe behavior or risk pattern clearly described?
- Is there enough specificity to justify follow-on handling?
- Is this a real artifact, a documented pattern, or only a weak rumor?

Alan’s findings should not be interpreted as operational approval to download, run, or redistribute a sample. Strong research support increases confidence in relevance, not permission for handling.

## How Turing’s findings should be interpreted
Turing’s work is the testability and coverage layer.

Decision-makers should read Turing’s output as an engineering assessment of whether a candidate can be translated into a safe, useful, and format-aligned test fixture. The key value is practicality. Turing’s findings should help answer questions such as:
- Does this candidate map to the supported artifact classes under evaluation?
- Does it improve coverage in a meaningful way?
- Can the scenario be tested with a synthetic or reconstructed fixture instead?
- What handling controls are required for safe lab use?

Turing’s findings should not be interpreted as proof that a candidate is important in the wild. A candidate can be easy to test and still be low-value if the evidence base is weak.

## How to combine Alan and Turing for decisions
A decision-maker should treat the two streams as complementary gates:
- Alan answers whether a candidate is well justified.
- Turing answers whether the candidate is safely and usefully testable.

The best candidates are those that clear both gates.

### High-confidence decision pattern
Proceed toward controlled-lab use when:
- provenance is credible
- the artifact or pattern is concrete enough to reproduce or review
- the format mapping is meaningful
- the handling path is legal, controlled, and practical
- the candidate adds distinct coverage

### Caution pattern
Use synthetic or reconstructed fixtures when:
- the real sample is unavailable
- licensing or redistribution is unclear
- the real artifact would introduce unnecessary operational risk
- the target behavior can be represented safely without the original sample

### Reject or defer pattern
Do not prioritize a candidate when:
- evidence is weak or ambiguous
- it duplicates existing coverage
- safe handling is not supportable
- the expected value is lower than the operational burden

## Expected value for leadership and product stakeholders
For leadership, the value of this project is disciplined test selection. It creates a documented basis for deciding what should enter a lab and why.

For product stakeholders, the value is cleaner future evaluation. Instead of testing against an ad hoc collection of suspicious files, teams can work from a curated set of candidate classes, provenance notes, and format-driven gaps.

For operators, the value is safety and repeatability. The project encourages using the smallest defensible set of fixtures and prefers reconstructed samples when real-world artifacts are unnecessary or unsafe.

## Recommended reading of later results
When later testing begins, interpret outcomes in this order:
1. Did the project select candidates with credible support?
2. Did the selected fixtures cover the relevant artifact classes and packaging patterns?
3. Were the samples handled in a controlled and policy-aligned way?
4. Did the resulting tests generate decision-useful product evidence?

This order matters. Product signal is only meaningful if the input set was selected and handled responsibly.

## Bottom line
This project is intended to make future model-security testing more credible, safer, and easier to govern. Its success should be measured by the quality of the selection framework and the defensibility of the resulting fixture set, not by the volume of risky artifacts collected.

The core decision rule for leaders is simple: treat Alan’s findings as relevance evidence, treat Turing’s findings as feasibility evidence, and approve only the candidates that are both justified and safe to operationalize in a controlled lab.