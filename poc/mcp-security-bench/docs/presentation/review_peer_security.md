# Peer Review Memo: MCP Security Presentation Package

Scope reviewed:
- `mcp_security_slide_manifest.md`
- `mcp_security_talk_track.md`
- `mcp_security_paper.md`
- `source_memo_microsoft_update.md`
- `source_memo_hammer_atlas.md`
- `source_memo_paper_originality.md`

Overall verdict: Accept with minor revisions

## 3 strengths

1. Strong central thesis and good security framing.
   The package is at its best when it treats MCP as a delegated-authority problem rather than a generic prompt-injection problem. That framing is coherent across the slide manifest, talk track, and paper, and it gives the audience a more mature mental model than a simple incident list.

2. Practical operator value, not just awareness-building.
   The five control planes, deployment-pattern emphasis, testing split, and Delegated-Authority Matrix are all useful artifacts for security and platform teams. This is materially better than a fear-based keynote with no reusable output.

3. Better source discipline than most security talks in this area.
   The source memos explicitly warn against overclaiming, derivative structure, and uncritical reuse of transcript examples. The talk track’s source-safe reminders are a good sign that the author is trying to stay within the evidence boundary.

## 5 concerns ranked by severity

1. Highest severity — evidence hierarchy is still too loose in the finished deliverables.
   The package sometimes presents transcript-backed or pattern-level examples with stronger wording than the source base justifies. Examples include `mcp_security_slide_manifest.md:63` (“Real MCP incidents include endpoints exposed on 0.0.0.0”), the matching wording in `mcp_security_talk_track.md:349`, and the paper’s use of incident-style phrasing in Section 5.1 (`mcp_security_paper.md:80-82`). The paper does acknowledge evidence limits at `mcp_security_paper.md:17`, and the talk track adds source-safe reminders at `mcp_security_talk_track.md:1078-1083`, but those caveats are too far away from the stronger claims. A skeptical conference audience will notice the mismatch.

2. High severity — Microsoft guidance is doing too much argumentative work.
   Slide 3 and Paper Section 3.1 lean heavily on Microsoft’s published Azure MCP guidance as the visible enterprise anchor. That is useful material, but it is vendor-authored guidance, not neutral field validation. The current framing risks sounding like “Microsoft has solved this pattern” rather than “Microsoft has published a thoughtful reference approach.” This is most visible in `mcp_security_slide_manifest.md:25-31`, `mcp_security_talk_track.md:137-168`, and `mcp_security_paper.md:42-52`.

3. Moderate severity — the package is more original in thesis than in narrative structure.
   The delegated-authority frame is good, but the middle of the talk still runs through a familiar sequence of exposed endpoints, identity confusion, indirect injection, malicious tools, and insecure reference code. That is exactly the derivative-risk pattern flagged in `source_memo_paper_originality.md:81-109`, yet the finished slides still mirror it in `mcp_security_slide_manifest.md:61-104` and the paper mirrors it in Section 5 (`mcp_security_paper.md:76-106`). The material is solid; the sequencing is less original than the package claims.

4. Moderate severity — several controls are directionally correct but under-nuanced.
   Statements like “Prefer task-oriented tools,” “trace discovery, approval, invocation, and response paths end to end,” and “control cross-tool chaining” are sensible, but the package does not spend enough time on trade-offs. Coarser tools can increase blast radius; tracing everything has privacy and cost implications; metadata/output scanning has false-positive limits; structured outputs help but do not solve semantic misuse. The result is occasionally more polished than operationally complete.

5. Lower severity but worth fixing — the matrix is promising, but it is under-demonstrated.
   The Delegated-Authority Matrix is positioned as the main original reusable artifact, yet it is illustrated with essentially one exfiltration-style story: the public-issue-to-private-repo chain (`mcp_security_slide_manifest.md:188-195`, `mcp_security_talk_track.md:954-1009`, `mcp_security_paper.md:184-192`). That makes the method look narrower than advertised. One additional worked example involving destructive write actions, approval bypass, or identity replay would make the framework feel more general and more conference-worthy.

## 3 specific line-level or section-level revision suggestions

1. Tighten evidence wording at the point of claim, not only in caveats.
   Revise `mcp_security_slide_manifest.md:61-67`, `mcp_security_talk_track.md:344-365`, and `mcp_security_paper.md:78-83` so that “real incidents” becomes something like “documented public examples,” “transcript-backed examples,” or “pattern-level failures,” depending on what is actually sourced. If there is no public postmortem-level citation, do not imply one.

2. Reframe the Microsoft section as illustrative guidance, not de facto proof.
   In `mcp_security_slide_manifest.md:25-32`, `mcp_security_talk_track.md:130-168`, and `mcp_security_paper.md:42-52`, rename or soften “MCP @ Microsoft” into a formulation such as “Published enterprise reference pattern,” and add one explicit sentence that Microsoft’s material is a useful public architecture reference, not evidence that all relevant controls are production-complete or broadly solved.

3. Restructure the middle third around trust planes instead of a serial incident parade.
   Rework `mcp_security_slide_manifest.md:61-104`, the parallel talk-track sections (`mcp_security_talk_track.md:337-545`), and `mcp_security_paper.md:76-106` into three buckets: admission/trust failures, delegated-authority/identity failures, and context/output-integrity failures. Keep one concise example under each bucket. That would better align the package with its own originality memo and make the thesis feel earned rather than bolted onto a familiar rundown.

## Source-faithfulness and risk of overclaiming

This package is more source-aware than average, and the supporting memos do a commendable job of marking where the evidence is strong versus illustrative. The strongest, most source-faithful parts are the architectural and control-design claims drawn from Microsoft’s published guidance, Hammer and Anvil’s governance-oriented control corpus, and the linked paper’s layered enterprise framing. The weak point is not fabricated content; it is rhetorical drift. A few slide and talk-track lines still sound more incident-backed, more ecosystem-general, or more deployment-validated than the underlying sources actually support. The local benchmark should remain clearly labeled as internal and illustrative, and transcript examples should remain examples, not implied prevalence data. If the final pass tightens those labels at the exact lines where the claims are made, the package will stay credible with a skeptical security audience.
