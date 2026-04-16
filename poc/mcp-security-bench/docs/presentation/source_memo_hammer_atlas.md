# Source Memo: Project Hammer and Anvil + MITRE ATLAS

Purpose: extract reusable checklist and matrix ideas for the MCP security keynote, deck, and paper.

Sources used:
- https://jitha-afk.github.io/ProjectHammerAndAnvil/
- https://github.com/Jitha-afk/ProjectHammerAndAnvil
- https://atlas.mitre.org/matrices/ATLAS
- Selected ATLAS technique pages used for grounding: AI Agent Tool Invocation, AI Agent Tool Poisoning, AI Agent Context Poisoning

Note: the Hammer and Anvil site had partial rendering glitches in the hero text, so the checklist JSON and repo README were used to verify structure and content.

## What Hammer and Anvil contributes that is original/useful for our talk

Hammer and Anvil is most useful as a curated MCP control corpus, not just as another “top 10” list.

What stands out:
- It organizes 234 controls across the full MCP operating stack, not only server hardening.
- It is already grouped in presentation-friendly domains: server, client/host, architecture, agentic behavior, execution, governance, and continuous validation.
- Each item is operationalized with priority, role mapping, and source references. That makes it much easier to turn into an executive scorecard or rollout checklist.
- It includes several MCP-native control ideas that are stronger than generic appsec advice:
  - no token passthrough
  - cryptographic tool manifests
  - tool version pinning and rug-pull prevention
  - tool description vs. behavior validation
  - cross-MCP function call control
  - multi-MCP environment scanning
  - memory segmentation by session/user
  - auto-approve restrictions
  - end-to-end request tracing across tool chains
- The repo’s contribution model is also useful: checklist changes are submitted as structured JSON and reviewed via PR workflow. That reinforces a good message for the talk: MCP security controls should be governed artifacts, not tribal knowledge.

Bottom line:
Hammer and Anvil gives us a practical way to say, “Here is what good looks like across the whole MCP lifecycle,” while still staying grounded in deployable controls.

## Which checklist domains or control clusters are most worth surfacing in a 45-minute keynote

Do not surface all 234 items. Surface 5 control clusters.

### 1. Identity brokering and delegated-authority control
Best Hammer and Anvil anchors:
- Server Authentication & Authorization
- Permission Token Storage & Management
- Session & Identity Isolation

Why it matters:
- This is where confused-deputy failures, token sprawl, over-broad scopes, and cross-tenant mistakes become real incidents.
- The strongest items here are no token passthrough, short-lived scoped tokens, sender-bound tokens, per-session isolation, and non-human identity governance.

### 2. Tool trust, provenance, and admission
Best Hammer and Anvil anchors:
- Tool Security & Integrity
- MCP Tools & Servers Management
- Governance Workflow

Why it matters:
- MCP adds a new problem: attackers do not just attack runtime, they compete to be discovered and trusted.
- This cluster lets us talk about manifests, version pinning, onboarding review, trusted registries, and conflict/shadow prevention.

### 3. Runtime containment and egress control
Best Hammer and Anvil anchors:
- Deployment & Runtime Security
- Unexpected Code Execution / RCE Prevention
- Multi-MCP Scenario Security

Why it matters:
- This is how teams reduce blast radius when a model makes a bad call or a tool goes bad.
- The strongest items are sandboxing, network segmentation, egress allowlists, SSRF prevention, and cross-MCP call control.

### 4. Context, memory, and output integrity
Best Hammer and Anvil anchors:
- Prompt Injection Controls
- Prompt Security
- Memory & Context Poisoning Prevention
- Sampling Security

Why it matters:
- This is the most MCP-specific control surface after identity.
- It covers indirect injection, hidden instruction channels, memory poisoning, unsafe output reuse, and context bleed.

### 5. Observability, review, and continuous validation
Best Hammer and Anvil anchors:
- Monitoring & Logging
- AI Asset Inventory & Threat Modeling
- AI Red Teaming

Why it matters:
- Platform teams need evidence, not hope.
- Good keynote material here includes request tracing across tool chains, immutable audit logs, anomaly detection, MCP-specific red teaming, and multi-turn attack simulation.

What to de-emphasize for this keynote:
- Cryptocurrency-specific controls should be a side note unless the audience is explicitly web3-heavy.
- The dedicated LLM execution section is useful, but most of its value is better folded into containment and output-handling slides.

## Which MITRE ATLAS attacker-behavior ideas can inspire an improved MCP threat-model matrix

ATLAS is valuable less as a taxonomy to copy and more as a design pattern: it models attacks as behaviors that progress across stages.

The most reusable ATLAS ideas for MCP are:

### 1. Tool invocation abuse as a first-class attacker move
Grounding:
- AI Agent Tool Invocation

Why it matters for MCP:
- MCP threats are often not “break crypto” or “break the model.” They are “get the agent to use a legitimate capability in the wrong way.”
- This is a better framing than generic “prompt injection” because it centers delegated action.

### 2. Tool poisoning as persistence, not just initial compromise
Grounding:
- AI Agent Tool Poisoning

Why it matters for MCP:
- A poisoned tool can remain trusted after onboarding and keep influencing many future sessions.
- This is a strong way to explain why provenance, signed releases, recertification, and behavior validation matter.

### 3. Context poisoning as durable control-channel abuse
Grounding:
- AI Agent Context Poisoning
- related matrix ideas around RAG poisoning and public-content prompt infiltration

