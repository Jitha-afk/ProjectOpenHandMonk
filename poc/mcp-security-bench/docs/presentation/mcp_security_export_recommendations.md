# Export Recommendations

Purpose: practical guidance for exporting the HTML deck or rebuilding it into PPT with minimal visual drift.

## 1) Recommended paths

### Best path: rebuild natively in PPT
Use the HTML deck as the design reference and rebuild the slides natively.
Why:
- editable text
- better projector behavior
- easier final touch-ups
- easier speaker note transfer

### Fast path: hybrid export
Use native PPT text for titles/body text and import selected visuals as images.
Best visuals to rasterize if needed:
- slide 1 orbit visual
- slide 17 containment rings
- slide 20 anatomy card stack if spacing drifts
- slide 21 right-side matrix block only

### Not recommended
- exporting the entire HTML deck as full-slide images for every slide
Why not:
- text becomes less editable
- citations can get too tiny
- projector scaling is less forgiving

## 2) Fonts and typography

Recommended PPT-safe font pairings:
- Aptos / Aptos Display
- Segoe UI / Segoe UI Semibold
- Calibri / Calibri Light
- Avenir Next if available

Approximate PPT font sizes
- Title slide title: 30–40 pt depending on line length
- Standard slide titles: 24–30 pt
- Body bullets: 16–20 pt
- Card labels: 14–18 pt
- Footer/citation text: 8–10 pt max

Rule:
If a cell or card needs to go below ~14 pt to fit, simplify the text instead.

## 3) Color and theme guidance

Preserve the current feel:
- dark navy / near-black dominant background
- white or near-white main text
- muted gray secondary text
- accent colors used sparingly: blue, cyan, green, amber, violet, red

Keep one dominant dark theme.
Do not convert this into a generic blue corporate deck.

## 4) Raster export recommendations

If you need images from HTML:
- export at 2x or 3x target resolution
- target at least 2560x1440 for slide artwork
- prefer PNG for diagrams and UI-like layouts
- prefer JPEG only for photo-heavy content (not applicable here)

When rasterizing only parts of slides:
- crop tightly to the visual block
- rebuild surrounding text in PPT natively
- avoid mixing fuzzy raster text with sharp editable text on the same block

## 5) Slide-specific export notes

Slides most likely to need special attention:
- Slide 1: maintain spaciousness; avoid cluttering with footer-heavy citations
- Slide 11: should remain highly visual and minimal
- Slide 19: make Day 1 baseline visually dominant
- Slide 20: preserve anatomy concept, not tiny-table concept
- Slide 21: verify matrix readability from the back of the room; shorten signal text further if needed
- Slide 22: protect whitespace and closing emphasis

## 6) Speaker note transfer guidance

For PPT notes pages:
- copy only the tightened presenter notes, not the full paper-grade explanation
- prefer:
  - core message
  - one story beat
  - one caution
  - transition line

Avoid pasting the full markdown talk track verbatim into PPT notes unless you want a teleprompter experience.

## 7) Venue / projector assumptions

Optimize for:
- medium-to-large room
- non-perfect projector contrast
- audience not reading dense cells from the back row

Therefore:
- keep matrix text as large as practical
- trim citations on-screen if needed
- avoid low-contrast gray helper text in final PPT
- make arrows and separators thicker than they look necessary on laptop screens

## 8) Final pre-presentation checklist

Before calling the PPT final:
- verify all 22 slides exist in order
- verify timings still total ~45 minutes
- verify no footer text collides with content
- verify slide 20 and 21 are readable from zoomed-out view
- verify closing slide has strong whitespace
- verify citations are either readable or intentionally moved to notes
- verify no placeholder styling or inconsistent fonts remain

## 9) If time is very limited

Minimal viable PPT conversion:
1. rebuild slides 1, 4, 11, 19, 20, 21, 22 carefully
2. simplify remaining slides into clean 2-column PPT slides
3. move detailed citations to notes
4. do one zoomed-out review for room readability

That will preserve most of the talk’s value even under deadline pressure.
