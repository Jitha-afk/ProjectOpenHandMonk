# Source inventory and gap analysis for issue #6

## Scope, method, and uncertainty

This memo is an initial intake artifact for the proposed Enterprise Security Survival Guide for the latest MCP specification.

What I inspected:
- All 12 PDFs currently present in `/home/sealjitha/toresearch`
- The repository-local project material under `poc/mcp-enterprise-security-survival-guide/`
- The public MCP specification at `https://modelcontextprotocol.io/specification/2025-11-25`, specifically the sections on authorization, transports, roots, sampling, elicitation, tools, resources, and prompts

What I could and could not verify:
- I was able to extract metadata and the first 1-2 pages from the PDFs using `pdfinfo` and `pdftotext`, which gave usable titles, abstracts, and opening sections for all files.
- I did not complete a full close reading of every page of every paper in this intake pass, so some source characterizations below are still probabilistic rather than definitive.
- Two files appear to be duplicate copies of the same paper: `Securing the Model Context Protocol (MCP)_ Risks, Controls, and Governance.pdf` and `Securing the Model Context Protocol (MCP)_ Risks, Controls, and Governance (1).pdf`.
- At intake time, there was no pre-existing repo-local MCP security research content in this project workspace beyond the template scaffold, so this memo is grounded mostly in the PDFs plus the latest public spec.

Interpretation note:
- Confidence levels below refer to confidence in my source characterization, not confidence that the paper's own claims are correct.

## Source inventory

| ID | PDF in `/home/sealjitha/toresearch` | Extraction basis | Likely focus | Confidence | Why it matters for enterprise MCP security |
|---|---|---|---|---|---|
| S1 | `Beyond the Protocol_ Unveiling Attack Vectors in the Model Context Protocol (MCP) Ecosystem.pdf` | Metadata + abstract/introduction | End-to-end attack-vector study across the MCP lifecycle, especially trust-boundary failures in registration, planning, and operation phases | Medium | Useful for modeling where enterprise controls should sit: server onboarding, tool-description sanitization, runtime response filtering, and cross-tool trust isolation |
| S2 | `Breaking the Protocol_ Security Analysis of the Model Context Protocol Specification and Prompt Injection Vulnerabilities in Tool-Integrated LLM Agents.pdf` | Metadata + abstract/introduction | Formal/security analysis of protocol-level weaknesses; highlights capability attestation gaps, sampling-origin/authentication issues, and trust propagation in multi-server settings; proposes `ATTEST MCP`-style remediation | Medium | Directly relevant to issue #6 because it suggests spec-level defenses that may be turned into enterprise architecture patterns or proof obligations |
| S3 | `Enterprise-Grade Security for the Model Context Protocol (MCP)_  Frameworks and Mitigation Strategies.pdf` | Title page + abstract/introduction | Enterprise security framework for MCP, with zero-trust, defense-in-depth, governance, and actionable mitigation patterns | Medium | Closest source to the project brief's enterprise angle; likely a baseline for translating attack literature into deployable controls |
| S4 | `MCP Safety Audit_ LLMs with the Model Context Protocol Allow Major  Security Exploits.pdf` | Title page + abstract/introduction | Broad exploit survey showing coercion of leading LLMs into harmful tool use; introduces an MCP server auditing tool (`McpSafetyScanner`) | Medium | Matters because enterprises need pre-deployment scanning and red-team style validation, not just taxonomies |
| S5 | `MCPGuard _ Automatically Detecting Vulnerabilities in MCP Servers.pdf` | Metadata + abstract/introduction | Automated vulnerability detection for MCP servers; frames threats as agent hijacking, web vulnerabilities, and supply-chain issues; surveys scanning/monitoring defenses | Medium | Important for turning enterprise guidance into automatable guardrails, CI checks, or registry admission controls |
| S6 | `MCPSecBench_ A Systematic Security Benchmark and Playground for Testing Model Context Protocols.pdf` | Metadata + abstract/introduction | Security benchmark and playground; formalizes secure MCP requirements, 17 attack types across client/protocol/server/host surfaces, and evaluates defenses on major platforms | Medium | Strong candidate foundation for measurable proof-of-concept evaluation and for selecting benchmark scenarios for this project |
| S7 | `Securing the Model Context Protocol (MCP)_ Risks, Controls, and Governance (1).pdf` | Metadata + abstract/introduction | Governance-oriented paper covering content injection, supply-chain attacks, agent overreach, scoped auth, provenance, sandboxing, DLP, anomaly detection, and private registries | Medium | Important because it connects MCP-specific issues to governance and compliance language that enterprises can operationalize |
| S8 | `Securing the Model Context Protocol (MCP)_ Risks, Controls, and Governance.pdf` | Metadata + abstract/introduction | Same as S7; appears to be a duplicate copy of the same paper in the research folder | Medium | Still worth noting because the duplicate confirms this paper is likely considered important source material for the issue |
| S9 | `Systematic Analysis of MCP Security.pdf` | Metadata + abstract/introduction | Attack-library paper (`MCPLIB`) with 31 attack methods: direct tool injection, indirect tool injection, malicious user attacks, and LLM-inherent attacks | Medium | Helps broaden the threat model beyond just malicious servers; useful for assembling an enterprise testing matrix and adversary taxonomy |
| S10 | `Systematization of Knowledge_ Security and Safety in the Model Context Protocol Ecosystem.pdf` | Metadata + abstract/introduction | SoK-style taxonomy distinguishing security threats from safety hazards; analyzes resources/prompts/tools; surveys defenses including cryptographic provenance and runtime intent verification | Medium | Likely the best umbrella source for organizing the eventual guide into threat classes, primitives, and defense families |
| S11 | `Trivial Trojans_ How Minimal MCP Servers Enable Cross-Tool Exfiltration of Sensitive Data.pdf` | Metadata + abstract/introduction | Low-barrier proof of concept showing simple malicious servers can exfiltrate sensitive data across otherwise benign tools | Medium | Important for enterprise readers because it reframes the risk: dangerous MCP attacks may not require advanced adversaries or complex malware |
| S12 | `When MCP Servers Attack_ Taxonomy, Feasibility, and Mitigation.pdf` | Metadata + abstract/introduction | Systematic study of malicious MCP servers as active threat actors; taxonomy of 12 categories; PoC server generation; tests current scanners and shows insufficiency | Medium | Highly relevant to enterprise procurement, server vetting, private registry design, and detection-evasion concerns |

