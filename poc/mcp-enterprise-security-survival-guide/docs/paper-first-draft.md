# Operationalizing Security for the Model Context Protocol in Enterprise Environments: Threats, Control Surfaces, Defensive Patterns, and Evidence-Grounded Deployment Guidance

Draft status: first full manuscript draft for issue #6. This version is intentionally evidence-labeled and should be read as a scoped research-and-practice draft rather than as a final paper.

Evidence tags used inline:
- [SPEC] — grounded directly in the MCP specification.
- [CITED-PRELIM] — supported by current project source synthesis, often at title/abstract/introduction depth.
- [HYPOTHESIS] — plausible proposal or inference that still needs direct validation.
- [LAB-PLANNED] — intended for repository-local proof-of-concept or evaluation work not yet completed.

## Abstract
The Model Context Protocol (MCP) is increasingly positioned as a practical way to connect language-model-based systems to tools, data sources, and enterprise workflows, yet the security implications of such integrations appear to be evolving faster than enterprise deployment guidance. Drawing on the current project brief, preliminary source inventory, claim ledger, threat model, and validation plan assembled for issue #6, this draft argues that the main near-term problem is not merely that MCP expands attack surface, but that enterprises lack sufficiently operational guidance for interpreting the latest specification surface in deployable control terms. [SPEC] [CITED-PRELIM]

This paper treats MCP security as a layered enterprise systems problem involving authorization, transport exposure, filesystem boundary declarations, elicitation interfaces, sampling-mediated trust chains, server onboarding, and cross-server composition. Several recent sources preliminarily highlight malicious server metadata, tool-description poisoning, and trust propagation across tools and servers as plausible enterprise concerns, although the present evidence base in this repository remains preliminary for many literature-backed claims. [CITED-PRELIM] At the same time, the latest MCP specification appears to introduce or sharpen security-relevant surfaces, including Streamable HTTP deployment guidance, OAuth-related authorization patterns, roots, and elicitation constraints, that may not yet be fully operationalized in the early MCP security literature surveyed so far. [SPEC] [CITED-PRELIM]

The contribution framed here is intentionally modest. Rather than claiming comprehensive protocol insecurity or validated universal defenses, the paper offers an evidence-grounded enterprise security guide with five elements: a latest-spec deployment interpretation, an enterprise threat model, a scenario-based risk framing, a layered defensive control framework, and a validation program that clearly separates current evidence from planned proof-of-concept work. Proposed patterns such as policy gateways, provenance-aware mediation, capability leases, and trust-tier enforcement are presented as promising directions for staged validation rather than established results. [HYPOTHESIS] [LAB-PLANNED]

## 1. Introduction
Enterprises are under growing pressure to connect language-model-based assistants to internal tools, external services, and organization-specific data. In that setting, MCP appears attractive because it offers a structured interface for tool and resource access rather than requiring ad hoc integrations for every model-enabled workflow. [SPEC] However, the same standardization that may improve interoperability also appears to create a more legible and reusable attack surface for malicious servers, deceptive tool descriptions, cross-system trust confusion, and unsafe delegation of privileged actions. [CITED-PRELIM]

The current project materials suggest that the literature already pays substantial attention to attack discovery, malicious server behavior, and benchmark-style evaluation. [CITED-PRELIM] By contrast, the most actionable enterprise problem may be the translation of those observations into deployment guidance that is specific to the current MCP specification and sufficiently concrete for platform, security, and governance teams. [CITED-PRELIM] [HYPOTHESIS] In other words, the central question is not simply whether MCP can be abused, but which controls should be treated as mandatory before pilot deployment, which controls are context-dependent, and which proposed mitigations still require repository-local validation before they can be described as findings. [HYPOTHESIS] [LAB-PLANNED]

This framing encourages a deliberately cautious stance. The project brief explicitly excludes sweeping ecosystem claims, premature publication of strong results, and the unqualified transfer of generic LLM security advice into MCP-specific conclusions. Consistent with that scope, this paper treats the latest MCP specification as a security-relevant design surface, but not as direct evidence of real-world implementation behavior. [SPEC] It also treats the preliminary literature inventory as informative but not yet equivalent to a completed systematic review, because several current claim candidates are grounded only at title, abstract, or introduction depth in the source set currently summarized in the repository. [CITED-PRELIM]

Accordingly, the paper's intended value is practical and bounded. It seeks to provide enterprise readers with a disciplined way to reason about MCP adoption under uncertainty: identify the main trust boundaries, map the latest specification features to plausible failure modes, define a minimal control stack, and make clear which assertions are supported by cited material, which derive directly from the specification, and which remain hypotheses awaiting proof-of-concept evaluation. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

## 2. Background and latest-spec deployment surface
At a high level, the project materials frame MCP as a protocol for connecting model-driven applications to tools, resources, prompts, and related interaction surfaces through client-server coordination. The current draft treats this not merely as a messaging format, but as an enterprise deployment pattern in which model intent, policy mediation, server capabilities, identity systems, and downstream enterprise assets interact across multiple trust boundaries. [SPEC] [CITED-PRELIM]

For enterprise deployment, the latest MCP specification appears especially important in at least six areas. First, the specification introduces or formalizes authorization expectations associated with OAuth 2.1-related flows, protected resource metadata, and optional dynamic client registration for applicable remote deployments. This matters because enterprise risk depends not only on whether authentication exists, but on how identities, scopes, and delegated permissions are represented between user, client, and server roles. [SPEC] The project materials therefore treat per-user scoped authorization as a likely high-value control direction, but they stop short of claiming MCP-specific empirical proof at this stage. [SPEC] [HYPOTHESIS]

Second, the source inventory emphasizes that Streamable HTTP has become a security-relevant transport surface in the current specification, replacing older assumptions tied to HTTP plus server-sent events. The same materials note explicit guidance around Origin validation and localhost binding for local deployments, which makes transport hardening a first-order enterprise concern rather than an implementation footnote. [SPEC] Because the present repository has not yet run transport experiments, these specification features should be treated as factors that deserve explicit enterprise review and planned validation rather than as already-established protection outcomes. [LAB-PLANNED]

Third, the specification's treatment of roots appears to elevate filesystem boundary declarations into a meaningful confinement primitive. In an enterprise context, that may matter wherever assistants or tool-enabled workflows interact with local files, synced drives, or developer workstations. [SPEC] Yet the source inventory suggests that current MCP security literature has focused more heavily on malicious tools, prompt injection, and server behavior than on proving or stress-testing roots as an enforceable boundary under adversarial guidance. [CITED-PRELIM] This makes roots a notable example of a feature that is normatively defined in the specification while remaining only partially characterized in the current research picture. [SPEC] [CITED-PRELIM]