Why it matters for MCP:
- MCP systems can be steered by memory, thread state, retrieved content, and tool output.
- This helps us frame memory and output handling as persistence risks, not just input-validation bugs.

### 4. Discovery of tool definitions, call chains, and configuration as attacker preparation
Grounding:
- matrix techniques around discovering agent configuration, tool definitions, activation triggers, and call chains

Why it matters for MCP:
- Before an attacker abuses tools, they often need to learn which tools exist, how they are named, and what sequence gets privileged actions.
- That supports a better matrix field for “attacker reconnaissance target” inside MCP.

### 5. Credential harvesting from agent/tool context
Grounding:
- matrix techniques around agent-tool credential harvesting, unsecured credentials, alternate auth material

Why it matters for MCP:
- MCP attacks often become serious only when combined with leaked or replayable authority.
- This strengthens the case for a dedicated identity/credential plane in our matrix.

### 6. Supply-chain compromise and reputation manipulation
Grounding:
- matrix ideas around AI supply chain compromise, poisoned tools, rug-pull behavior, and reputation inflation

Why it matters for MCP:
- MCP ecosystems are likely to have many third-party connectors, registries, and sample servers.
- Attackers can win before runtime by getting selected, approved, or updated into trust.

## Proposed ORIGINAL matrix structure for MCP, inspired by ATLAS but not a copy

Proposed name:
`MCP Delegated-Authority Matrix`

Design goal:
Track how attacker behavior moves through MCP trust surfaces, while still giving platform teams direct ownership, telemetry, and recovery actions.

Use one row per realistic abuse story.

Recommended columns:

| Column | Purpose |
|---|---|
| Trust plane | Where the abuse lives: identity, tool, context, runtime, network, governance |
| Flow stage | Where it happens in the MCP lifecycle: discover, select, approve, invoke, return, retain |
| Asset / capability at risk | What can actually be used, changed, or exposed |
| Attacker behavior | Plain-language action the attacker is trying to achieve |
| Preconditions | What must already be true for the attack to work |
| User-visible disguise | Why the action might look normal to a user or reviewer |
| Primary prevention control | Best control to stop it early |
| Detection / telemetry | What signal should expose it |
| Containment / recovery | What to do after detection |
| Owner | Team that must own the control |
| Priority | Practical prioritization: P0, P1, P2 |

Why this structure is better for MCP than a direct ATLAS copy:
- It keeps ATLAS’s behavioral mindset and stage-awareness.
- It adds the MCP-specific issue that matters most: delegated authority moving through trust planes.
- It is immediately usable by platform/security teams because every row ends with owner and recovery action.
- It is better for a keynote because it can be shown as a small, comprehensible worksheet rather than a giant taxonomy wall.

Recommended trust planes for the keynote version:
- Identity plane
- Tool plane
- Context plane
- Runtime plane
- Network plane
- Governance plane

Recommended flow stages for the keynote version:
- Discover
- Select
- Approve
- Invoke
- Return
- Retain

This left-to-right sequence is inspired by ATLAS’s progression model, but it is tailored to MCP’s actual operating flow.

## One worked example row for an MCP threat-model matrix

| Trust plane | Flow stage | Asset / capability at risk | Attacker behavior | Preconditions | User-visible disguise | Primary prevention control | Detection / telemetry | Containment / recovery | Owner | Priority |
|---|---|---|---|---|---|---|---|---|---|---|
| Tool plane + Context plane | Select -> Invoke -> Return | Internal code repo access via GitHub MCP tool | Attacker plants hidden instructions in public issue content so the agent selects the repo-reading tool, pulls sensitive files, and returns secrets in a “helpful” summary | Agent can read public issue content; tool has private repo scope; output is fed back into the model without strong filtering | Looks like routine triage or summarization work | Split public-content reading from privileged repo access; require scoped JIT credentials; high-risk tool approval; output redaction before model reuse | Trace showing public issue read followed by private repo calls; unusual repo enumeration; high-entropy output; cross-tool chain anomaly | Revoke tool token, quarantine session, block issue-derived context reuse, review accessed repos, rotate exposed secrets | Platform security + developer tools team | P0 |

## 5 concrete update recommendations for the deck/talk/paper

1. Replace the current broad threat-model close with one new slide that shows the `MCP Delegated-Authority Matrix` and explains the six MCP flow stages: discover, select, approve, invoke, return, retain.

2. Add one checklist slide built from Hammer and Anvil’s strongest clusters, not from all sections. Use five executive buckets: identity, tool trust, containment, context integrity, observability.

3. Rework the incident section so each example maps to a trust plane and flow stage. That will make the talk feel more original and more architectural than a sequence of anecdotes.

4. Add a paper subsection on “tool trust as a lifecycle control” using Hammer and Anvil items such as manifests, version pinning, onboarding review, trusted registry, and recertification. This is currently under-emphasized and is a strong differentiator.

5. Add one worked matrix row to the paper and deck notes, using a public-content-to-private-tool abuse chain. This gives the audience something reusable the next day, not just something memorable on stage.

## Quick citation notes

Hammer and Anvil facts used here:
- 234 total items
- Section structure: server (90), client/host (50), architecture (17), agentic (46), LLM execution (5), governance (19), crypto-specific (7)
- Example control clusters verified from checklist JSON and repo README

ATLAS facts used here:
- Matrix progression model across attacker behaviors
- Technique pages verified for AI Agent Tool Invocation, AI Agent Tool Poisoning, and AI Agent Context Poisoning