## What the current literature already seems to cover well

Across the papers, the following themes recur often enough in this preliminary intake to treat them as likely already-covered research territory rather than novel project contributions:

1. MCP expands the attack surface beyond classic prompt injection.
   - The literature repeatedly treats MCP risk as multi-surface: client, protocol, server, host, and supply chain.
   - This means the guide should not frame MCP security as just another prompt-injection problem.

2. Malicious server metadata is a first-class attack vector.
   - Tool descriptions, prompts, and resources are repeatedly described as instruction-carrying channels.
   - Registration and planning are treated as exploitable stages, not harmless setup phases.

3. Cross-server trust propagation is central.
   - Several papers argue that even if each individual server looks benign, composition effects can create unexpected exfiltration or privilege-escalation paths.
   - This is particularly relevant to enterprises that mix internal tools with third-party servers.

4. Benchmarking and PoC-driven evaluation already exist.
   - `MCPSecBench`, `MCPLIB`, `McpSafetyScanner`, and `MCPGuard` suggest the literature is already moving toward repeatable evaluation rather than purely conceptual warning.
   - That is good news for issue #6 because it means the project can anchor its claims in measurable experiments.

5. Existing defenses are discussed, but often at a high level.
   - Common recommendations include least privilege, scoped auth, sandboxing, provenance, private registries, DLP, anomaly detection, and human approval.
   - However, the literature often stops short of specifying exactly how enterprises should implement these controls for the latest spec features.

