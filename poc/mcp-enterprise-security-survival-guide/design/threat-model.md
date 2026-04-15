# Threat Model — MCP Enterprise Security Survival Guide

## Purpose and scope
This artifact defines a concise enterprise threat model for MCP deployments scoped to the project inputs for issue #6. It is intended to support the manuscript, the validation plan, and later formalization work. The emphasis is the latest-spec risk surface called out in the project materials: authorization, Streamable HTTP, roots, elicitation, sampling-with-tools, and provenance/trust.

## 1. System model and deployment assumptions
Reference deployment assumed by this project:
- A host application or broker receives model-generated tool intents and mediates execution.
- The broker connects to multiple MCP servers: one trusted internal server, one semi-trusted external server, and one adversarial or misconfigured server used for validation.
- Sensitive enterprise tools may include file, network, shell, identity-bearing, and write-capable operations.
- A policy layer sits between model intent and tool execution and can allow, deny, or require approval.
- Remote MCP servers use per-user authorization where possible; local stdio servers may instead rely on environment-scoped credentials.
- Streamable HTTP is an in-scope transport surface, including local deployments where Origin validation and localhost binding matter.
- Clients may expose roots as filesystem boundary declarations.
- Servers may request elicitation and sampling; sampling may optionally include tool use and therefore creates nested delegation risk.
- Provenance, trust tiering, logging, and approval UX are treated as enterprise control points rather than optional add-ons.

Assumptions:
- Enterprises mix internal and third-party servers, so cross-server trust propagation is a primary risk.
- Malicious behavior may come from server metadata, tool descriptions, tool outputs, compromised clients, or adversarial users; not only from explicit malware.
- The project does not assume protocol-wide formal security proofs. It assumes a narrow, implementation-adjacent enforcement core can be validated and partially formalized.
- Availability matters, but confidentiality, integrity, authorization correctness, bounded autonomy, and auditability are the dominant security goals.

## 2. Assets, actors, and trust boundaries
### Assets
- User identity, tokens, and delegated authorization scopes
- Enterprise data exposed through tools, resources, prompts, or retrieved context
- Tool invocation rights, especially write, execute, network, and identity-bearing actions
- Files reachable through roots or local execution context
- Provenance records, trust labels, policy decisions, and audit logs
- Server metadata, capability declarations, and registry/admission state

### Actors
- End user requesting legitimate work
- Host application / MCP broker
- Model component generating tool intents
- Trusted internal MCP server
- Semi-trusted external MCP server
- Malicious or compromised MCP server
- Adversarial user attempting prompt or workflow abuse
- Enterprise identity provider, registry, logging, and approval systems

### Trust boundaries
1. User ↔ host application: user intent can be mixed with adversarial prompt content.
2. Model ↔ policy gateway: model output is not itself an authorization decision.
3. Broker ↔ MCP server: server metadata and outputs may be attacker-controlled.
4. Trusted server ↔ semi-trusted or external server: cross-server influence must not imply transitive trust.
5. MCP layer ↔ enterprise tools and data stores: side effects become real at this boundary.
6. Local workstation / stdio environment ↔ remote authorization domain: credential handling differs by transport and deployment mode.
7. Approval / logging / provenance systems ↔ execution path: if these are bypassed, the deployment becomes non-auditable and hard to contain.

## 3. Threat surfaces by latest-spec area
### Authorization
Main risk: shared static credentials, over-broad scopes, token mix-up, or weak mediation can let malicious or confused workflows execute actions beyond user intent.
Security objective: bind remote tool execution to per-user, least-privilege authorization and make the broker enforce policy before execution.

### Streamable HTTP
Main risk: transport migration and local deployment mistakes can expose MCP servers to DNS rebinding, origin confusion, or unintended network reachability.
Security objective: require strict Origin validation, safe binding defaults, and explicit exposure decisions for local and remote servers.

### Roots
Main risk: roots are boundary declarations only if the client and policy layer actually enforce them under adversarial prompting and tool guidance.
Security objective: prevent file reads/writes outside approved roots even when the model or a server tries to widen scope indirectly.

### Elicitation
Main risk: elicitation can become a credential-harvesting or consent-bypass channel, especially if secret collection is blurred with normal forms.
Security objective: keep secret collection out of unsafe modes, disclose destination/domain, and require explicit user consent for sensitive inputs.

### Sampling-with-tools
Main risk: nested delegation lets a server ask for model sampling and optionally tool use, creating a second-order path from low-trust input to high-impact action.
Security objective: treat sampling requests as policy-relevant execution requests, not as harmless generation.

### Provenance and trust
Main risk: downstream components cannot distinguish trusted observations from attacker-controlled output, enabling confused-deputy, cross-server escalation, and malicious onboarding.
Security objective: attach verifiable provenance, trust tiers, and admission controls so low-trust content cannot silently trigger high-trust actions.