Fourth, elicitation appears to be a distinct deployment surface rather than a minor user-interface detail. The repository inputs indicate that the latest specification differentiates form mode from URL mode and explicitly prohibits collection of secrets through form mode. [SPEC] For enterprise defenders, this suggests that credential collection, consent signaling, domain disclosure, and client UX policy should be considered part of the security model. Whether these mechanisms materially reduce credential-harvesting risk in practice remains an open question for later experimentation. [HYPOTHESIS] [LAB-PLANNED]

Fifth, sampling and tool-use interactions seem to create a nested trust problem. The preliminary source inventory notes that the current specification supports sampling requests and tool use within that flow, while also soft-deprecating some cross-server context behavior. [SPEC] In enterprise settings, this may complicate provenance, intent verification, and the separation of low-trust outputs from high-impact downstream actions, especially when multiple servers or tools participate in a single workflow. [CITED-PRELIM] [HYPOTHESIS]

Sixth, server-side tools, resources, prompts, and change-notification flows broaden the operational surface that enterprises must inventory and govern. The research materials repeatedly suggest that instruction-carrying metadata is not merely descriptive; it may itself become part of the attack path. [CITED-PRELIM] As a result, enterprise deployment background for MCP must include not only protocol roles and message flow, but also registry decisions, provenance handling, allowlisting, and audit design. [CITED-PRELIM] [HYPOTHESIS]

Taken together, these features suggest that the latest specification should be read as both an interoperability standard and a deployment-security map. Some surfaces are directly grounded in the spec text; others become enterprise-relevant because the preliminary literature points to failure modes around server trust, tool mediation, and composition effects. [SPEC] [CITED-PRELIM] The core implication for this paper is that any enterprise guidance worth publishing should remain explicit about this distinction.

## 3. Threat model framing and paper contributions
The project materials support a threat model in which the principal security problem is not a single malicious prompt, but a distributed system of partially trusted actors, artifacts, and control planes. For this draft, however, the primary evaluation focus remains broker-observable and server-mediated threats, with broader compromised-client and adversarial-user coverage included only where it can be exercised through the same control path. The relevant assets include enterprise data, credentials, filesystem access, network reachability, tool invocation rights, policy decisions, logs, and the integrity of trust labels or provenance claims that shape subsequent actions. [CITED-PRELIM] [SPEC] Adversaries may include malicious users, compromised or deceptive MCP servers, poisoned tool metadata, cross-server confused-deputy chains, supply-chain threats in server onboarding, and ordinary model errors that become security-significant when coupled to privileged tools. [CITED-PRELIM]

A reference enterprise deployment for this paper assumes a host application or broker receiving model-generated tool intents; multiple MCP servers across trust levels; sensitive tool classes including file, network, shell, identity-bearing, and write-capable operations; a policy layer able to allow, deny, or require approval; and supporting systems for authorization, provenance, logging, and emergency disablement. [SPEC] [CITED-PRELIM] The core trust boundaries run between user and host, model and policy gateway, broker and servers, mixed-trust servers, MCP layers and enterprise systems, workstation-local execution context and remote authorization domains, and execution paths versus audit or approval systems. [SPEC] [HYPOTHESIS]

This framing is consistent with the current ledger's strongest observations: MCP appears to expand attack surface beyond classic prompt injection; malicious tool descriptions and server metadata appear to be recurrently highlighted candidate attack vectors; and cross-server trust propagation may enable privilege escalation or exfiltration even when no single component is catastrophic in isolation. [CITED-PRELIM] At the same time, the ledger recommends that several important defenses remain hypotheses until experiments are run, including policy-gateway efficacy, roots enforcement under attack, elicitation restrictions for credential protection, response normalization, and formal assurance for a small enforcement core. [HYPOTHESIS] [LAB-PLANNED]

The draft's contributions are therefore intentionally bounded. First, it offers a latest-spec deployment interpretation for enterprise readers. Second, it proposes an enterprise threat-model lens that centers trust boundaries and mediation points rather than isolated vulnerabilities. Third, it provides an evidence-discipline model for MCP security writing by separating specification facts, preliminary source-backed observations, analogical enterprise guidance, and still-unvalidated proposals. Fourth, it translates that framing into a concrete control stack and rollout model. Fifth, it defines a validation plan that could later promote selected claims from [HYPOTHESIS] to [LAB-PLANNED] and eventually to lab-backed findings. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

## 4. Enterprise risk scenarios and abuse cases
This section translates the threat-model framing into concrete enterprise scenario families. The aim is not to claim that every scenario is already broadly observed in production, but to identify where the current specification surface and the preliminary literature most plausibly intersect with enterprise trust boundaries. Unless noted otherwise, the scenario families below are grounded either in the latest MCP specification features summarized in the repository or in preliminary literature signals captured in the source inventory, bibliography notes, and claim ledger. [SPEC] [CITED-PRELIM]

### 4.1 Malicious server metadata and tool-description poisoning
A recurring concern in the current source set is that MCP server metadata should not be treated as passive description. The project literature synthesis repeatedly characterizes tool descriptions, prompts, and related server-provided fields as instruction-carrying channels that can shape model planning and tool selection. The resulting enterprise abuse case is straightforward: a server that appears operationally useful can embed coercive or misleading instructions in its metadata so that the client or model is steered toward unsafe invocation sequences, excessive data disclosure, or misleading approval requests. [CITED-PRELIM]

This scenario matters in enterprise environments because MCP explicitly exposes tools, resources, prompts, and change-notification flows as first-class protocol surfaces rather than accidental side channels. That architectural choice does not by itself prove exploitation in a given deployment, but it does mean that descriptive text and capability metadata may sit on the execution path for real business actions. [SPEC] A cautious enterprise reading is therefore that server discovery, onboarding, and runtime mediation all become security-relevant, especially when third-party servers are mixed with internal ones. [HYPOTHESIS]

### 4.2 Delegated-authority failures and confused-deputy execution
A second scenario family concerns delegated authority: who is actually acting when an MCP-mediated tool call reaches a protected enterprise system? The current specification surface gives unusual weight to authorization design, including OAuth-related flows and protected-resource metadata for applicable remote deployments. The project materials accordingly emphasize that model output should not be conflated with authorization, and that remote tool use should be bound as clearly as possible to user identity, server identity, and scope. [SPEC]

