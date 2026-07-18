# Second-draft citation tightening plan

Priority rule: work packets marked HIGH are the first close-read pass; for those sections, either promote the cited claims to close-read support or downgrade the manuscript wording.

| Packet | Risk if left as-is | Target sections | Claims most in need of close-read support | Likely source keys to revisit first |
|---|---|---|---|---|
| 1. Core framing and thesis guardrails | Medium | Abstract; §1 Introduction; §10 Conclusion | C-01 attack-surface expansion; C-05 latest-spec novelty/gap framing; C-18 governance-gap framing; broad "enterprises lack operational guidance" language | S1, S3, S7, S10, SPEC-2025 |
| 2. Latest-spec deployment surface | HIGH | §2 Background and latest-spec deployment surface | C-05 spec-feature coverage and literature-gap claim; C-08 per-user scoped auth framing; C-09 roots as confinement; C-10 elicitation mode restrictions; any claim that Streamable HTTP, roots, elicitation, or sampling-with-tools are underanalyzed | SPEC-2025, S2, S3, S7, S10 |
| 3. Threat model foundations | HIGH | §3 Threat model framing and paper contributions | C-01 multi-surface threat expansion; C-02 malicious tool-description risk; C-03 cross-server trust propagation; C-11 prompt-injection amplification; C-14 audit-surface breadth | S1, S2, S6, S9, S10, S11 |
| 4. Metadata poisoning and delegated authority scenarios | Medium-High | §4.1-§4.2 | C-02 malicious metadata/tool-description coercion; C-08 delegated-authority and scoped-auth claims; any wording that implies recurring real-world exploitation rather than plausible attack paths | S1, S4, S7, S9, S12, SPEC-2025 |
| 5. Local boundaries, elicitation, and cross-server escalation | HIGH | §4.3-§4.5 | C-03 cross-server escalation; C-05 Streamable HTTP and sampling security significance; C-09 roots enforcement; C-10 elicitation abuse; C-13 low-barrier exfiltration example | SPEC-2025, S2, S7, S10, S11 |
| 6. Control framework and proposed defense patterns | HIGH | §5; §6.1-§6.6 | C-04 scanner feasibility/limits; C-06 gateway efficacy; C-07 provenance envelopes; C-12 ATTEST-style quantitative claims; C-14 audit schema; C-15 formal-core realism; C-16 registry/attestation governance; C-17 response normalization | S3, S5, S6, S7, S10, S12, S2 |
| 7. Evaluation, rollout, and evidence-boundary language | Medium-High | §7; §8; §9 | Provisional thresholds and evaluation language attached to C-06, C-07, C-09, C-10, C-15, and C-17; operational guidance tied to C-08, C-14, and C-18; any sentence that could read as measured efficacy instead of planned validation | S6, S7, S3, S10, SPEC-2025 |

## Tightening order
1. Packet 2
2. Packet 6
3. Packet 5
4. Packet 3
5. Packet 4
6. Packet 7
7. Packet 1

## Second-draft standard
- Replace title/abstract-dependent support with close-read citations wherever the packet is marked HIGH.
- If close reading does not hold, narrow the claim to spec-grounded, analogical, or hypothesis language instead of keeping broad empirical wording.
- Prefer multi-source support for attack prevalence, cross-server escalation, and scanner efficacy; avoid single-source quantitative claims unless the relevant methods/results sections are read closely.