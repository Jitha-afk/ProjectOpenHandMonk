# Presenter Notes — Day Of Presentation

Purpose: tightened speaking notes for stage use.
These are intentionally shorter than the full talk track.
Use them as cue cards, not as a script.

## Slide 1 — S in MCP stands for Security
- Land the line early.
- This is not anti-MCP; it is pro-adoption with controls.
- Key idea: once tools reach real systems, security becomes part of the product.
Transition: why now.

## Slide 2 — Why this matters now
- Adoption is accelerating because MCP solves a real integration problem.
- Risk is scaling faster than review discipline.
- Security has to move at rollout speed.
Transition: public enterprise reference pattern.

## Slide 3 — MCP @ Microsoft: a published reference pattern
- Phrase carefully: useful public guidance, not proof the ecosystem is solved.
- Emphasize control plane, not protocol alone.
- Identity, policy, private execution, telemetry.
Transition: what is the right mental model?

## Slide 4 — MCP is delegated authority
- This is the signature concept.
- Ask: where does authority move, and what constrains it?
- Not just prompt safety; system authority.
Transition: execution loop.

## Slide 5 — The MCP execution loop
- Six stages: discover, select, approve, invoke, return, retain.
- Point: security is not just one runtime checkpoint.
- You can lose before, during, or after execution.
Transition: design-time security.

## Slide 6 — Build security into the tool contract
- Poor tool shape creates avoidable risk.
- Prefer task-oriented tools and structured outputs.
- Safe errors matter.
Transition: failure buckets.

## Slide 7 — Exposure and sample-code failures
- Classic mistakes still matter.
- Internal-only and reference-code are not controls.
- MCP compresses prototype-to-production mistakes.
Transition: identity failures.

## Slide 8 — Delegated-authority failures
- A token is a portable action right.
- Confused deputy and pass-through authority are the big ideas.
- Brokered, short-lived, scoped credentials are safer.
Transition: context and trust.

## Slide 9 — Context and trust failures
- Untrusted context can steer privileged actions.
- Trust itself can be manipulated via shadowing, poisoning, rug pulls.
- Treat context as untrusted and trust as attackable.
Transition: why simple defenses miss attacks.

## Slide 10 — Why simple defenses still miss attacks
- Keep benchmark caveated as internal and illustrative.
- Some obvious attacks are catchable; plausible abuse survives.
- Layered controls beat one detector.
Transition: operating checklist.

## Slide 11 — Five control planes
- This is the photo slide.
- Say the five planes clearly and slowly.
- Keep detailed explanation verbal, not visual.
Transition: ownership.

## Slide 12 — Who owns what
- Controls die when ownership is vague.
- Platform, IAM, Security, SOC/Ops, Builders/Product.
- The exact org chart can vary; explicit ownership cannot.
Transition: walk the planes.

## Slide 13 — Secure deployment patterns
- Architecture is a security control.
- Identity, networking, policy, telemetry must be default-path decisions.
- Secure architecture comes before secure prompting.
Transition: tool admission.

## Slide 14 — Tool admission and provenance
- Treat tools like production dependencies.
- Registry, provenance, change review, recertification.
- Trust should decay without review.
Transition: identity and approval.

## Slide 15 — Brokered identity and approval
- Authority should shrink as it moves.
- Separate read/write/admin.
- Some actions should never be silent.
Transition: validation.

## Slide 16 — Validate inputs, outputs, and errors
- Context integrity must be engineered.
- Structured outputs beat ambiguous prose.
- Treat retrieved content and tool output as untrusted until validated.
Transition: containment.

## Slide 17 — Containment and observability
- Containment reduces consequence.
- Telemetry reduces dwell time.
- Log the chain, not just the final step.
Transition: testing.

## Slide 18 — Continuous validation
- Three layers: logic, protocol, agent behavior.
- A secure tool that is consistently mis-selected is still a problem.
- This gives teams a concrete rollout habit.
Transition: minimum baseline.

## Slide 19 — Day-1 baseline and 90-day roadmap
- Emphasize Day 1 most strongly.
- Minimum production standard before discoverability.
- Then standardize; then improve ecosystem defaults.
Transition: matrix artifact.

## Slide 20 — Matrix anatomy
- Explain how to read one row.
- The artifact must survive contact with a real meeting room.
- It is about prioritized action, not threat-model theater.
Transition: two examples.

## Slide 21 — Read path and write path
- Example A: read-path exfiltration.
- Example B: destructive write path.
- Same matrix shape, different control and ownership story.
Transition: final call to action.

## Slide 22 — Closing
- Ask for one workflow, one trust path, one fix.
- Do not end on fear; end on disciplined optimism.
- Final line: If your model can reach it, your security model must explain it.

## Delivery reminders
- Slow down on Slides 4, 11, 19, 20, 22.
- Do not over-explain Microsoft guidance; keep it bounded.
- Do not oversell benchmark results.
- Treat transcript-backed examples as examples, not prevalence claims.
- If time gets tight, shorten Slides 7–10 first, not the artifact slides.