The abuse case arises when that binding is weak. Shared static credentials, over-broad scopes, or poor separation between user identity and agent identity can let a malicious server, deceptive workflow, or confused model induce actions that appear policy-compliant while exceeding user intent. In practice, this scenario family is especially important for enterprises because it converts ordinary planning errors into authorization failures with real side effects. A low-trust component does not need full compromise if it can influence a higher-trust actor that already holds broad credentials. [CITED-PRELIM] [HYPOTHESIS]

### 4.3 Streamable HTTP, roots, and workstation boundary erosion
The local deployment surface creates a third scenario family in which transport exposure, filesystem reachability, and workstation credential context interact. The project inputs note that Streamable HTTP now carries explicit security implications, including Origin validation and localhost binding guidance for local deployments. They also note that local stdio servers commonly rely on environment-scoped credentials rather than the remote HTTP authorization model. [SPEC]

The enterprise abuse case is therefore not limited to a single network bug. A weakly exposed local server may become reachable through origin confusion or rebinding-style interaction paths; a permissive client may expose roots that are declared but not robustly enforced; and a workstation-scoped stdio server may inherit credentials or filesystem reach far beyond what the user expects for the current task. This is a scenario family where the distinction between normative boundary declaration and effective boundary enforcement is especially important. Roots are specification-level confinement hints, but the repository does not yet treat them as empirically proven protections under adversarial prompting, path reshaping, or indirect server guidance. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

### 4.4 Elicitation abuse and consent-channel manipulation
Elicitation introduces a fourth scenario family centered on consent, disclosure, and secret collection. The latest specification distinguishes form mode from URL mode and explicitly prohibits collecting secrets through form mode. Within the project materials, this feature is treated as security-relevant rather than as a minor interface detail, because enterprise users may interpret an elicitation prompt as an approved part of the client workflow even when the initiating server is only semi-trusted. [SPEC]

The concrete abuse case is a malicious or deceptive server that uses elicitation to request credentials, sensitive business data, or approvals under misleading framing. Even without directly violating the protocol, weak client UX could still blur destination, identity, or risk level enough to enable consent confusion or approval fatigue. The strongest support here is for plausibility and importance rather than for settled empirical results. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

### 4.5 Cross-server trust chains, sampling-mediated escalation, and provenance loss
The fifth scenario family concerns composition effects across servers, especially when sampling and tool use create nested delegation paths. The source inventory and claim ledger repeatedly identify cross-server trust propagation as a central enterprise concern, and the threat model elevates low-trust-to-high-trust action flow as the core mediation problem. [CITED-PRELIM] At the same time, the specification notes that sampling requests may themselves interact with tool use, which makes generation behavior potentially relevant to execution control rather than merely to text production. [SPEC]

A representative abuse case begins with a low-trust server producing content, metadata, or a sampling request that appears informational, but that content later influences a more trusted server or tool router. If provenance is absent, stripped, or ignored, downstream policy may no longer distinguish attacker-controlled output from trusted operational context. In enterprise settings, that can yield exfiltration, privilege escalation, or other confused-deputy behavior even when no individual server appears overwhelmingly powerful in isolation. [CITED-PRELIM] [HYPOTHESIS]

In synthesis, the best first-wave validation targets appear to be scenario families that map most directly to explicit specification surfaces and observable policy outcomes: delegated-authority failures around scoped authorization, local boundary failures involving Streamable HTTP and roots, elicitation abuse around secret collection and consent signaling, and cross-server trust-chain cases where provenance-aware mediation can be tested against clear escalation paths. Metadata-poisoning scenarios remain strategically important, but they may be slightly harder to validate cleanly without a stable benchmark corpus of malicious descriptions. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

## 5. Defensive control framework for enterprise MCP deployments
This section proposes a layered enterprise control model that connects the threat surfaces in the current specification and the project threat model to concrete defensive control points. The framework is intentionally cautious: some elements are directly motivated by the latest specification, some are consistent with preliminary MCP security literature, and several higher-order controls remain deployment hypotheses that should be validated in the planned lab environment before being described as measured results. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

The central design assumption is that enterprise MCP risk is produced less by any single mechanism than by unsafe trust transitions: model output is mistaken for authorization, server metadata is treated as trustworthy planning guidance, low-trust server output silently influences high-trust actions, or transport and filesystem boundaries are declared but not enforced. A defensible control framework therefore appears to require multiple layers that constrain identity, transport exposure, execution rights, data movement, and trust propagation at the same time. [SPEC] [CITED-PRELIM] [HYPOTHESIS]

### 5.1 Control principles
Four principles organize the framework.

First, authorization should be interpreted as a separate decision point rather than an emergent property of model behavior. Model intent, server suggestions, and tool descriptions may help propose an action, but they should not themselves determine whether an action is permitted. [SPEC] [HYPOTHESIS]

Second, trust should not be treated as transitive across servers, tools, or sampling flows. Preliminary literature signals suggest that cross-server influence and malicious tool or server metadata are credible concerns, which implies that enterprise deployments should assume that low-trust content may attempt to shape higher-trust execution paths. [CITED-PRELIM] [HYPOTHESIS]

Third, boundary declarations are only meaningful if they are enforced under adversarial conditions. This is especially relevant for Streamable HTTP exposure decisions, roots-based filesystem constraints, and elicitation restrictions for sensitive input. [SPEC] [HYPOTHESIS] [LAB-PLANNED]

Fourth, failures on protected paths should tend to fail closed. Missing provenance, ambiguous path resolution, unsafe secret-collection mode, or absent policy state should generally trigger denial, quarantine, or approval rather than silent continuation. [SPEC] [HYPOTHESIS]

### 5.2 Layered control stack
1. Admission and governance
   - Objective: prevent unsafe servers from entering the deployment path without review.
   - Controls: private registry or allowlist, capability review, metadata review, ownership assignment, change control for server enablement.
   - Threats addressed: malicious server onboarding, deceptive capability claims, untracked external dependencies. [CITED-PRELIM] [HYPOTHESIS]

2. Identity and authentication
   - Objective: bind actions to the correct user, client, and server context.
   - Controls: per-user scoped authorization for remote servers, short-lived tokens where feasible, separation of user identity from broker identity, explicit scope design.
   - Threats addressed: shared-credential blast radius, token mix-up, confused deputy through identity ambiguity. [SPEC] [CITED-PRELIM]

