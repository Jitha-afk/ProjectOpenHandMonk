# Slide Manifest: S in MCP stands for Security

Presenter: Jitesh Thakur
Session format: 45-minute keynote / TEDx-style practical talk
Audience: Security engineers, platform teams, agent/LLM developers, and enterprise architects
Target runtime: ~45 minutes main talk + optional appendix

## Slide 1 — S in MCP stands for Security
Objective: Open with the session thesis and establish the tone.
- MCP is becoming operating fabric, not just an interesting protocol
- Tool access turns model capability into production capability
- Security is what makes adoption survivable, not what blocks it
Speaker notes: Keep this calm and direct. The opening line should land hard, then immediately shift into practical operator energy.
Estimated time: 2 minutes

## Slide 2 — Why this matters now
Objective: Show why the urgency is operational, not hypothetical.
- MCP is spreading through copilots, platform tooling, and enterprise gateways
- Reachable action surface is growing faster than review discipline
- Small mistakes now compose into high-consequence chains
Speaker notes: This slide should be shorter and lighter than before. Let the audience feel speed, not bureaucracy.
Estimated time: 1.5 minutes

## Slide 3 — MCP @ Microsoft: a published reference pattern
Objective: Ground the talk in a public enterprise reference approach without overclaiming it.
- Microsoft publishes a defense-in-depth reference model for MCP on Azure
- Identity, gateway policy, private execution, data controls, and telemetry all matter
- Treat it as useful public guidance, not proof that the ecosystem is “solved”
Speaker notes: The key phrase is “published reference pattern.” Keep it useful and bounded.
Estimated time: 2 minutes

## Slide 4 — MCP is delegated authority
Objective: Introduce the talk’s original framing.
- Authority moves across host, client, server, tool, and backend systems
- The security question is not only what the model says; it is what the system can do
- Every credential, tool, and approval path becomes part of the trust boundary
Speaker notes: This is the conceptual anchor for the entire talk. Everything later should feel like a consequence of this framing.
Estimated time: 2.5 minutes

## Slide 5 — The MCP execution loop
Objective: Give the audience a compact model of where attacks and controls appear.
- Discover
- Select
- Approve
- Invoke / Return / Retain
Speaker notes: Keep this visual and simple. The audience should remember the loop, not a paragraph of explanation.
Estimated time: 2 minutes

## Slide 6 — Build security into the tool contract
Objective: Show that design-time choices are part of security.
- Design for agent success, not API exhaustiveness
- Prefer task-oriented tools over endpoint sprawl
- Use clear schemas, structured outputs, and safe error handling
Speaker notes: This is the talk’s first originality move: start with insecure tool shape, not just runtime incidents.
Estimated time: 2 minutes

## Slide 7 — Bucket 1: exposure and sample-code failures
Objective: Group the “classic but newly amplified” failures together.
- Documented public examples include exposed MCP surfaces and unsafe bind defaults
- Sample and reference servers can carry insecure assumptions into real environments
- “Internal only” and “reference code” are not controls
Speaker notes: Combine open endpoints and sample-derived server risk into one bucket so the talk is less incident-parade-like.
Estimated time: 2 minutes

## Slide 8 — Bucket 2: delegated-authority failures
Objective: Explain why identity mistakes become especially dangerous in MCP.
- Token leaks are portable action rights
- Pass-through authority and confused-deputy patterns create silent escalation
- Brokered, scoped, short-lived credentials are the safer default
Speaker notes: This is where to use the transcript-backed confused-deputy example, but briefly.
Estimated time: 2 minutes

## Slide 9 — Bucket 3: context and trust failures
Objective: Combine indirect injection and tool-trust abuse into one stronger category.
- Untrusted context can steer privileged tool use
- Shadowing, poisoned metadata, and rug pulls are trust-admission failures
- Output reuse is part of the control surface, not a harmless convenience
Speaker notes: This bucket should feel more original than the old one-slide-per-incident sequence.
Estimated time: 2 minutes

## Slide 10 — Why simple defenses still miss attacks
Objective: Use local benchmark material to justify layered controls without overselling it.
- Internal examples show some obvious malicious metadata is catchable
- Subtle or semantically plausible abuse still gets through
- Scanning helps, but layered controls matter more than one classifier
Speaker notes: Keep the benchmark clearly labeled as internal and illustrative.
Estimated time: 1.5 minutes

## Slide 11 — The photo slide: five control planes
Objective: Give the audience the first clearly reusable artifact.
- Architecture
- Tool trust
- Delegated authority
- Context integrity
- Containment + telemetry
Speaker notes: This should be the “take a picture of this” slide. Minimal on-screen text, maximum clarity.
Estimated time: 2 minutes

## Slide 12 — Who owns what: a rollout operating model
Objective: Add practical ownership clarity for platform teams.
- Platform: deployment pattern, gateway, registry, defaults
- IAM: brokered credentials, scopes, sender/audience rules
- AppSec / Security Eng: validation standards, onboarding review, red-team patterns
- SOC / Operations: tracing, anomaly detection, response playbooks
- Product / Builders: high-risk approval paths, tool purpose, business fit
Speaker notes: This addresses the peer-review concern that ownership was implied more than operationalized.
Estimated time: 2 minutes