6. Formalization is emerging but not mature.
   - A few sources attempt secure-MCP definitions or protocol-level remediation ideas, but the space still looks early.
   - There is room for stronger proofs, invariants, or mechanically-checkable policy models.

## Gap analysis for the latest MCP spec and for enterprise deployment

The strongest apparent gap is not basic threat discovery. The strongest gap is the translation from known MCP threats into deployable, spec-aware enterprise controls for the `2025-11-25` protocol surface.

### A. The newest spec features do not appear fully covered by the current papers

From the latest spec sections I inspected, several security-relevant capabilities now need targeted treatment:
- HTTP authorization based on OAuth 2.1-related flows, protected resource metadata, and optional dynamic client registration
- Streamable HTTP replacing the older HTTP+SSE model
- Explicit DNS rebinding guidance via `Origin` validation and localhost binding recommendations
- Client `roots` as filesystem boundary declarations
- `sampling/createMessage` with tool-use support and soft-deprecated cross-server context inclusion
- `elicitation/create` with separate form and URL modes, and explicit prohibition on using form mode for secrets
- Server-side tools/resources/prompts plus change-notification flows

What seems missing in the papers I inspected:
1. A dedicated evaluation of the `2025-11-25` authorization model in enterprise identity environments
   - I did not see clear evidence yet of comparative testing against real enterprise IdPs, token lifetimes, scope design, service accounts vs per-user auth, or failure modes in metadata discovery.

2. A focused treatment of Streamable HTTP security migration
   - The spec now makes `Origin` checking and local bind behavior explicit, but I did not see literature centered on deployment mistakes introduced during migration from older SSE-style patterns.

3. A systematic study of elicitation security
   - The latest spec clearly separates form vs URL mode and says secrets must not be collected through form mode. This looks important, but I have not yet seen a mature literature cluster around measuring violations, UX bypasses, or secret-harvesting prevention quality.

4. A systematic study of `roots` as a confinement primitive
   - The spec positions roots as filesystem boundaries, but the literature I reviewed seems far more focused on malicious tools and prompt injection than on proving or stress-testing root confinement guarantees.

5. A systematic study of sampling-with-tools as a nested trust channel
   - The latest spec lets servers request model sampling and optionally enable tool use inside that flow. That creates a nested delegation problem that feels underexplored relative to the severity of the risk.

### B. Enterprise defense techniques are discussed, but not yet operationalized deeply enough

The literature points at many controls, but several enterprise-grade implementation gaps remain:

1. Reference architecture gap
   - There is still room for a concrete enterprise MCP security architecture showing how registry, gateway, policy engine, sandbox, token broker, approval UI, and telemetry pipeline should fit together.
   - This is especially useful for issue #6 because practitioners need deployable blueprints, not just lists of controls.

2. Control-to-threat traceability gap
   - Many papers enumerate attacks and many papers enumerate controls, but fewer appear to map each latest-spec feature to a minimal set of effective defenses and measurable acceptance tests.

3. Multi-tenant identity and authorization gap
   - Enterprises need guidance on per-user tokens, delegated scopes, just-in-time approval, revocation, break-glass behavior, and separation between user identity and agent identity.
   - That is more specific than generic advice to "use OAuth" or "apply least privilege."

4. Registry and software supply-chain gap
   - The literature recognizes malicious servers, but there is still a gap around signed manifests, capability attestations, provenance records, admission policies, and private-registry workflows that enterprises can actually enforce.

5. Audit and compliance gap
   - There is little obvious consensus yet on what a minimally sufficient MCP audit log must include across prompts, resources, tools, sampling, elicitation, auth events, and policy decisions.
   - That matters for SOC 2, ISO 27001, incident response, and internal auditability.

6. Deployment-hardening gap for local stdio servers
   - The latest spec says stdio should generally retrieve credentials from the environment rather than use the HTTP auth flow. That means local process hardening, env-secret scoping, subprocess isolation, and workstation hygiene may be more important than the current literature emphasizes.

### C. Formal and provable security still looks underdeveloped

Because the issue specifically asks for grounded information, mathematically provable code, and proofs of concept, the following gaps look especially promising:

