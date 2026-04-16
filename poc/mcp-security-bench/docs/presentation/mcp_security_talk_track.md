# S in MCP stands for Security

Presenter: Jitesh Thakur
Session length: 45 minutes
Format: Word-for-word keynote script
Audience: Security engineers, platform teams, agent and LLM developers, and enterprise architects

## Abstract

MCP is rapidly gaining adoption, and so are the associated security risks. In this presentation, Senior Security Engineer Jitesh Thakur explains why MCP should be treated as a delegated-authority security problem, not just a protocol convenience layer. The talk covers public failure patterns, practical safeguards, a rollout baseline teams can implement immediately, and a repeatable threat-modeling method tailored to MCP.

## Delivery guidance

This file is now written as a spoken script, not a planning memo. It should be deliverable nearly word for word on stage. Small improvisations are fine, but the default assumption is that Jitesh can read this straight through and sound natural.

Keep the tone calm, direct, and credible.
Do not sound anti-MCP.
Do not sound alarmist.
Sound like a security engineer helping teams adopt MCP responsibly.

---

## Slide 1 — S in MCP stands for Security

Good afternoon, everyone.

I want to begin with the simplest sentence in this entire talk, because it is the sentence I most want you to remember when you leave this room.

The S in MCP stands for Security.

Not because security should slow adoption down.
Not because MCP is uniquely broken.
And not because this is one more talk telling you that everything is on fire.

The reason is much simpler than that.

MCP is crossing the line from interesting protocol to real operating fabric.
It is connecting models to tools.
It is connecting tools to systems.
And it is connecting systems to real data, real credentials, and real actions.

The moment that starts happening, security stops being optional polish.
It becomes part of the product.

So this is not a panic talk.
It is an operator’s talk.

I want to show you how to think about MCP the way a security engineer or platform team should think about it: not just as context exchange, but as delegated authority moving through a system.

If your model can discover something, select something, or invoke something, it is part of your security boundary.

So let’s start with why this matters now, and why it is becoming urgent faster than many teams expected.

---

## Slide 2 — Why this matters now

MCP is being pulled into copilots, internal assistants, platform tooling, and enterprise gateways because it solves a real problem. It gives teams a standardized way to connect models to useful capabilities.

That is the good news.

The security problem is that the reachable action surface is growing faster than the review discipline around it.

More tools means more callable actions.
More callable actions means more hidden trust assumptions.
And more hidden trust assumptions means more ways for a small mistake to turn into a large incident chain.

That is why security cannot be phase two.
It has to move at rollout speed.

One of the most useful public examples of that mindset is how Microsoft frames MCP deployment.

---

## Slide 3 — MCP @ Microsoft: a published reference pattern

When people ask what a more mature enterprise MCP pattern looks like, one of the better public reference points right now is Microsoft’s published guidance.

And I want to be careful with that phrase.
This is useful public reference guidance.
It is not proof that the ecosystem is solved.

What matters in that guidance is the architecture mindset.
Identity.
Gateway policy.
Private execution.
Data access controls.
Telemetry.
Defense in depth.

The right question is not, “Do we have MCP?”

The right question is, “What is the control plane around MCP?”

Where are authentication and authorization enforced?
Where are approval decisions made?
Where is exposure reduced?
Where is telemetry collected?
Where is trust revoked when something goes wrong?

If every team stands up MCP servers ad hoc, you do not get a platform. You get a distributed security experiment.

So if the protocol is not the security model, what is the right model?
My answer is delegated authority.

---

## Slide 4 — MCP is delegated authority

This is the central idea I want to give you today.

MCP is best understood as delegated authority moving across components.

Authority starts somewhere.
A user.
A service identity.
A broker.
Then it moves through a host, a client, a server, a tool, and eventually into a backend system that can read data or perform an action.

That movement is the real security story.

Because when we say, “The model used a tool,” what we usually mean is that some chain of trust allowed a system to do something meaningful on our behalf.

Read a ticket.
Open a repo.
Query a database.
Write a record.
Send a message.
Trigger a workflow.

So the wrong mental model is, “This is just prompt safety.”

The better mental model is, “Where does authority move, and what constrains it at each step?”

Once you start asking that question, the rest of the security model becomes much clearer.

Let me make that concrete with a simple execution loop.

---

## Slide 5 — The MCP execution loop

When I threat-model MCP systems, I find it useful to break the workflow into six stages.

Discover.
Select.
Approve.
Invoke.
Return.
Retain.

Discover is what the model can see.
Select is what the model chooses.
Approve is where policy or a user decides if the action should proceed.
Invoke is runtime execution.
Return is what comes back.
Retain is what persists into later context, memory, or state.

