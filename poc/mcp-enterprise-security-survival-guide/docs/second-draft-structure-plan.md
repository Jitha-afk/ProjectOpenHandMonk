# Second-draft narrative revision plan

Goal: turn the first draft from a comprehensive catalog into a tighter argument: what MCP changes for enterprises, which risk scenarios matter most, which control stack follows from those risks, and what still remains unvalidated.

## Recommended second-draft spine
1. Abstract
2. Introduction: problem, scope, and contributions
3. MCP deployment surfaces that change enterprise risk
4. Enterprise risk scenarios
5. Enterprise control priorities and rollout guidance
6. Methods and evidence boundaries
7. Limitations
8. Conclusion

## Structural edits

1. Use `opening-draft.md` as the canonical front end.
   - Replace the current Abstract and early framing in Sections 1-3 with the tighter setup already present in `opening-draft.md`.
   - Keep one concise contribution list at the end of the Introduction.
   - Cut repeated caveats about evidence posture that currently recur across the abstract, introduction, Section 3, and Section 7.
   - Result: the paper reaches its core argument faster.

2. Separate introduction work from threat-model work.
   - End the Introduction with scope, contribution, and reader promise.
   - Make Section 3 about assets, adversaries, trust boundaries, and evaluation focus only.
   - Remove the repeated “paper contributions” material from the threat-model section.
   - Result: cleaner handoff from setup to analysis.

3. Make Section 4 the main narrative hinge.
   - Keep the scenario families from `section-4-risk-scenarios.md` as the paper’s primary story arc.
   - End each scenario with one explicit control question that the next section answers.
   - Reuse those same scenario labels inside the controls section instead of re-explaining the threats from scratch.
   - Result: less repetition and a stronger throughline from risk to response.

4. Merge the overlapping material in Sections 5, 6, and 8 into one operational section.
   - Build one section titled along the lines of “Enterprise control priorities and rollout guidance.”
   - Sequence it as: control principles -> layered control stack -> minimum pilot baseline -> phased rollout -> trade-offs.
   - Keep only the most distinctive forward-looking patterns from current Section 6 as short subsections or callout boxes, rather than a full separate section.
   - Result: removes the current three-pass repetition over controls, rollout, and guidance.

5. Compress methods so they support the narrative instead of interrupting it.
   - In main text, keep only the method posture, first-wave validation tracks, and explicit evidence-boundary summary from `section-7-methods-and-evaluation.md`.
   - Move the detailed lab topology, full attack corpus, metrics tables, provisional thresholds, and formal-core mechanics out of the body.
   - Result: the paper stays rigorous without reading like an internal validation memo.

6. Move project scaffolding out of the manuscript body.
   - Remove the working bibliography/source inventory from the main narrative.
   - Strip out inline source-ID parentheticals and other research-ledger artifacts where normal citations will suffice.
   - Keep only a short evidence-tag note up front; place extended source mapping and working reference lists elsewhere.
   - Result: the second draft reads like a paper for readers, not a repository snapshot.

## Main text vs appendix / companion docs

### Keep in the main text
- Problem statement, scope, and bounded contribution
- Latest-spec deployment surfaces that materially change enterprise risk
- The core enterprise risk scenarios
- One integrated control-and-rollout section
- A short methods and evidence-boundary section
- Limitations and conclusion

### Move to an appendix or companion doc
- Full lab topology
- Attack corpus inventory
- Metrics and threshold tables
- Formal-core validation details
- Extended implementation-pattern detail from current Section 6
- Working bibliography, source ledger, and source-ID mapping

## Execution order
1. Rebuild the opening from `opening-draft.md`.
2. Re-outline the manuscript to the eight-part spine above.
3. Use Section 4 scenario headings as anchors for the controls section.
4. Merge Sections 5, 6, and 8; cut duplicate lists and repeated baseline guidance.
5. Shorten Section 7 in the main text and relocate detail.
6. Remove bibliography/scaffolding material from the manuscript body and clean transitions.
