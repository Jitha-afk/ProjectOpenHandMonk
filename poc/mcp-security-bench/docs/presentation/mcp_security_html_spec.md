# MCP Security HTML Deck Implementation Spec

Purpose: implementation blueprint for a self-contained HTML keynote deck for the talk "S in MCP stands for Security." This spec matches the revised, peer-review-driven session structure and should be treated as the design reference for `index.html`.

## 1) Narrative structure

The deck should not read like an incident parade.
It should follow this keynote spine:
1. MCP is a delegated-authority system, not just a protocol.
2. Public enterprise guidance is useful as a bounded reference pattern.
3. Failures should be compressed into three buckets, not many separate incident slides.
4. The main reusable artifact is a five-control-plane rollout model.
5. The second reusable artifact is an MCP Delegated-Authority Matrix.
6. The close should push the audience toward one workflow, one risky path, one fix.

The two memorable artifacts the audience should leave with are:
- a five-control-plane MCP rollout checklist
- an MCP Delegated-Authority Matrix

Transcript-derived incidents remain valid supporting examples, but they should not determine the structure or voice of the session.

## 2) Slide ID plan for the current 24-slide deck

- `s01-title` — title / thesis
- `s02-why-now` — operational urgency
- `s03-microsoft-pattern` — Microsoft published reference pattern
- `s04-delegated-authority` — original framing: MCP as delegated authority
- `s05-execution-loop` — discover / select / approve / invoke / return / retain
- `s06-tool-contract` — secure tool contract, schemas, and errors
- `s07-exposure-bucket` — exposure and sample-code failures
- `s08-authority-bucket` — delegated-authority failures
- `s09-context-bucket` — context and trust failures
- `s10-benchmark` — why simple defenses still miss attacks
- `s11-control-planes` — five control planes photo slide
- `s12-ownership` — rollout ownership model
- `s13-architecture-plane` — secure deployment pattern choice
- `s14-tool-admission` — tool admission and provenance
- `s15-identity-plane` — brokered identity and approval
- `s16-validation-plane` — validate schemas, outputs, and errors
- `s17-containment-plane` — containment and observability
- `s18-continuous-validation` — logic / protocol / agent testing
- `s19-roadmap` — day-1 baseline and 90-day roadmap
- `s20-matrix` — matrix anatomy
- `s21-worked-example` — read path and write path matrix examples
- `s22-closing` — final call to action
- `s23-appendix-figure2` — enterprise paper Figure 2 reference framework
- `s24-appendix-table1` — enterprise paper Table I threat/control summary

## 3) Visual system

Keep the keynote-style visual language:
- dark-first deck with a few light reset slides
- high contrast
- large typography
- editorial spacing
- CSS-only gradients and simple diagram shapes
- no external assets, frameworks, or fonts

Recommended slide rhythm:
- thesis
- architecture / framing
- compact failure buckets
- photo slide + ownership
- control planes
- baseline / roadmap
- matrix anatomy + examples
- closing CTA

## 4) Design requirements for originality

- Do not visually imply that the deck is a retelling of another speaker’s talk.
- Compress incident material into broader buckets and shift emphasis to governance and control planes.
- Ensure the checklist and matrix slides feel like original deliverables, not summary slides.
- Favor Jitesh’s voice as an operator / enterprise security engineer.
- Keep transcript-backed examples short and subordinate to the control-plane narrative.
- Use the uploaded example matrix slides only for structural inspiration.
- Our matrix should differ structurally by being keynote-friendly, flatter, and easier to read on a projector.

## 5) Citation and notes model

- Use compact citation rails in each slide footer.
- Use transcript-backed citations only where needed and label them clearly as transcript-backed rather than as broad public claims.
- Do not reference the inspiration slides directly in the on-screen deck.
- Keep notes in `<aside class="notes">` blocks.
- Notes should emphasize delivery, framing, and source-safety reminders.

## 6) Component expectations in HTML

Current reusable primitives expected in the deck:
- `.mini-cards`
- `.metric-strip`
- `.timeline`
- `.chain`
- `.check-routes`
- `.layer-stack`
- `.pillar-grid`
- `.containment-rings`
- `.stage-grid`
- `.phase-grid`
- `.matrix-table`

The matrix implementation should be different from dense appendix tables.
Use one slide to explain the fields and one slide to show two example rows.

## 7) Interaction model

Preserve the current minimal inline-JS interaction model:
- next / previous with arrows, page keys, and space
- `Home` / `End`
- `n` for notes
- `c` for citation expansion
- `f` for fullscreen
- click right half to advance, left half to go back
- hash-based deep linking to slide IDs

## 8) Implementation constraints

- No external fonts, JS libraries, CSS frameworks, or image assets.
- Build for 1920x1080 first, but keep text readable on smaller screens.
- Keep the whole deck in one editable HTML file.
- `mcp_security_presentation.html` should remain a redirect wrapper to `index.html`.
- The HTML should remain suitable for later conversion into PPT.

## 9) Quality bar

Before the deck is considered final:
- verify there are 24 slides total (22 main + 2 appendix)
- verify every slide has notes and a footer
- verify titles broadly match the markdown manifest structure
- verify citations are present but not overwhelming
- verify visible text is materially lighter than the earlier revision
- verify the matrix reads clearly from a projector and is not a dense appendix clone
- verify appendix Figure 2 and Table I are clearly labeled as reference material, not main-talk artifacts
- verify the deck feels like an original Jitesh keynote, not a paraphrase with new wording