Why does this matter?
Because security is not one checkpoint at runtime.
You can lose before execution, during execution, or after execution when output is reused unsafely.

That is why MCP security needs to span design, policy, runtime, and output handling.

And if you want proof that design matters, not just runtime, start with how the tools themselves are shaped.

---

## Slide 6 — Build security into the tool contract

One of the strongest ideas in Microsoft’s development guidance is this:

Design for agent success, not API exhaustiveness.

That sounds like a usability point.
It is also a security point.

A lot of teams make the same mistake.
They treat MCP as a way to expose every backend operation as a separate tool.
One endpoint, one tool.
Another endpoint, another tool.

Very quickly, the model is looking at a wall of low-level actions.
That increases ambiguity.
It increases reasoning burden.
And it increases the odds that the wrong tool gets selected or the right tool gets used the wrong way.

A better pattern is task-oriented tools.
Bounded business actions.
Clear names.
Well-structured input schemas.
Structured outputs.
Recoverable but non-revealing errors.

So before you ever get to incident response, ask a design question:
Did we build tools that are easy to reason about, well bounded, and safe to consume?

If the answer is no, then risk already exists before runtime.

Now let’s look at the three failure buckets that matter most.

---

## Slide 7 — Bucket 1: exposure and sample-code failures

The first bucket is the classic one.
Exposure mistakes and unsafe defaults.

We already have public examples and transcript-backed examples of MCP surfaces being exposed more broadly than intended, including open bindings and local-first tooling becoming reachable farther than people expected.

And then there is the sample-code problem.
Reference servers and demo integrations often teach protocol mechanics, not production hardening.

That means two dangerous phrases keep showing up.

“It is internal only.”
And, “It is just reference code.”

Neither of those is a control.

Bind address, transport security, authentication, network isolation, and real secure-code review still matter.
MCP did not remove those basics.
It just made them easier to forget under delivery pressure.

The second bucket is where MCP starts to feel more distinct: identity mistakes become much more portable.

---

## Slide 8 — Bucket 2: delegated-authority failures

Identity failures become especially dangerous in MCP because authority moves so easily.

A leaked token is not just a secret exposure problem.
It is a portable action right.
It means the system may now be able to do something meaningful automatically.

This is why over-scoped OAuth grants, shared bearer tokens, and raw pass-through credential patterns are so risky.

One especially useful framing here is the confused deputy problem.
That is the case where the MCP server or connector ends up acting with broader authority than the requester should actually have.

A better pattern is to broker access.
Use short-lived, scoped, tool-specific credentials.
Validate audience, issuer, and expiry.
Separate read, write, and admin capabilities.
And require stronger approval for destructive actions.

The principle is simple: authority should shrink as it moves, not stay maximally portable across the chain.

Once authority is available, the next question is who gets to influence what the system does with it.

---

## Slide 9 — Bucket 3: context and trust failures

The third bucket combines two failure classes that often get discussed separately, but really belong together.

First, untrusted context can steer privileged actions.
Indirect injection can arrive through docs, issues, web pages, tickets, or tool output.

Second, attackers can win before runtime by being discovered or selected into trust.
That is where shadowing, poisoned metadata, and rug pulls matter.

A transcript-backed example makes the first part concrete: public issue content can steer an agent toward private repository access if scope and output handling are weak.

The second part is where Hammer and Anvil is especially useful.
It treats tool trust as a lifecycle problem.
Registry.
Ownership.
Versioning.
Review.
Recertification.

So the lesson from this bucket is simple.
Treat context as untrusted.
And treat trust itself as something attackers can manipulate.

At this point, the natural question is: if simple attacks are known, why do simple defenses still miss them?

---

## Slide 10 — Why simple defenses still miss attacks

This is where the internal benchmark material is useful, as long as we keep it in bounds.

In our internal examples, some obvious malicious metadata is catchable.
Some suspicious responses are catchable.
But semantically plausible abuse still gets through.

That is exactly why I would not ask one scanner, one classifier, or one policy check to do the work of a system.

Scanning helps.
But layered controls matter more.

That is the bridge to the first real artifact I want you to take away from this session.

---

## Slide 11 — The photo slide: five control planes

If you remember only one framework before the close, remember this one.

Five control planes.

Architecture.
Tool trust.
Delegated authority.
Context integrity.
Containment and telemetry.

This is the slide I want people to take a picture of.
Because it compresses a messy security conversation into an operating model.