## 4. Attack-control matrix
| Threat | Preconditions | Affected component | Control idea | Validation status | Priority |
|---|---|---|---|---|---|
| Shared or static credentials enable broad compromise | Remote server uses non-user-bound credentials; tool scopes are broad | Authorization layer, broker, remote MCP server | Prefer per-user scoped authorization, short-lived tokens, explicit scope design, deterministic decision logs | ANALOGICAL + SPEC-GROUNDED; recommended first-wave claim | High |
| Token or identity mix-up causes confused-deputy execution | User identity, agent identity, and server identity are not cleanly separated | Broker, IdP integration, approval path | Bind execution to user/server/scope tuple; log every auth and policy decision | ANALOGICAL + SPEC-GROUNDED; not yet lab-validated | High |
| DNS rebinding or origin confusion reaches a local Streamable HTTP server | Local server is reachable beyond intended boundary and Origin checks are weak | Streamable HTTP transport, local server endpoint | Localhost-only binding where possible; strict Origin validation; explicit remote exposure policy | SPEC-GROUNDED + HYPOTHESIS; validation planned | High |
| Migration mistakes expose Streamable HTTP endpoints to unintended clients | Legacy assumptions from older HTTP+SSE patterns persist | Transport layer, deployment configuration | Safe defaults, transport-specific hardening checklist, deny-by-default exposure | SPEC-GROUNDED + HYPOTHESIS | High |
| Malicious server induces file access outside approved roots | Client exposes roots but does not enforce them under adversarial guidance | Client, broker, filesystem tools | Client-side roots enforcement, argument validation, deny on out-of-root resolution | SPEC-GROUNDED + HYPOTHESIS; recommended first-wave claim | High |
| Path reshaping or aliasing bypasses roots intent | Relative paths, symlinks, or wildcard patterns are not normalized before policy | Client, policy engine, file tools | Canonicalize path targets before authorization; fail closed on ambiguity | HYPOTHESIS; should be tested in replay fixtures | High |
| Elicitation form flow is abused to collect credentials or secrets | Sensitive input is requested without strong disclosure or mode restriction | Client UX, elicitation handler | Restrict secret collection to safer flow, disclose destination/domain, require explicit consent | SPEC-GROUNDED + HYPOTHESIS; recommended first-wave claim | High |
| Deceptive elicitation gains approval fatigue or consent confusion | User sees frequent or poorly explained prompts | Approval UX, elicitation layer | Risk-based prompting, clearer trust labels, low-volume approval gates for high-risk requests | HYPOTHESIS; human-factors gap noted | Medium |
| Sampling request with tool use becomes an unmediated second-order execution path | Server can trigger sampling and optional tool use without equivalent policy checks | Sampling handler, broker, tool router | Apply same policy gateway and trust rules to sampling-triggered actions as normal tool calls | SPEC-GROUNDED + HYPOTHESIS | High |
| Low-trust server output directly triggers high-trust server action | Cross-server workflows lack taint or trust lineage | Broker, multi-server routing, high-trust tools | Trust tiers, taint propagation, upgrade/approval step before privileged follow-on actions | TITLE/ABSTRACT-ONLY + HYPOTHESIS; POC Track 6 planned | High |
| Provenance stripping or forgery makes malicious output appear trusted | Response metadata is missing, altered, replayed, or not consumed by policy | Provenance envelope, downstream policy, logs | Integrity envelope with server/tool identity, request/response hash, trust tier, reject or downgrade missing metadata | HYPOTHESIS; POC Track 2 planned | High |
| Malicious server onboarding through weak registry/admission process | Public installation or metadata review is unaudited | Registry, admission control, server onboarding | Private allowlist, signed metadata/manifests, capability review before enablement | ANALOGICAL + TITLE/ABSTRACT-ONLY; not yet lab-validated | Medium |
| Tool descriptions or metadata coerce unsafe invocation | Server metadata is treated as trustworthy planning guidance | Model-planning path, broker, tool router | Treat server metadata as untrusted input; sanitize, constrain with policy, require explicit allowlists | TITLE/ABSTRACT-ONLY + HYPOTHESIS | High |
| Missing audit schema prevents incident reconstruction | Auth, sampling, elicitation, policy, and execution events are logged inconsistently | Logging pipeline, incident response, compliance controls | Minimum unified audit schema spanning auth, discovery, prompts/resources, tools, sampling, elicitation, policy decisions | ANALOGICAL + SPEC-GROUNDED | Medium |

## 5. Four realistic invariants for formalization
1. Policy non-bypass
   - No tool execution occurs unless there is a corresponding allow decision from the broker policy state machine.

2. Roots confinement
   - For protected file operations, the canonical target path must remain within an approved root; otherwise execution is denied.

3. Trust monotonicity across servers
   - Low-trust or tainted data cannot directly authorize a higher-trust action without an explicit upgrade step such as independent verification or human approval.

4. Fail-closed handling for protected flows
   - Missing or malformed provenance, ambiguous path resolution, or unsafe secret-collection mode on a protected path yields deny, quarantine, or approval-required outcomes rather than silent execution.

## 6. Prioritized takeaways for the manuscript
- The dominant enterprise risk is not a single bug class; it is unsafe trust propagation across model output, server metadata, transport exposure, delegated authorization, and multi-server workflows.
- The minimum credible control stack is a policy gateway, per-user scoped authorization for remote servers, Streamable HTTP hardening, roots enforcement, provenance/trust labeling, and auditable approval for sensitive actions.
- The most useful near-term validation targets remain the project’s first-wave claims: Origin/binding hardening, per-user auth, roots enforcement, elicitation restrictions, provenance-aware policy, and private-registry controls.
- Formal work should stay narrow and focus on the broker’s enforcement core rather than attempting to prove the whole MCP ecosystem secure.