1. Capability-verification gap
   - MCP servers describe what they can do, but the literature still appears to lack a mature, practical mechanism to prove that declared capabilities match observed behavior.

2. Noninterference / taint-propagation gap
   - There is no obvious standard proof story yet for showing that low-trust server content cannot cause high-impact actions without explicit approval or policy transition.

3. Confinement-proof gap for roots and tool scopes
   - The spec introduces boundaries, but stronger formal statements are still needed, e.g., "a compliant client plus policy layer cannot read outside approved roots" or "a low-trust tool cannot transitively trigger a high-trust action without mediation."

4. Policy-soundness gap
   - Enterprises need policies that are explainable, enforceable, and machine-checkable. The literature still appears to be earlier on examples than on proof-oriented policy design.

### D. Human factors and measurable trade-offs are still thin

What also seems missing:
- Good data on approval fatigue for human-in-the-loop MCP actions
- Clear UX patterns for explaining server identity, provenance, and trust level to end users
- Performance/latency/usability costs of defenses such as proxy mediation, sandboxing, provenance tagging, or attestation checks
- Empirical comparisons of "secure enough" enterprise defaults versus maximally locked-down defaults

## Concrete research questions for this project

1. Which `2025-11-25` MCP features create the largest net-new enterprise risk delta relative to earlier MCP versions: Streamable HTTP, authorization, elicitation, roots, or sampling-with-tools?

2. Can an enterprise MCP gateway that enforces per-user authorization, server allowlists, provenance labels, and policy checks materially reduce unauthorized tool calls and data exfiltration without breaking compliant clients and servers?

3. Can signed server manifests or capability attestation detect mismatches between declared MCP capabilities and runtime-observed behavior with acceptable operational overhead?

4. How effective are `roots` plus client-side policy enforcement at preventing file access outside approved boundaries under indirect prompt injection and malicious server guidance?

5. Does forcing secret collection into URL-mode elicitation, combined with client-side secret detection and domain disclosure, significantly reduce credential-harvesting success compared with weaker client implementations?

6. Can provenance-aware taint tracking across prompts, resources, tool outputs, and sampling requests block cross-server exfiltration chains while preserving useful interoperability?

7. What formal invariant or proof obligation is both realistic and valuable for enterprise MCP security: capability authenticity, confinement of file access, noninterference across trust zones, or mandatory mediation of high-impact actions?

8. What minimum audit schema should an enterprise retain to reconstruct MCP incidents end-to-end across auth, server discovery, prompt/resource exposure, tool execution, sampling, elicitation, and policy decisions?

## Recommended first-wave claims to validate

Only claims that look testable should enter the first wave.

1. Enforcing `Origin` validation and localhost-only binding for local Streamable HTTP MCP servers blocks known DNS-rebinding-style interaction paths that succeed against weaker defaults.

2. Per-user scoped authorization for remote MCP servers reduces the blast radius of malicious tool use compared with shared static credentials.

3. Client-side enforcement of `roots` boundaries prevents file reads outside approved `file://` roots even when a malicious server attempts indirect prompt injection.

4. Restricting sensitive data collection to URL-mode elicitation, plus explicit domain disclosure and user consent, lowers credential-exfiltration success relative to form-mode handling.

5. Provenance labels and policy rules that prevent low-trust server output from directly triggering high-impact tools reduce cross-server exfiltration success rates.

6. Private registry allowlisting plus signed server metadata reduces successful onboarding of malicious MCP servers compared with unaudited installation flows.

7. Capability attestation or manifest hashing can detect at least some classes of server-description/runtime-behavior mismatch with tolerable latency overhead.

## Bottom line

The current corpus is already rich in threat taxonomies, PoCs, and early defense ideas. The biggest opportunity for issue #6 is not to rediscover that MCP is risky. It is to produce a spec-aware, enterprise-deployable, and preferably partially provable defense guide for the `2025-11-25` MCP surface, especially around authorization, Streamable HTTP, roots, elicitation, sampling-with-tools, provenance, and private-registry control planes.