3. Transport and endpoint hardening
   - Objective: reduce exposure created by remote and local protocol surfaces.
   - Controls: strict Origin validation, localhost-only binding for local deployments where possible, explicit remote exposure decisions, network segmentation, transport-specific hardening checklists.
   - Threats addressed: DNS rebinding, origin confusion, unintended endpoint reachability, migration mistakes. [SPEC] [HYPOTHESIS] [LAB-PLANNED]

4. Policy mediation and authorization enforcement
   - Objective: ensure that no high-impact action bypasses enterprise policy.
   - Controls: broker or policy gateway between model intent and tool execution, deterministic allow/deny logging, approval-required states, same policy path for direct tool use and sampling-triggered tool use.
   - Threats addressed: unauthorized tool invocation, sampling as second-order execution path, inconsistent approval decisions. [HYPOTHESIS] [LAB-PLANNED]

5. Capability scoping and containment
   - Objective: limit what a permitted action can actually touch.
   - Controls: least-privilege tool design, roots enforcement, path canonicalization, sandboxing or isolation for risky tools, read-only defaults for early phases.
   - Threats addressed: over-broad file access, out-of-scope writes, shell or network abuse, path-manipulation bypass attempts. [SPEC] [HYPOTHESIS] [LAB-PLANNED]

6. Interaction integrity and trust propagation control
   - Objective: keep attacker-controlled content from silently acquiring higher trust.
   - Controls: provenance metadata, trust tiers, taint-aware routing, response normalization, instruction-data separation, explicit treatment of server metadata as untrusted input, elicitation mode restrictions.
   - Threats addressed: malicious tool descriptions, tool-output prompt injection, cross-server escalation, credential harvesting through elicitation. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

7. Observability, response, and recovery
   - Objective: make misuse detectable and containable.
   - Controls: unified audit schema, alerting on policy denials and trust-tier upgrades, rapid token revocation, server disablement, kill-switches, incident runbooks.
   - Threats addressed: invisible policy bypass, incomplete forensics, slow containment, repeated server abuse. [CITED-PRELIM] [HYPOTHESIS]

The layers are best read as mutually reinforcing rather than as substitutes. Per-user authorization may reduce blast radius, but it does not by itself prevent malicious server metadata from influencing tool choice; roots may narrow file exposure, but they do not solve cross-server trust confusion; provenance labels may aid downstream policy, but only if a gateway consumes them before authorizing a sensitive action. [SPEC] [CITED-PRELIM] [HYPOTHESIS]

### 5.3 Conservative proposed starter stack for meaningful enterprise pilots
Under the current evidence state, a conservative proposed starter stack before a non-trivial enterprise pilot would appear to include: (1) a mediated policy decision point before tool execution; (2) per-user scoped authorization for remote servers where feasible; (3) Streamable HTTP hardening with explicit exposure choices; (4) roots or equivalent containment for filesystem access; (5) elicitation restrictions that keep secret collection out of unsafe modes; (6) provenance or trust labeling sufficient to distinguish low-trust from higher-trust outputs; and (7) unified audit logging with a tested emergency disable path. This list should be read as a cautious starting stack rather than a validated maturity model. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

## 6. Proposed defense techniques and deployment patterns
This section narrows the paper's more forward-looking contribution. The techniques below are not presented as validated results. Instead, they are framed as enterprise-deployable patterns that appear promising given the current specification surface, the preliminary literature, and the project threat model. Some are extensions of familiar security principles; others are tailored proposals for MCP-specific trust mediation. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

### 6.1 Trust-transition gateway
A central proposal of this draft is that enterprises should treat the broker as a trust-transition gateway rather than as a thin protocol relay. Under this model, every proposed tool action is evaluated against actor identity, server trust tier, capability class, argument risk, provenance state, and workflow phase before execution is allowed. The conceptual novelty here is not the existence of policy enforcement itself, but the explicit treatment of model-mediated actions as transitions across trust states rather than as ordinary API calls. [HYPOTHESIS] [LAB-PLANNED]

This framing appears useful because several of the highest-priority risks in the claim ledger share the same structure: a lower-trust source attempts to influence a higher-impact action without an explicit upgrade step. A trust-transition gateway would make those transitions visible and governable. The repository does not yet demonstrate that such a gateway can preserve benign task completion at acceptable cost, so this remains an experimental target rather than a claimed solution. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

### 6.2 Capability leases for delegated tool use
One candidate technique for reducing delegated-authority risk is a capability lease model in which high-impact permissions are short-lived, context-bound, and scoped to a narrow workflow rather than granted as standing ambient authority. In this pattern, a model or broker does not receive broad reusable credentials; instead, it receives narrowly time-limited permission to perform a specific class of action within a specific task context. [HYPOTHESIS]

The value of this proposal is that it translates least privilege into an MCP-native workflow shape. Shared credentials and broad OAuth scopes become harder to justify if the system can mint smaller, expiring grants that correspond to individual actions or narrowly grouped tasks. The current repository contains no implementation of capability leasing yet, so this is best described as a promising enterprise pattern requiring later prototype work and cost analysis. [SPEC] [HYPOTHESIS] [LAB-PLANNED]

### 6.3 Provenance envelopes and trust-tier propagation
A second proposal is to make provenance a first-class execution artifact rather than a logging afterthought. In this model, server responses carry a structured envelope containing server identity, tool identity, request hash, response hash, timestamp, trust tier, and possibly controlled-environment attestation metadata. Downstream policy can then distinguish between trusted observations, untrusted external content, and provenance-deficient material that should be downgraded or quarantined. [HYPOTHESIS] [LAB-PLANNED]

This proposal directly addresses the cross-server trust problem surfaced in the literature inventory and threat model. If untrusted server output can silently influence a privileged downstream action, then the absence of explicit provenance becomes part of the vulnerability. A provenance envelope does not by itself solve the problem, because downstream controls must actually consume and enforce it, but it may create a tractable basis for policy, replay, and later formalization. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

### 6.4 Roots-aware local containment and workstation capsules
The project materials suggest that local deployments deserve more attention than they often receive in generic security summaries. For local and stdio-heavy workflows, a useful pattern may be a workstation capsule that combines roots-aware path mediation, canonical path validation, environment scoping, and deny-by-default handling for ambiguous filesystem or credential contexts. [SPEC] [HYPOTHESIS]

