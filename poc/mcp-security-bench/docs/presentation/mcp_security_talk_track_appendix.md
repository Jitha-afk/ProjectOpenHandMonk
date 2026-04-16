## Slide 15 — Control plane 3: brokered identity and approval

### Core message
Authority should shrink as it moves.

### Talk track

The safest pattern is not broad pass-through authority.
It is explicit,
brokered,
short-lived,
scoped authority.

That means tool-specific credentials.
Limited lifetimes.
Clear separation between read,
write,
and admin capabilities.
Audience restriction.
Sender constraints where available.
And stronger approval or step-up auth for high-risk actions.

This is also where teams need to decide what should never be silent.
There are actions that should not happen purely because the model found a capable tool.
Delete.
Transfer.
Publish.
Rotate.
Approve.
Those often deserve explicit policy or human gating.

### Transition
But even a well-brokered identity system can still be steered badly if validation is weak.

---

## Slide 16 — Control plane 4: validate inputs, outputs, and errors

### Core message
Context integrity has to be engineered.

### Talk track

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

If the model has to parse vague prose,
you create ambiguity.
If unknown fields are accepted silently,
you create room for drift and abuse.
If error messages leak internals,
you create information disclosure.
If tool output is reused raw,
you create a control channel.

### Transition
Now we come to the part that decides whether a bad decision becomes a catastrophe.
Containment.

---

## Slide 17 — Control plane 5: containment and observability

### Core message
Containment reduces blast radius; telemetry reduces dwell time.

### Talk track

If a tool is abused,
or a model makes the wrong call,
or a trusted component turns out to be untrustworthy,
what happens next?

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

### Transition
Now that we have the five control planes, the next question is: how do you keep them honest over time?
Testing.

---

## Slide 18 — Continuous validation: logic, protocol, and agent behavior

### Core message
MCP needs a three-layer testing model.

### Talk track

This is another area where Microsoft’s public guidance is unusually practical.

You validate MCP systems at three layers.

First,
unit tests for tool logic and local policy behavior.

Second,
protocol tests for MCP compliance and error handling.

Third,
agent tests for discoverability,
selection,
argument construction,
and recovery behavior.

That split matters because a secure tool that is consistently mis-selected is still a security problem.

Operationally,
logic and protocol tests fit naturally into every-commit workflows.
Agent-behavior tests are usually better for pull requests or nightly runs because they are slower but closer to deployment reality.

### Transition
At this point, teams usually ask: what is the minimum I should insist on before something is discoverable in production?

---

## Slide 19 — Day-1 baseline and 90-day roadmap

### Core message
You need a minimum production standard before you need a mature program.

### Talk track

Before an MCP-enabled workflow becomes discoverable in production,
I would insist on a day-one baseline.

A registry entry.
A named owner.
A scoped credential policy.
High-risk approval.
Mandatory telemetry.
And a containment baseline appropriate to the workflow.

That is the minimum production standard.

Then in the next thirty to ninety days,
standardize gateway patterns,
onboarding workflows,
metadata and output scanning,
and incident playbooks.

Longer term,
you want stronger registries,
signed artifacts,
policy-aware clients,
continuous recertification,
and safer defaults across the ecosystem.

### Transition
Now let me show you the second reusable artifact from this talk: the matrix.

---

## Slide 20 — The MCP Delegated-Authority Matrix: anatomy

### Core message
A threat model should produce action, not just a nice diagram.

### Talk track

The matrix I am proposing is deliberately simple.
Not because the problem is simple,
but because the artifact needs to survive contact with a real meeting room.

Each row is one realistic abuse story.

And each row answers a short list of operator questions.

What is the threat ID and domain?
What is the attacker trying to achieve?
At what lifecycle stage does it happen?
What is the impact?
What is the likelihood?
Who owns the primary guardrail?
What signal or quick test would expose it?
And what is the resulting priority?

That structure is inspired by attacker-behavior thinking,
by the enterprise MCP paper,
and by the useful presentation pattern in appendix-style threat matrices.
But it is tailored for MCP adoption teams.

### Transition
A matrix is only valuable if it works for more than one scary story, so let me show two different rows.

---

## Slide 21 — Matrix examples: read path and write path

### Core message
The matrix is reusable because the shape stays stable while the threat story changes.

### Talk track

Example one is a read-path problem.
Public issue content steers an agent toward privileged private-repo access,
and the result comes back looking helpful.

In the matrix,
that becomes a row with a clear goal,
a stage in the flow,
a guardrail owner,
a detection signal,
and a priority.

Example two is a write-path problem.
Now the question is not secret exposure.
It is whether a prompt-steered workflow can trigger a destructive connector action.

The controls change.
The telemetry changes.
The ownership may even shift.
But the matrix shape still holds.

That is the point.
You stop collecting folklore,
and you start collecting prioritized threat rows.

### Transition
So let me close with the simplest possible next step.

---

## Slide 22 — Final checklist and call to action

### Core message
Start with one workflow and one risky path.

### Talk track

If you take only one practical next step after this session,
make it this.

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

If your model can reach it,
your security model must explain it.

---

## Appendix A — Enterprise reference framework (Figure 2)

### Core message
This is the paper’s full enterprise framework, shown as reference material rather than as the main keynote artifact.

### Talk track

If somebody wants the denser enterprise version of the story,
this is it.

Figure 2 from the enterprise MCP security paper lays out the full layered framework:
client,
server,
runtime controls,
external services,
and the threat groupings around them.

It is useful.
But it is also exactly why I simplified the main talk into the five control planes.

On stage,
you want an artifact people can remember.
In architecture review,
you often want the fuller map.
This appendix gives you that fuller map.

### Transition
And if you want the paper’s category-level threat/control summary, that is the next appendix slide.

---

## Appendix B — Enterprise threat/control summary (Table I)

### Core message
This table is a good reference summary, but it is not the same kind of tool as the delegated-authority matrix.

### Talk track

Table I from the paper is useful because it maps broad threat categories to broad control families.

Tool poisoning.
Data exfiltration.
Command and control.
Identity and access control subversion.
Denial of service.
Insecure configuration.

That is a good enterprise reference view.

But notice what it does not do.
It does not give you one operator row per abuse story,
with a lifecycle stage,
a concrete owner,
a quick test,
and an implementation priority.

So this appendix table complements the main talk.
It does not replace the matrix.

If I were using both internally,
I would use Table I for category-level control mapping,
and the delegated-authority matrix for actual rollout prioritization.
