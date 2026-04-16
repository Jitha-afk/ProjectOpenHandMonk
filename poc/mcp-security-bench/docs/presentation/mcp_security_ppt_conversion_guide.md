# PPT Conversion Guide

Session: S in MCP stands for Security
Presenter: Jitesh Thakur
Source of truth for visual structure: `index.html`

Goal: rebuild the deck as a native PPT while preserving the keynote feel and projector readability.

## Overall conversion rules

- Target canvas: 16:9 widescreen
- Keep slide count at 22
- Prefer editable native text over screenshots
- Recreate shapes, cards, and grids natively where feasible
- Avoid importing whole-slide screenshots unless under time pressure
- If you must use screenshots, do it only for:
  - orbit slide artwork
  - containment rings
  - matrix/example micro-layouts
- Keep slide footers smaller than in HTML; in PPT they can move into speaker notes if the venue does not require citations on-screen
- Keep citations concise on slides and put fuller attribution in notes or backup appendix if needed

## Slide-by-slide conversion guidance

### Slide 1 — Title / thesis
PPT build:
- dark full-bleed background
- large title
- one thesis line only
- optional orbit visual at right
Keep editable:
- title
- thesis line
Can rasterize if needed:
- orbit visual
Presenter priority:
- make this feel spacious, not informational

### Slide 2 — Why this matters now
PPT build:
- 2-column layout
- left: short objective sentence + 3 bullets
- right: 3 metric cards
Keep editable:
- all text
Notes:
- this slide should stay light and fast

### Slide 3 — Microsoft reference pattern
PPT build:
- light slide
- left: 3 bullets
- right: layered stack diagram
Keep editable:
- all text
Can recreate natively:
- stacked layers as rounded rectangles
Notes:
- say “published reference pattern,” not “industry standard” or “proof”

### Slide 4 — Delegated authority
PPT build:
- 2-column layout
- left: 3 bullets
- right: 5-card chain
Keep editable:
- all text
Native recreation recommended:
- five rounded rectangles with arrows between them
This is a signature slide; make it look premium.

### Slide 5 — Execution loop
PPT build:
- one strong title
- six equally spaced step cards across the slide or 2x3 if needed
Keep editable:
- all text
Priority:
- readability over strict HTML fidelity

### Slide 6 — Tool contract
PPT build:
- left bullets
- right four stacked route cards
Keep editable:
- all text
Goal:
- emphasize “task-oriented” and “structured outputs” visually

### Slide 7 — Exposure + sample-code bucket
PPT build:
- left short bullets
- right 4-step horizontal timeline
Keep editable:
- all text
Compression note:
- do not add extra incident detail in PPT

### Slide 8 — Delegated-authority failures
PPT build:
- left short bullets
- right 4-card chain
Keep editable:
- all text
Tip:
- make arrows bold enough for projection

### Slide 9 — Context and trust failures
PPT build:
- left short bullets
- right 4-card flow
Keep editable:
- all text
Tip:
- prioritize the “trust abuse” concept visually

### Slide 10 — Why simple defenses still miss attacks
PPT build:
- left concise bullets
- right 3 metric cards
Keep editable:
- all text
Tip:
- keep this slide light; it is a bridge slide

### Slide 11 — Five control planes photo slide
PPT build:
- minimal text
- five large labeled cards only
Keep editable:
- title and labels
Do not overload this slide in PPT.
This is meant to be photographed.

### Slide 12 — Who owns what
PPT build:
- left: role bullets
- right: 4 owner cards / swimlane-style blocks
Keep editable:
- all text
Optional improvement:
- color-code owner groups subtly if done consistently

### Slide 13 — Secure deployment patterns
PPT build:
- left bullets
- right layered architecture stack
Keep editable:
- all text
Native shapes recommended.

### Slide 14 — Tool admission and provenance
PPT build:
- left bullets
- right 3-4 route cards
Keep editable:
- all text
Tip:
- emphasize registry / provenance / recertification

### Slide 15 — Brokered identity and approval
PPT build:
- left bullets
- right 2x2 pillar grid
Keep editable:
- all text
Tip:
- make “Approval” visually strong

### Slide 16 — Validate inputs, outputs, and errors
PPT build:
- left bullets
- right 3 route cards
Keep editable:
- all text
Keep this slide compact.

### Slide 17 — Containment and observability
PPT build:
- left bullets
- right containment rings graphic
Keep editable:
- text
Can rasterize if needed:
- ring graphic
Native recreation option:
- three concentric circles with labels

### Slide 18 — Continuous validation
PPT build:
- left bullets
- right 3 metric cards: Logic / Protocol / Agent
Keep editable:
- all text
This should feel practical and neat.

### Slide 19 — Day-1 baseline and 90-day roadmap
PPT build:
- 3 large cards across the slide
Keep editable:
- all text
Tip:
- make Day 1 visually dominant over the other two

### Slide 20 — Matrix anatomy
PPT build:
- left bullets
- right 4 stacked anatomy cards
Keep editable:
- all text
Important:
- do NOT convert this into a tiny table in PPT
- keep it as anatomy, not appendix

### Slide 21 — Matrix examples
PPT build:
- left concise bullets
- right compact 2-row matrix
Keep editable:
- all text if possible
Fallback:
- if recreating matrix precisely is too slow, use a high-res crop/screenshot for the right panel only, not the full slide
Tip:
- ensure Priority column remains visible
- if needed, shorten Signal text further in PPT

### Slide 22 — Closing
PPT build:
- dark slide
- strong closing line
- 3 action cards
Keep editable:
- all text
This is the final memory slide. Give it space.

## PPT-specific improvements allowed

You can improve on the HTML deck during conversion if the change improves projector readability without changing meaning:
- reduce footer/citation prominence
- enlarge key matrix/example text
- add subtle color emphasis to P0 on slide 21
- simplify arrows or icons that may not project cleanly
- rebalance columns for room readability

## Do not change during conversion

- central thesis: MCP as delegated authority
- five control planes
- day-1 baseline emphasis
- two-part matrix sequence (anatomy + examples)
- final closing line:
  “If your model can reach it, your security model must explain it.”