The point of this proposal is to avoid treating roots as purely declarative hints. A roots-aware containment layer would actively resolve and validate candidate targets before execution and would separate low-risk read operations from write, shell, or network-capable tools that may need stronger sandboxing. This proposal is particularly attractive for proof-of-concept evaluation because its success criteria can be made concrete: either an out-of-root path is reachable under adversarial prompting, or it is not. [HYPOTHESIS] [LAB-PLANNED]

### 6.5 Elicitation escrow for sensitive inputs
Because elicitation appears to be part of the security model rather than a cosmetic UI feature, this draft proposes an elicitation escrow pattern for sensitive inputs. Under this pattern, potentially secret-bearing user input is not handed directly from a semi-trusted server prompt into the normal interaction flow. Instead, the client or broker routes the request through a dedicated trusted collection path that displays identity, destination, purpose, and permission context explicitly and logs the consent decision as a security-relevant event. [SPEC] [HYPOTHESIS]

This technique extends the specification's separation of form and URL modes into an enterprise-consent pattern. It does not yet have evaluation results in the repository, and it may introduce usability friction, but it appears to offer a more defensible way to handle secret collection than treating all elicitation as equivalent interaction. [SPEC] [HYPOTHESIS] [LAB-PLANNED]

### 6.6 Registry-centric capability attestation
A final forward-looking proposal is to strengthen server admission with registry-centric capability attestation. The idea is not to claim that server behavior can be universally proven from metadata, but to require that published capabilities, versions, ownership, and trust classification be explicit, reviewable, and ideally bound to signed manifests or attestations before a server becomes discoverable in a governed environment. Runtime behavior could later be compared against these declarations as part of admission review, recertification, or anomaly handling. In this draft, that proposal should be read as follow-on work rather than as a first-wave validated mechanism. [HYPOTHESIS] [LAB-PLANNED]

This proposal responds to a recurrent gap in the source inventory: enterprises may need more than scanning and allowlisting if malicious servers can look benign at onboarding time. Attestation will likely be imperfect, and the current draft does not claim otherwise. Its value may lie less in perfect detection and more in creating a stronger governance and accountability substrate for server lifecycle control. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

In summary, the proposed patterns in this section should be read as a research and engineering agenda anchored to enterprise deployment needs. Their importance to the paper lies not in present validation, but in giving the project a coherent set of defense hypotheses to test in a broker-centered, mixed-trust MCP environment. [HYPOTHESIS] [LAB-PLANNED]

## 7. Experimental evaluation plan and evidence boundaries
This section defines the methods that will be used to test the paper's defensive claims and to bound what the current draft can honestly say now. The method is threat-model-driven, spec-aware, and explicitly falsifiable: each evaluable claim must map to a concrete attacker action, a reproducible fixture, measurable success criteria, and a failure condition that would weaken or disprove the claim. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

The current repository state supports a design-level evaluation plan, not empirical findings. What is already demonstrated in this draft is the security-relevant deployment surface, the enterprise threat model, the claim-status discipline, and the prioritization of candidate controls. What is not yet demonstrated is quantitative defense efficacy, false-positive trade-offs, operator burden, or machine-checked assurance for any implementation. Those stronger statements remain planned evaluation targets only. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

### 7.1 Method and current evidence posture
The evaluation method combines four layers. First, the latest MCP specification supplies the normative surfaces that matter for enterprise deployment: authorization, Streamable HTTP exposure, roots, elicitation, sampling-with-tools, and provenance or trust handling. Second, the threat model converts those surfaces into attacker goals, trust boundaries, and failure modes relevant to enterprise brokers, mixed-trust servers, and sensitive tools. Third, the attack corpus translates those failure modes into replayable fixtures. Fourth, a narrow formal core is reserved for the broker-side enforcement logic rather than for the entire MCP ecosystem. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

Current status is deliberately split:
- Already established in-repo: reference threat assumptions, attack classes, validation workflow, and prioritized first-wave tracks. [SPEC] [CITED-PRELIM]
- Planned but not yet demonstrated: measured block rates, benign-task pass rates, latency overhead, approval burden, roots enforcement under attack, elicitation protection efficacy, transport-hardening efficacy, and formal proofs for the enforcement core. [HYPOTHESIS] [LAB-PLANNED]

### 7.2 Reference lab topology
The reference lab is intentionally minimal but representative of an enterprise MCP deployment. It centers on one host application or broker that receives model-generated tool intents and mediates execution through explicit policy decisions rather than prompt-only control. The broker connects to three server classes so that both single-server and cross-server failures can be exercised under the same harness. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

- Host application or broker
  - Role: receives model tool intents and applies allow, deny, or approval-required decisions.
  - Trust posture: high-trust control point.
  - Security purpose: main enforcement surface for policy, provenance, taint, and audit checks. [HYPOTHESIS] [LAB-PLANNED]

- Trusted internal MCP server
  - Role: exposes approved low-risk read tools and selected write-capable tools.
  - Trust posture: high trust.
  - Security purpose: baseline for legitimate enterprise workflows. [CITED-PRELIM] [LAB-PLANNED]

- Semi-trusted external MCP server
  - Role: exposes useful but less governed tools and resources.
  - Trust posture: partial trust.
  - Security purpose: tests whether external utility can be preserved without implicit transitive trust. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

- Adversarial or misconfigured MCP server
  - Role: supplies deceptive descriptions, unsafe outputs, or forged metadata.
  - Trust posture: low trust or attacker-controlled.
  - Security purpose: exercises prompt-channel abuse, provenance tampering, and cross-server escalation paths. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

- Sensitive tool classes
  - Role: file, network, shell, identity-bearing, and write-capable actions.
  - Security purpose: makes authorization correctness, roots, and trust transitions measurable. [SPEC] [HYPOTHESIS] [LAB-PLANNED]

- Approval, logging, and provenance layer
  - Role: records decisions and exposes trust lineage for review.
  - Security purpose: measures auditability and prevents silent privilege transitions. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

### 7.3 Attack corpus classes
The attack corpus is designed to cover the failure modes already identified in the threat model and claim ledger while preserving a benign baseline for false-positive measurement. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

1. Unauthorized tool or server selection.
2. Tool-output injection and instruction-data confusion.
3. Cross-server trust propagation and confused-deputy escalation.
4. Provenance tampering and metadata forgery.
5. Roots and path-resolution boundary escape attempts.
6. Elicitation abuse and unsafe secret collection.
7. Streamable HTTP exposure and origin-confusion cases.
8. Benign baseline tasks.

