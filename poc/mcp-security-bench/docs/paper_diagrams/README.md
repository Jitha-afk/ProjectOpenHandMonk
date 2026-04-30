# Paper diagram assets

These figures support `../AGT_MCP_SCAN_CLI_REPAIR_RESEARCH_PAPER.md`.

Generated variants:

| Figure | Mermaid source | Rendered SVG | PNG QA fallback |
|---|---|---|---|
| AGT mcp-scan repair lifecycle | `agt_mcp_scan_repair_lifecycle.mmd` | `agt_mcp_scan_repair_lifecycle.mermaid.svg` | `agt_mcp_scan_repair_lifecycle.mermaid.png` |
| Metadata inspection boundary | `metadata_inspection_boundary.mmd` | `metadata_inspection_boundary.mermaid.svg` | `metadata_inspection_boundary.mermaid.png` |
| Evidence-to-claim boundary map | `evidence_claim_boundary_map.mmd` | `evidence_claim_boundary_map.mermaid.svg` | `evidence_claim_boundary_map.mermaid.png` |

Rendering command used:

```bash
npx -y @mermaid-js/mermaid-cli \
  -p pptr-mermaid.json \
  -i figure.mmd \
  -o figure.mermaid.svg \
  -t neutral -b transparent

npx -y @mermaid-js/mermaid-cli \
  -p pptr-mermaid.json \
  -i figure.mmd \
  -o figure.mermaid.png \
  -t neutral -b white
```

Notes:
- The markdown paper embeds the SVG files for crisp rendering in GitHub and print-like review.
- PNG files are included as QA fallbacks for quick visual inspection.
- Figures are conceptual summaries; paper claims remain governed by the evidence boundaries in the text.