Architecture asks where MCP is exposed and governed.
Tool trust asks what becomes discoverable and why.
Delegated authority asks how credentials and approvals are brokered.
Context integrity asks how inputs, outputs, schemas, and errors are validated.
Containment and telemetry asks how misuse is constrained and how fast you will know.

That is much more usable than trying to memorize ten disconnected risks.

Now let’s make it more practical and answer the next question platform teams always ask: who owns what?

---

## Slide 12 — Who owns what: a rollout operating model

One of the easiest ways for a security program to fail is to have everyone agree that a control matters and nobody clearly owns it.

So here is a simple operating model.

Platform owns deployment pattern, gateway defaults, registry mechanics, and safe exposure by default.

IAM owns brokered credentials, scopes, audience rules, and sender constraints.

Security engineering, or AppSec, owns onboarding review, validation standards, and red-team patterns.

SOC or operations owns tracing, detection, and response playbooks.

Builders and product owners still own tool purpose, workflow fit, and approval decisions for high-risk actions.

That ownership model is not universal. But some version of it has to exist if the control planes are going to survive contact with reality.

With ownership on the table, let’s walk the control planes one by one.

---

## Slide 13 — Control plane 1: secure deployment patterns

The linked enterprise-grade paper lays out several secure deployment patterns.
Gateway-centric patterns.
Dedicated security zones.
Tightly governed service deployment.

The exact shape can vary.
But the principles should not.

Identity should be part of the default path.
Private networking should be part of the default path.
Policy should be part of the default path.
Telemetry should be part of the default path.

Secure architecture comes before secure prompting.
That is the sequence I want teams to remember.

The second control plane is the one many teams skip: tool admission.

---

## Slide 14 — Control plane 2: tool admission and provenance

Before a tool becomes discoverable, someone should be able to answer a few basic questions.

Who owns it?
Why does it exist?
What permissions does it need?
What environment can it reach?
What changed in the last release?
Why should the model be allowed to see it at all?

If you cannot answer those questions, the tool is not ready for discovery.

This is where Hammer and Anvil contributes something really useful.
It treats MCP controls as governed artifacts.
A registry.
A review state.
Version pinning.
Provenance checks.
Approval workflows.
Periodic recertification.

In other words, treat tools more like production dependencies and less like convenient plugins.

Once tools are admitted, the next question is how authority is carried into them.

---

## Slide 15 — Control plane 3: brokered identity and approval

The safest pattern is not broad pass-through authority.
It is explicit, brokered, short-lived, scoped authority.

That means tool-specific credentials.
Limited lifetimes.
Clear separation between read, write, and admin capabilities.
Audience restriction.
Sender constraints where available.
And stronger approval or step-up authentication for high-risk actions.

This is also where teams need to decide what should never be silent.
There are actions that should not happen purely because the model found a capable tool.
Delete.
Transfer.
Publish.
Rotate.
Approve.
Those often deserve explicit policy or human gating.

But even a well-brokered identity system can still be steered badly if validation is weak.

---

## Slide 16 — Control plane 4: validate inputs, outputs, and errors

This control plane is about validation.
And I mean validation in a broad sense.

Input schemas.
Unexpected fields.
Metadata.
Tool output.
Recovered errors.
Retrieved content.
Everything that shapes the next decision in the chain.

Microsoft’s guidance is clear on structured inputs and structured outputs.
The linked paper goes further and treats input and output validation as its own control family.

That is the right instinct.

If the model has to parse vague prose, you create ambiguity.
If unknown fields are accepted silently, you create room for drift and abuse.
If error messages leak internals, you create information disclosure.
If tool output is reused raw, you create a control channel.

Now we come to the part that decides whether a bad decision becomes a catastrophe.
Containment.

---

## Slide 17 — Control plane 5: containment and observability

If a tool is abused, or a model makes the wrong call, or a trusted component turns out to be untrustworthy, what happens next?

That is what containment answers.

Sandbox the runtime.
Restrict filesystem access.
Restrict process execution.
Restrict network access.
Use egress allowlists.
Control cross-tool chaining where you can.
Assume prevention will be imperfect and design for survivable failure.

And pair that with observability.
Log discovery.
Log approvals.
Log invocation.
Log responses.
Log policy decisions.
Log the chain, not just the final step.

Containment reduces blast radius.
Telemetry reduces dwell time.
You need both.

Now that we have the five control planes, the next question is how to keep them honest over time.
Testing.

---

## Slide 18 — Continuous validation: logic, protocol, and agent behavior

This is another area where Microsoft’s public guidance is unusually practical.

You validate MCP systems at three layers.