Sampling-triggered tool-use chains are treated as a cross-cutting case inside the unauthorized-selection and cross-server classes, because the risk of nested delegation is that low-trust requests can indirectly reach high-impact tools unless the same policy and trust checks apply. [SPEC] [HYPOTHESIS] [LAB-PLANNED]

### 7.4 Metrics and scorecard
All tracks are evaluated with the same core scorecard so that defenses can be compared on both security benefit and operational cost. Quantitative thresholds are provisional kickoff targets from the validation plan, not measured results. [HYPOTHESIS] [LAB-PLANNED]

Core metrics:
- Attack success rate.
- Defense block rate.
- Benign task success rate.
- False-denial or false-positive rate.
- Median latency overhead.
- Human approval burden.
- Policy coverage.
- Trust-lineage and audit completeness.
- Replay determinism.

### 7.5 First-wave validation tracks
The first implementation wave is intentionally limited to the three tracks already prioritized in the validation plan: a policy enforcement gateway, a provenance and integrity envelope, and multi-server trust controls with taint tracking. This subset best matches the enterprise-control focus of the paper and provides a realistic path to a later formal model of broker enforcement and trust transitions. Within that wave, Track 1 is also intended to carry auth-focused fixtures for shared credentials, scope overreach, and identity mix-up at the broker boundary, even if those checks are not treated as a standalone build track. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

Track 1: Policy enforcement gateway
- Tests whether an explicit broker-side policy layer can reduce unsafe tool or server selection without materially harming benign task completion.
- Provisional success targets: at least 95% blocking of unauthorized selection fixtures, at least 90% benign completion, deterministic decision logging for all attempted calls, and less than 50 ms median decision latency in replay mode. [HYPOTHESIS] [LAB-PLANNED]

Track 2: Provenance and integrity envelope
- Tests whether verifiable response metadata can reduce unsafe reliance on attacker-controlled outputs.
- Provisional success targets: detection of intentionally tampered fixtures, correct trusted-versus-untrusted origin distinction in logs, and prevention of most privileged follow-on actions triggered solely by untrusted output when policy requires trusted origin. [HYPOTHESIS] [LAB-PLANNED]

Track 6: Multi-server trust controls and cross-server taint tracking
- Tests whether trust-aware routing and taint propagation can stop low-trust outputs from silently authorizing high-trust actions.
- Provisional success targets: blocking most cross-server escalation fixtures, explainable trust lineage for privileged actions, and acceptable benign completion for multi-server workflows. [HYPOTHESIS] [LAB-PLANNED]

Roots enforcement, elicitation restrictions, and Streamable HTTP hardening remain first-wave claim targets at the fixture and scorecard level even though they are not separate first-wave build tracks. In practice, the first-wave corpus should include explicit probes for origin-validation and binding failures, out-of-root path attempts, unsafe secret-collection flows, and broker-observable adversarial-user or compromised-client perturbations that try to trigger the same protected actions through different entry points. [SPEC] [HYPOTHESIS] [LAB-PLANNED]

### 7.6 Formal-core validation approach
Formal work is intentionally scoped to a small enforcement core rather than to the full protocol, the model, or every server implementation. The purpose is not to claim mathematically proven safety for MCP as a whole, but to model-check the broker-side decision logic that is most security-critical and most amenable to precise specification. [HYPOTHESIS] [LAB-PLANNED]

The planned approach has three layers:
1. Formal model layer — specify the broker policy and trust-state machine in a compact notation suitable for state exploration, such as TLA+ or Alloy. [HYPOTHESIS] [LAB-PLANNED]
2. Reference implementation layer — build one small enforcement core whose inputs, outputs, and state transitions match the formal model closely enough to support traceability. [HYPOTHESIS] [LAB-PLANNED]
3. Conformance layer — use replay traces and property-based tests to check that implementation behavior conforms to the modeled invariants under normal, adversarial, and malformed inputs. [HYPOTHESIS] [LAB-PLANNED]

Initial proof targets are narrow and practical: policy non-bypass, trust monotonicity across servers and tainted outputs, and fail-closed handling when provenance is missing, malformed, or ambiguous. Roots or capability confinement should be treated as formal targets only to the extent that canonicalization and capability checks are implemented inside the broker-controlled enforcement core; otherwise they should remain empirical validation targets rather than proof claims. [HYPOTHESIS] [LAB-PLANNED]

### 7.7 Evidence boundaries for this draft
The draft can already make some bounded claims, but only at the right evidence level. It cannot yet make lab-backed efficacy claims.

- Specification facts
  - Can say now: the latest MCP specification defines security-relevant surfaces such as authorization, Streamable HTTP guidance, roots, elicitation constraints, and sampling or tool interactions. [SPEC]
  - Cannot say yet: that these mechanisms are consistently implemented correctly or effective in production. [HYPOTHESIS] [LAB-PLANNED]

- Preliminary literature observations
  - Can say now: multiple sources preliminarily indicate attack-surface expansion, malicious metadata or tool-description risk, and cross-server trust problems. [CITED-PRELIM]
  - Cannot say yet: ecosystem-wide prevalence rates, settled consensus, or benchmark-grade effect sizes for defenses. [HYPOTHESIS] [LAB-PLANNED]

- Enterprise control guidance
  - Can say now: the paper may recommend bounded controls such as policy gateways, scoped authorization, provenance handling, trust tiering, and auditability as design guidance. [SPEC] [CITED-PRELIM] [HYPOTHESIS]
  - Cannot say yet: that any one of these controls already reduces risk by a measured amount in this repository. [HYPOTHESIS] [LAB-PLANNED]

- Quantitative defense claims
  - Can say now: the paper may publish provisional thresholds as evaluation targets and falsification criteria. [HYPOTHESIS] [LAB-PLANNED]
  - Cannot say yet: measured block rates, false-positive rates, latency numbers, or operator-burden reductions. [HYPOTHESIS] [LAB-PLANNED]

- Formal assurance claims
  - Can say now: the paper may describe a narrow formalization strategy for the broker core. [HYPOTHESIS] [LAB-PLANNED]
  - Cannot say yet: machine-checked proofs, verified conformance, or mathematically proven end-to-end MCP security. [HYPOTHESIS] [LAB-PLANNED]

## 8. Operational guidance, rollout sequencing, and trade-offs
Because the repository does not yet contain empirical findings from the planned prototypes, this section translates the Section 5 framework into staged operational guidance rather than outcome claims. The aim is to help enterprises decide how to sequence rollout, where to apply stricter controls first, and when to stop or narrow deployment if the control environment is immature. Every recommendation below should therefore be interpreted as provisional deployment guidance under uncertainty. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