## Slide 13 — Control plane 1: secure deployment patterns
Objective: Turn architecture into an actionable decision.
- Gateway-centric, dedicated security zone, or tightly governed services
- Make identity, policy, networking, and telemetry part of the default path
- Secure architecture comes before secure prompting
Speaker notes: Use the enterprise-grade paper and Microsoft reference model here.
Estimated time: 2 minutes

## Slide 14 — Control plane 2: tool admission and provenance
Objective: Treat tool onboarding like supply-chain governance.
- Registry every tool with owner, purpose, permissions, and review state
- Require provenance, version pinning, and change approval
- Re-certify tools over time; trust should decay without review
Speaker notes: Emphasize lifecycle, not one-time approval.
Estimated time: 2 minutes

## Slide 15 — Control plane 3: brokered identity and approval
Objective: Show how to reduce confused-deputy and over-scope failures.
- Use tool-specific, short-lived, scoped credentials
- Separate read, write, and admin authority
- Make destructive or high-consequence paths explicitly non-silent
Speaker notes: This is the most directly actionable control plane for many teams.
Estimated time: 2 minutes

## Slide 16 — Control plane 4: validate inputs, outputs, and errors
Objective: Make context integrity an engineering discipline.
- Validate schemas and reject drift where possible
- Prefer structured outputs over prose the model must interpret
- Treat metadata, retrieved content, tool output, and errors as untrusted until validated
Speaker notes: Connect build-time design and runtime hygiene.
Estimated time: 2 minutes

## Slide 17 — Control plane 5: containment and observability
Objective: Reduce blast radius and improve time to detection.
- Sandbox runtime and restrict filesystem, process, and network access
- Use egress allowlists and cross-tool-chain controls
- Trace discovery, approval, invocation, and response end to end
Speaker notes: Pair containment and telemetry on purpose: one reduces consequence, the other reduces dwell time.
Estimated time: 2 minutes

## Slide 18 — Continuous validation: logic, protocol, and agent behavior
Objective: Give the audience a concrete testing model.
- Unit tests verify tool logic and policy behavior
- Protocol tests verify MCP compliance and error handling
- Agent tests verify discoverability, selection, argument construction, and recovery
Speaker notes: This should feel practical and rollout-ready, not theoretical.
Estimated time: 2 minutes

## Slide 19 — Day-1 baseline and 90-day roadmap
Objective: Make the talk immediately actionable.
- Day 1 baseline: registry entry, named owner, scoped credential policy, high-risk approval, mandatory telemetry
- 30–90 days: standardized gateways, onboarding workflows, metadata/output scanning, incident playbooks
- Long-term: signed artifacts, policy-aware clients, continuous recertification, safer defaults
Speaker notes: This addresses the peer-review request for a minimum viable platform standard.
Estimated time: 2.5 minutes

## Slide 20 — The MCP Delegated-Authority Matrix: simplified starter shape
Objective: Simplify the threat-model matrix so teams will actually use it.
- Start with 5 fields only: risk, stage, first control, owner, priority
- Keep asset, signal, impact, and likelihood in the team worksheet, not the keynote slide
- One row should represent one realistic abuse story
- Use OWASP MCP Top 10 categories as seed rows, not as the whole threat model
Speaker notes: The audience should feel relief here. The message is that the matrix becomes usable when you stop trying to solve every question in one slide.
Estimated time: 2.5 minutes

## Slide 21 — Starter matrix examples from the OWASP MCP Top 10
Objective: Show a broader, more practical set of example rows without turning the slide into an appendix table.
- Seed rows drawn from MCP01, MCP02, MCP03, MCP05, MCP09, and MCP10
- Group them into two visible priorities: fix-now rows and harden-next rows
- Keep each row to one first control, one owner, and one priority
Speaker notes: This is now the operator’s starter matrix: broad enough to begin prioritization this week, simple enough to read on stage. The handout or paper can carry the fuller list.
Estimated time: 2.5 minutes

## Slide 22 — Final checklist and call to action
Objective: End with a memorable and concrete close.
- Pick one MCP-enabled workflow this week
- Map where authority moves
- Find one risky path
- Fix it before adding more capability
Speaker notes: End on disciplined optimism. The last line should still be: if your model can reach it, your security model must explain it.
Estimated time: 1.5 minutes

## Appendix A — Enterprise reference framework (Figure 2)
Objective: Show the paper’s full enterprise security framework as backup/reference material.
- Multi-layered MCP security framework from the enterprise MCP paper
- Useful as architectural grounding, not as the main keynote takeaway artifact
- Use only in Q&A, backup, or follow-up discussion
Speaker notes: If shown, explain that the main talk deliberately simplified this into the five-control-plane takeaway. This appendix proves the enterprise grounding.
Estimated time: optional appendix

## Appendix B — Enterprise threat/control summary (Table I)
Objective: Show the paper’s category-level threat/control table as supporting reference material.
- Threat categories mapped to mitigation controls from the enterprise MCP paper
- Useful as a companion reference, not a replacement for the delegated-authority matrix
- Use to answer “how does your matrix relate to enterprise control mapping?”
Speaker notes: If shown, contrast this table with the main talk’s matrix: this appendix is category-to-controls; the talk matrix is row-level operator prioritization.
Estimated time: optional appendix