First, unit tests for tool logic and local policy behavior.

Second, protocol tests for MCP compliance and error handling.

Third, agent tests for discoverability, selection, argument construction, and recovery behavior.

That split matters because a secure tool that is consistently mis-selected is still a security problem.

Operationally, logic and protocol tests fit naturally into every-commit workflows.
Agent-behavior tests are usually better for pull requests or nightly runs because they are slower, but closer to deployment reality.

At this point, teams usually ask: what is the minimum I should insist on before something is discoverable in production?

---

## Slide 19 — Day-1 baseline and 90-day roadmap

Before an MCP-enabled workflow becomes discoverable in production, I would insist on a day-one baseline.

A registry entry.
A named owner.
A scoped credential policy.
High-risk approval.
Mandatory telemetry.
And a containment baseline appropriate to the workflow.

That is the minimum production standard.

Then, in the next thirty to ninety days, standardize gateway patterns, onboarding workflows, metadata and output scanning, and incident playbooks.

Longer term, move toward stronger registries, signed artifacts, policy-aware clients, continuous recertification, and safer defaults across the ecosystem.

So the sequence is simple.
Minimum standard first.
Standardization next.
Safer defaults over time.

Now let me show you the second reusable artifact from this talk: the matrix.

---

## Slide 20 — The MCP Delegated-Authority Matrix: simplified starter shape

I want to make one important simplification here.

Most threat-modeling artifacts fail for a boring reason.
They ask one slide to do too much.

So here is the rule I recommend.
Start with a core matrix, and keep the fuller worksheet for the team actually doing rollout.

The matrix I want on screen needs only five fields.

Risk.
Stage.
First control.
Owner.
Priority.

That is enough to force a useful conversation.

What kind of failure is this?
Where in the lifecycle does it show up?
What is the first control that should stop it?
Who owns that control?
And how urgently does it need attention?

You can absolutely keep more detail in the team worksheet.
Asset at risk.
Detection signal.
Impact.
Likelihood.
Recovery action.
All of that is useful.

But if you try to start with the full worksheet, most teams will never use it.

So instead of showing only two bespoke rows, let me show you a broader starter set seeded from the OWASP MCP Top 10.

---

## Slide 21 — Starter matrix examples from the OWASP MCP Top 10

The fuller starter matrix can absolutely contain six or more rows.
But on stage, you still want prioritization, not a spreadsheet.

So here is the easier way to show it.

Take the OWASP-seeded rows and split them into two buckets.

Fix now:
MCP01 secret exposure.
MCP02 scope creep.
MCP05 command execution.

Harden next:
MCP03 tool poisoning.
MCP09 shadow servers.
MCP10 context over-sharing.

That is already much easier to read.
And it tells the audience something more useful than a long undifferentiated table.

It tells them what to fix first.

If you want the fuller worksheet, that belongs in the paper, in the appendix, or in the team worksheet.
But the matrix on screen should make prioritization visible.

So let me close with the simplest possible next step.

---

## Slide 22 — Final checklist and call to action

If you take only one practical next step after this session, make it this.

Pick one MCP-enabled workflow this week.
Map where authority moves.
Find one risky path.
And fix it before you add more capability.

That is the operating discipline I would encourage.
Not stop.
Not panic.
Not wait for a perfect framework.

Start with one workflow.
Make authority visible.
Reduce one risky path.
Then scale from there.

Because the real lesson is simple.

If your model can reach it, your security model must explain it.

---

## Appendix A — Enterprise reference framework (Figure 2)

If someone wants the denser enterprise version of the story, this is it.

Figure 2 from the enterprise MCP security paper lays out the fuller layered framework: client, server, runtime controls, external services, and the threat groupings around them.

It is useful.
But it is also exactly why I simplified the main talk into the five control planes.

On stage, you want an artifact people can remember.
In architecture review, you often want the fuller map.
This appendix gives you that fuller map.

And if you want the paper’s category-level threat and control summary, that is the next appendix slide.

---

## Appendix B — Enterprise threat/control summary (Table I)

Table I from the paper is useful because it maps broad threat categories to broad control families.

Tool poisoning.
Data exfiltration.
Command and control.
Identity and access control subversion.
Denial of service.
Insecure configuration.

That is a useful enterprise reference view.

But notice what it does not do.
It does not give you one operator row per abuse story, with a lifecycle stage, a concrete owner, a quick test, and an implementation priority.

So this appendix table complements the main talk.
It does not replace the matrix.

If I were using both internally, I would use Table I for category-level control mapping, and the delegated-authority matrix for actual rollout prioritization.