### 8.1 A staged rollout ladder
A cautious enterprise rollout appears better framed as a ladder of increasing trust and autonomy than as a binary enabled-versus-disabled decision. The same control stack may be relevant in all phases, but the acceptable defaults, approval thresholds, and exposure radius should differ substantially. [HYPOTHESIS]

Phase 0: Sandbox or lab
- Scope: single internal or intentionally instrumented test server; synthetic or low-sensitivity data; read-only or no-side-effect tools where possible.
- Hard-to-defer controls: policy gateway, full logging, isolated environment, explicit server inventory, deny-by-default networking, manual approval for any write-capable action.
- Exit criteria: operators can explain all execution paths, disable a server quickly, and review coherent logs for auth, tool, and policy events. [LAB-PLANNED]

Phase 1: Controlled pilot
- Scope: small user cohort, narrow workflow scope, limited production-like data, preferably one trust tier at a time.
- Hard-to-defer controls: per-user scoped authorization for remote servers, transport hardening, roots or equivalent filesystem confinement, approval gates for sensitive actions, registry allowlisting.
- Exit criteria: the pilot can run without repeated policy surprises, approval fatigue remains manageable, and no control class is routinely bypassed for convenience. [SPEC] [HYPOTHESIS]

Phase 2: Limited production
- Scope: more users, selective write-capable actions, defined external dependencies, formal on-call ownership.
- Hard-to-defer controls: trust tiering, provenance-aware routing, incident runbooks, token revocation, server disablement, tighter change control for new servers or capabilities.
- Exit criteria: security and platform teams can reconstruct incidents end to end and contain a problematic server without broad service interruption. [CITED-PRELIM] [HYPOTHESIS]

Phase 3: Broader deployment
- Scope: multiple workflows, mixed trust domains, stronger operational dependence on MCP-mediated actions.
- Hard-to-defer controls: periodic control review, regression testing for policy and roots behavior, cross-server trust restrictions, measured approval tuning, governance for server lifecycle changes.
- Exit criteria: expansion is justified only if earlier phases show stable control operation and acceptable operator burden; absent that, scope should remain narrow. [HYPOTHESIS] [LAB-PLANNED]

### 8.2 High-priority controls to consider before pilot deployment
Three categories of controls appear especially high priority to consider before exposing meaningful enterprise tools in a pilot.

First, enterprises likely need identity and policy discipline before exposing meaningful tools. If a deployment cannot distinguish user identity from broker or service identity, or cannot bind execution to explicit scopes and policy decisions, then later logging and detection may record misuse without meaningfully preventing it. [SPEC] [HYPOTHESIS]

Second, enterprises likely need concrete boundary enforcement for current specification surfaces that directly touch exposure and data access. This includes Streamable HTTP hardening, roots or equivalent filesystem constraints, and elicitation handling that keeps secret collection inside safer, disclosed flows. Without these, the deployment may rely on boundary declarations that exist on paper but not in operation. [SPEC] [HYPOTHESIS] [LAB-PLANNED]

Third, enterprises likely need enough provenance and logging to reconstruct trust transitions. The threat model suggests that MCP incidents may involve subtle multi-step influence rather than one obvious exploit event, so the inability to connect discovery, authorization, elicitation, sampling, tool use, and final side effects would materially weaken response and governance. [CITED-PRELIM] [HYPOTHESIS]

### 8.3 Operational trade-offs
The controls most likely to reduce trust-propagation risk also tend to increase friction at precisely the points where developers want convenience: onboarding new servers, granting broader scopes, suppressing approval prompts, or allowing richer tool access.

- Per-user scoped authorization instead of shared credentials
  - Likely benefit: smaller blast radius and clearer accountability for remote actions.
  - Likely cost: more integration work with identity systems and more token lifecycle complexity.
  - Stance: plausible baseline for remote enterprise deployments, but local efficacy is not yet measured. [SPEC] [HYPOTHESIS]

- Strict approval gates for sensitive tool calls
  - Likely benefit: lower chance that low-trust influence silently reaches high-impact actions.
  - Likely cost: slower workflows, reviewer fatigue, user frustration, pressure to over-broaden allowlists.
  - Stance: advisable early, then tune carefully; excessive prompting may erode its own value. [CITED-PRELIM] [HYPOTHESIS]

- Private registry or allowlisted server onboarding
  - Likely benefit: lower exposure to malicious or poorly understood servers.
  - Likely cost: slower experimentation and higher governance burden.
  - Stance: appears appropriate for enterprise settings with meaningful data or write capability. [CITED-PRELIM] [HYPOTHESIS]

- Provenance labels and trust-tier routing
  - Likely benefit: better separation of low-trust and high-trust outputs across multi-server workflows.
  - Likely cost: added metadata handling, policy complexity, and possible interoperability friction.
  - Stance: promising, but especially in need of prototype validation before strong external claims. [HYPOTHESIS] [LAB-PLANNED]

- Strong roots enforcement and sandboxing
  - Likely benefit: reduced file and host-level blast radius.
  - Likely cost: tool limitations, developer inconvenience, false positives on legitimate workflows.
  - Stance: likely worthwhile for higher-risk tools, though usability effects remain to be characterized locally. [SPEC] [HYPOTHESIS]

- Aggressive deny-by-default transport exposure
  - Likely benefit: smaller attack surface and fewer accidental endpoint exposures.
  - Likely cost: harder developer setup and possible resistance during early adoption.
  - Stance: seems justified where MCP endpoints can reach valuable enterprise systems. [SPEC] [HYPOTHESIS]

### 8.4 Recommended decision rules for scope restriction or deferral
The current inputs suggest several cases where enterprises should consider restricting scope sharply or deferring deployment altogether.

- If remote server actions cannot be tied to user-scoped authorization or an equivalent compensating control, deployment should likely remain narrow and low impact. [SPEC] [HYPOTHESIS]
- If filesystem, shell, or network-capable tools cannot be meaningfully contained through roots, sandboxing, or comparable boundaries, read-only or synthetic-data use may be the safer interim posture. [SPEC] [HYPOTHESIS] [LAB-PLANNED]
- If the organization cannot maintain coherent logs across discovery, policy, sampling, elicitation, and execution, incident response and accountability may be too weak for broader rollout. [CITED-PRELIM] [HYPOTHESIS]
- If low-trust external servers are expected to influence high-trust internal actions without provenance-aware mediation or approval, multi-server composition should likely be restricted until stronger controls exist. [CITED-PRELIM] [HYPOTHESIS]
- If approval fatigue or exception handling becomes the normal operating mode during the pilot, that should be treated as a control-design warning rather than as evidence that the controls are unnecessary. [HYPOTHESIS]

