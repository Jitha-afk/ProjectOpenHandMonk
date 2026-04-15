# Project Brief — Issue #6

Project: `poc/mcp-enterprise-security-survival-guide`
Issue: `#6` — [Idea] Create Enterprise Security Survival Guide for latest MCP specification
Branch: `issue-6-mcp-enterprise-security-survival-guide`

## Problem Statement
MCP is moving quickly from experimentation into real integration scenarios, but enterprise security guidance is still fragmented. The existing literature appears strong on attack discovery and early benchmarks, yet weaker on spec-aware deployment controls, operational architecture, and narrowly provable enforcement mechanisms that enterprises can actually adopt.

## Goal
Produce an evidence-grounded enterprise MCP security guide that combines:
- literature synthesis,
- deployable defensive architecture,
- a concrete validation plan,
- targeted proof-of-concept defenses,
- and a publishable paper draft with explicit claim hygiene.

## In Scope
- Latest-spec-focused MCP security analysis using the issue’s cited spec version (`2025-11-25`)
- Source inventory and gap analysis from `/home/sealjitha/toresearch`
- Enterprise threat model and control framework
- Testable defense proposals and validation criteria
- Narrow formal-methods plan for a security-critical control core
- Draft paper structure, figure plan, and publication workflow

## Out of Scope
- Claiming whole-ecosystem formal security proofs
- Shipping a production-ready enterprise MCP platform in the first pass
- Publishing strong results before corresponding experiments exist
- Treating generic LLM security guidance as MCP-specific evidence without qualification

## Initial Hypothesis
The strongest contribution is unlikely to be “MCP is insecure.” The likely contribution is a spec-aware enterprise control model that shows which defenses are mandatory, which are optional, and which can be validated through replayable proofs of concept and a small machine-checkable enforcement core.

## Workstreams
### 1. Research workstream
Owner: Alan
Outputs:
- `research/source-inventory-and-gap-analysis.md`
- later source memos, claim inventory, and threat taxonomy notes
Questions:
- What is already established in the literature?
- Where are the real enterprise guidance gaps?
- Which latest-spec features are underexplored?

### 2. Validation and prototype workstream
Owner: Turing
Outputs:
- `design/validation-and-poc-plan.md`
- later threat model, formal properties, replay fixtures, prototype defenses
Questions:
- Which defenses can be tested credibly in this repo?
- What metrics define success or failure?
- What “mathematically provable code” is realistic here?

### 3. Paper and publication workstream
Owner: Mira
Outputs:
- `docs/paper-blueprint.md`
- later manuscript drafts, figure captions, publication packages
Questions:
- How should evidence be separated from hypotheses?
- What paper structure best serves both enterprise practitioners and research readers?
- Which figures most improve comprehension without overclaiming?

### 4. Orchestration workstream
Owner: Hermes
Outputs:
- branch management, issue updates, PR hygiene, cross-workstream synthesis
Questions:
- Which claims deserve prototype attention first?
- When is the project ready for a draft PR versus an external paper draft?
- Where should scope be narrowed to keep the work rigorous?

## Recommended First-Wave Claims
1. Origin validation and localhost-only binding reduce exposure for local Streamable HTTP MCP servers.
2. Per-user scoped authorization reduces blast radius compared with shared static credentials.
3. Client-side roots enforcement can prevent out-of-scope file access under malicious guidance.
4. Elicitation restrictions plus disclosure/consent controls can reduce credential-harvesting risk.
5. Provenance- and trust-aware policies can reduce cross-server escalation and exfiltration.
6. Private registry allowlisting plus signed metadata improves resistance to malicious server onboarding.

## Success Criteria for the Kickoff Phase
- Project workspace exists and is scoped
- Research intake memo exists
- Validation/POC plan exists
- Paper blueprint exists
- Issue is marked in progress and linked to the branch/PR workflow

## Risks
- MCP spec and implementation ecosystem may continue to change during drafting
- Literature may over-index on attacks relative to deployable defenses
- “Novel techniques” pressure may tempt overclaiming without experiments
- Formal-methods ambitions could sprawl unless the proof surface stays narrow

## Immediate Next Steps
1. Normalize the literature into a claims ledger with citation status.
2. Write the project threat model and attack/control matrix.
3. Select 2–3 first prototype tracks rather than trying to build every defense idea at once.
4. Open a draft PR with kickoff artifacts so progress is reviewable.
5. Begin evidence-backed drafting only where claims can be tagged as cited, lab-backed, or hypothesis.
