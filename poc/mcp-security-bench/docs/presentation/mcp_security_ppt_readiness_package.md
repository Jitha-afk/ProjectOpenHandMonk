# PPT Readiness Package

Purpose: make the HTML keynote package easy to convert into a polished `.pptx` later without losing the narrative, pacing, or visual identity.

Canonical source files:
- HTML deck: `index.html`
- Slide manifest: `mcp_security_slide_manifest.md`
- Full talk track: `mcp_security_talk_track.md`
- Paper: `mcp_security_paper.md`

This package adds three conversion-oriented artifacts:
- `mcp_security_ppt_conversion_guide.md`
  - slide-by-slide PPT conversion guidance
- `mcp_security_export_recommendations.md`
  - export, rasterization, font, and layout recommendations
- `mcp_security_presenter_notes_day_of.md`
  - tightened speaker notes for presentation day use

Recommended conversion strategy:
1. Use the HTML deck as the visual reference, not as the final deliverable.
2. Rebuild the PPT natively in PowerPoint / Google Slides / Keynote so text stays editable.
3. Only rasterize complex visuals when native recreation is slower than the value it adds.
4. Preserve the 22-slide structure and 44.5-minute pacing.
5. Keep the two main reusable artifacts prominent:
   - five control planes
   - MCP Delegated-Authority Matrix

If converting under time pressure, prioritize these slides for faithful recreation:
- 1, 4, 5, 11, 12, 19, 20, 21, 22

Those slides carry most of the talk’s identity and audience memory.