### 8.5 Residual risk and near-term research needs
Even a disciplined rollout would leave residual risk. The repository materials do not yet establish how well current clients enforce roots under attack, how reliably operators interpret provenance or trust labels, how much usability cost strict elicitation and approval policies impose, or how much cross-server taint-tracking is needed in realistic mixed-trust deployments. Those uncertainties matter because they shape whether the proposed framework is merely conceptually attractive or operationally sustainable. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

The practical conclusion is restrained: enterprises may be able to pilot MCP safely only when the deployment is deliberately narrow, policy-mediated, identity-aware, and operationally observable. Broader automation across mixed-trust servers may eventually be supportable, but the current repository inputs justify describing that outcome as contingent on later validation rather than as an established result. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

## 9. Limitations and open questions
This draft has several important limits that should be stated plainly.

First, the current literature synthesis is preliminary. Several source-backed claims are grounded at title, abstract, or introduction depth rather than at full close-reading depth, which means the paper can legitimately state directional findings and recurring themes more readily than it can state settled empirical consensus. [CITED-PRELIM]

Second, the draft is specification-aware but not implementation-complete. The MCP specification can define security-relevant surfaces, but that does not guarantee that current clients, brokers, or servers implement them consistently or robustly. Some of the most practically important claims in this paper, such as roots enforcement under adversarial prompting or elicitation safety in real clients, remain open exactly because specification text does not substitute for deployment evidence. [SPEC] [HYPOTHESIS] [LAB-PLANNED]

Third, the paper is explicitly enterprise-centered. That focus is useful for the issue's goal, but it means the guidance may over-index on governance, mixed-trust server composition, authorization, and auditability relative to lighter-weight hobbyist or single-user deployments. Some controls that appear necessary for enterprise pilots may be disproportionate elsewhere, while some consumer-oriented risks may be underexplored here. [HYPOTHESIS]

Fourth, the most original proposals in the draft are not yet validated. Trust-transition gateways, capability leases, provenance envelopes, elicitation escrow, and registry-centric capability attestation are presented as plausible and potentially useful techniques, but the repository has not yet shown their efficacy, overhead, or failure modes. [HYPOTHESIS] [LAB-PLANNED]

Fifth, the formal-assurance component remains only a plan. This draft can argue that a narrow formal model of broker enforcement is both realistic and valuable, but it cannot yet claim any machine-checked results, verified conformance, or mathematical security proof for MCP deployments. [HYPOTHESIS] [LAB-PLANNED]

These limitations generate several open questions for the next phase of work:
- Which current clients actually enforce roots robustly under adversarial path manipulation or indirect prompt guidance?
- How much protection does Streamable HTTP hardening add in realistic local deployment patterns, and where do configuration errors remain common?
- Can provenance-aware mediation reduce cross-server escalation meaningfully without rendering multi-server workflows impractical?
- How much operator burden do approval gates, elicitation restrictions, and trust upgrades impose in benign enterprise tasks?
- What is the smallest enforcement core that is both worth formalizing and stable enough to model-check against replay traces?

## 10. Conclusion
The current evidence base is already sufficient to motivate a more disciplined enterprise conversation about MCP security. The protocol should not be understood only as a convenience layer for tool access, nor only as a new site for prompt injection. Rather, it appears to create a delegated-authority environment in which model output, server metadata, authorization state, transport exposure, local boundaries, and cross-server trust interact in ways that can amplify familiar security failures. [SPEC] [CITED-PRELIM]

The most useful contribution of this first draft is therefore not a claim of finality, but a structured way to proceed responsibly. The paper identifies the security-relevant surfaces introduced or sharpened by the current specification, translates them into enterprise risk scenarios, proposes a layered control framework, and defines a validation program that clearly distinguishes what this repository can already say from what it still needs to test. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

If the project succeeds in the next phase, some of the proposed defense patterns may mature from design hypotheses into experimentally supported guidance. If it does not, the negative findings will still be valuable because they will narrow the gap between appealing architecture sketches and practically defensible enterprise deployments. Either way, the correct near-term stance is neither blanket rejection nor careless adoption. It is governed experimentation with explicit evidence boundaries. [HYPOTHESIS] [LAB-PLANNED]

## Preliminary references and source base
This first draft uses the project's current source base. The entries below are not yet formatted as final publication references; they are the working bibliography for the issue #6 draft.

Primary MCP and project sources:
- SPEC-2025 — Model Context Protocol Specification (2025-11-25).
- README — Project README for `poc/mcp-enterprise-security-survival-guide`.
- BRIEF — `design/PROJECT_BRIEF.md`.
- VALPLAN — `design/validation-and-poc-plan.md`.
- THREATMODEL — `design/threat-model.md`.
- CLAIMLEDGER — `research/claim-ledger.md`.

Distinct PDF or paper sources currently inventoried in `/home/sealjitha/toresearch`:
- S1 — Beyond the Protocol: Unveiling Attack Vectors in the Model Context Protocol (MCP) Ecosystem.
- S2 — Breaking the Protocol: Security Analysis of the Model Context Protocol Specification and Prompt Injection Vulnerabilities in Tool-Integrated LLM Agents.
- S3 — Enterprise-Grade Security for the Model Context Protocol (MCP): Frameworks and Mitigation Strategies.
- S4 — MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits.
- S5 — MCPGuard: Automatically Detecting Vulnerabilities in MCP Servers.
- S6 — MCPSecBench: A Systematic Security Benchmark and Playground for Testing Model Context Protocols.
- S7 — Securing the Model Context Protocol (MCP): Risks, Controls, and Governance.
- S9 — Systematic Analysis of MCP Security.
- S10 — Systematization of Knowledge: Security and Safety in the Model Context Protocol Ecosystem.
- S11 — Trivial Trojans: How Minimal MCP Servers Enable Cross-Tool Exfiltration of Sensitive Data.
- S12 — When MCP Servers Attack: Taxonomy, Feasibility, and Mitigation.

Note on references: source S7 was present twice in the research folder and is treated here as one distinct source. Final publication formatting, citation normalization, and any source-pruning pass should happen after closer reading and claim verification.