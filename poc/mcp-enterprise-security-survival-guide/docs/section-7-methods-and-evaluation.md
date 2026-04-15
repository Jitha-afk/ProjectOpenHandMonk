# 7. Experimental evaluation plan and evidence boundaries

This section defines the methods that will be used to test the paper's defensive claims and to bound what the current draft can honestly say now. The method is threat-model-driven, spec-aware, and explicitly falsifiable: each evaluable claim must map to a concrete attacker action, a reproducible fixture, measurable success criteria, and a failure condition that would weaken or disprove the claim. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

The current repository state supports a design-level evaluation plan, not empirical findings. What is already demonstrated in this draft is the security-relevant deployment surface, the enterprise threat model, the claim-status discipline, and the prioritization of candidate controls. What is not yet demonstrated is quantitative defense efficacy, false-positive trade-offs, operator burden, or machine-checked assurance for any implementation. Those stronger statements remain planned evaluation targets only. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

## 7.1 Method and current evidence posture

The evaluation method combines four layers. First, the latest MCP specification supplies the normative surfaces that matter for enterprise deployment: authorization, Streamable HTTP exposure, roots, elicitation, sampling-with-tools, and provenance/trust handling. Second, the threat model converts those surfaces into attacker goals, trust boundaries, and failure modes relevant to enterprise brokers, mixed-trust servers, and sensitive tools. Third, the attack corpus translates those failure modes into replayable fixtures. Fourth, a narrow formal core is reserved for the broker-side enforcement logic rather than for the entire MCP ecosystem. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

Current status is therefore deliberately split:
- Already established in-repo: reference threat assumptions, attack classes, validation workflow, and prioritized first-wave tracks. [SPEC] [CITED-PRELIM]
- Planned but not yet demonstrated: measured block rates, benign-task pass rates, latency overhead, approval burden, roots enforcement under attack, elicitation protection efficacy, transport-hardening efficacy, and formal proofs for the enforcement core. [HYPOTHESIS] [LAB-PLANNED]

## 7.2 Reference lab topology

The lab is intentionally minimal but representative of an enterprise MCP deployment. It centers on one host application or broker that receives model-generated tool intents and mediates execution through explicit policy decisions rather than prompt-only control. The broker connects to three server classes so that both single-server and cross-server failures can be exercised under the same harness. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

| Component | Role in evaluation | Trust posture | Security purpose |
|---|---|---|---|
| Host application / broker | Receives model tool intents and applies allow, deny, or approval-required decisions | High-trust control point | Main enforcement surface for policy, provenance, taint, and audit checks [HYPOTHESIS] [LAB-PLANNED] |
| Trusted internal MCP server | Exposes approved low-risk read tools and selected write-capable tools | High trust | Baseline for legitimate enterprise workflows [CITED-PRELIM] [LAB-PLANNED] |
| Semi-trusted external MCP server | Exposes useful but less governed tools/resources | Partial trust | Tests whether external utility can be preserved without implicit transitive trust [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED] |
| Adversarial or misconfigured MCP server | Supplies deceptive descriptions, unsafe outputs, or forged metadata | Low trust / attacker-controlled | Exercises prompt-channel abuse, provenance tampering, and cross-server escalation paths [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED] |
| Sensitive tool classes | File, network, shell, identity-bearing, and write-capable actions | High impact | Makes authorization correctness, roots, and trust transitions measurable [SPEC] [HYPOTHESIS] [LAB-PLANNED] |
| Approval, logging, and provenance layer | Records decisions and exposes trust lineage for review | High-trust support system | Measures auditability and prevents silent privilege transitions [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED] |

Deployment assumptions follow the existing design documents. Remote servers should use per-user scoped authorization where available, while local stdio servers may rely on environment-scoped credentials. Streamable HTTP is treated as an in-scope transport surface, including local cases where Origin validation and localhost binding matter. Clients may expose roots as filesystem boundary declarations. Servers may request elicitation and sampling, and sampling may itself create nested tool-use risk. These are method assumptions and evaluation targets, not completed implementation findings. [SPEC] [HYPOTHESIS] [LAB-PLANNED]

Task sets are also fixed in advance so that control costs can be compared against a common baseline: benign productivity tasks, security-sensitive tasks involving files/network/shell/identity, and multi-step workflows in which one server can influence follow-on tool use on another server. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

## 7.3 Attack corpus classes

The attack corpus is designed to cover the failure modes already identified in the threat model and claim ledger while preserving a benign baseline for false-positive measurement. The corpus classes are as follows. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

1. Unauthorized tool or server selection
   - Prompt-injection or model-error fixtures that attempt to invoke tools outside intended server, privilege, or task boundaries. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]
2. Tool-output injection and instruction/data confusion
   - Malicious outputs that try to redirect the broker or model into unsafe follow-on actions. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]
3. Cross-server trust propagation and confused-deputy escalation
   - Multi-hop cases in which a weaker server attempts to influence actions on a stronger server. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]
4. Provenance tampering and metadata forgery
   - Replay cases with stripped, replayed, malformed, or forged provenance and server metadata. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]
5. Roots and path-resolution boundary escape attempts
   - File-access fixtures that try to induce out-of-root reads or writes through path reshaping, aliasing, or indirect guidance. [SPEC] [HYPOTHESIS] [LAB-PLANNED]
6. Elicitation abuse and unsafe secret collection
   - Cases that blur normal user interaction with credential harvesting or unsafe consent flows. [SPEC] [HYPOTHESIS] [LAB-PLANNED]
7. Streamable HTTP exposure and origin-confusion cases
   - Transport fixtures that test local exposure assumptions, weak Origin checks, or unsafe binding decisions. [SPEC] [HYPOTHESIS] [LAB-PLANNED]
8. Benign baseline tasks
   - Non-adversarial workflows used to measure false denials, usability cost, and workflow breakage under the same controls. [CITED-PRELIM] [LAB-PLANNED]

Sampling-triggered tool-use chains are treated as a cross-cutting case inside the unauthorized-selection and cross-server classes, because the risk of nested delegation is that low-trust requests can indirectly reach high-impact tools unless the same policy and trust checks apply. [SPEC] [HYPOTHESIS] [LAB-PLANNED]

## 7.4 Metrics and scorecard

All tracks are evaluated with the same core scorecard so that defenses can be compared on both security benefit and operational cost. Quantitative thresholds in this section are provisional kickoff targets from the validation plan, not measured results. [HYPOTHESIS] [LAB-PLANNED]

| Metric | What it measures | Why it matters |
|---|---|---|
| Attack success rate | Fraction of adversarial fixtures that still achieve the intended unsafe effect | Primary measure of residual exposure [HYPOTHESIS] [LAB-PLANNED] |
| Defense block rate | Fraction of attack fixtures blocked, downgraded, quarantined, or surfaced for approval | Direct measure of control efficacy [HYPOTHESIS] [LAB-PLANNED] |
| Benign task success rate | Fraction of legitimate tasks that still complete | Prevents a security-only evaluation from hiding usability collapse [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED] |
| False-denial / false-positive rate | Benign workflows incorrectly blocked or burdened | Captures operational friction and over-restrictive policy behavior [HYPOTHESIS] [LAB-PLANNED] |
| Median latency overhead | Added decision or serialization cost per control | Distinguishes plausible enterprise controls from impractical ones [HYPOTHESIS] [LAB-PLANNED] |
| Human approval burden | Approvals required per task or per risky action | Measures whether a defense merely shifts cost to operators [HYPOTHESIS] [LAB-PLANNED] |
| Policy coverage | Percentage of attempted tool calls matched by explicit policy | Indicates whether the deployment is governed or partly implicit [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED] |
| Trust-lineage / audit completeness | Whether privileged actions have explainable provenance, trust tier, and decision logs | Required for incident reconstruction and for evaluating trust-aware controls [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED] |
| Replay determinism | Stability of outcomes across repeated runs | Needed for credible comparison and later regression testing [HYPOTHESIS] [LAB-PLANNED] |

## 7.5 First-wave validation tracks

The full candidate space is broader, but the first implementation wave is intentionally limited to the three tracks already prioritized in the validation plan: a policy enforcement gateway, a provenance and integrity envelope, and multi-server trust controls with taint tracking. This subset is chosen because it best matches the enterprise-control focus of the paper and provides a realistic path to a later formal model of broker enforcement and trust transitions. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

### Track 1: Policy enforcement gateway

This track tests whether an explicit broker-side policy layer can reduce unsafe tool or server selection without materially harming benign task completion. The gateway evaluates proposed calls against allowed servers, allowed tools, argument constraints, risk labels, and approval requirements. Provisional success targets are at least 95% blocking of unauthorized tool/server-selection fixtures, at least 90% benign-task completion, deterministic decision logging for all attempted calls, and less than 50 ms median decision latency in replay mode. These numbers are design thresholds only and do not yet constitute findings. [HYPOTHESIS] [LAB-PLANNED]

### Track 2: Provenance and integrity envelope

This track tests whether verifiable response metadata can reduce unsafe reliance on attacker-controlled outputs. Candidate envelope fields include server identity, tool identity, timestamp, request hash, response hash, and trust tier, with optional controlled-environment attestation. Provisional success targets are detection of all intentionally tampered replay fixtures, trusted-versus-untrusted origin distinction for all responses in logs, prevention of at least 90% of privileged follow-on actions triggered solely by untrusted output when policy requires trusted origin, and acceptable payload overhead. These remain planned measurements rather than demonstrated outcomes. [HYPOTHESIS] [LAB-PLANNED]

### Track 6: Multi-server trust controls and cross-server taint tracking

This track tests whether trust-aware routing and taint propagation can stop low-trust outputs from silently authorizing high-trust actions. Servers are assigned trust tiers, responses carry taint labels, and higher-trust actions require an explicit upgrade step such as independent verification or approval. Provisional success targets are blocking at least 90% of cross-server escalation fixtures, providing explainable trust lineage for all privileged actions in the trace set, and preserving at least 85% benign completion for multi-server workflows in the initial prototype. These are first-wave evaluation goals, not current results. [HYPOTHESIS] [LAB-PLANNED]

Roots enforcement, elicitation restrictions, and Streamable HTTP hardening remain first-wave claim targets at the fixture and scorecard level even though they are not separate first-wave build tracks. In practice, the first-wave corpus should include focused probes for out-of-root access, unsafe secret collection, and origin/binding failures so that later dedicated controls can be evaluated against already-versioned attack cases. [SPEC] [HYPOTHESIS] [LAB-PLANNED]

## 7.6 Formal-core validation approach

Formal work is intentionally scoped to a small enforcement core rather than to the full protocol, the model, or every server implementation. The purpose is not to claim mathematically proven safety for MCP as a whole, but to model-check the broker-side decision logic that is most security-critical and most amenable to precise specification. [HYPOTHESIS] [LAB-PLANNED]

The planned approach has three layers. [HYPOTHESIS] [LAB-PLANNED]

1. Formal model layer
   - Specify the broker policy and trust-state machine in a compact notation suitable for state exploration, such as TLA+ or Alloy. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]
2. Reference implementation layer
   - Build one small enforcement core whose inputs, outputs, and state transitions match the formal model closely enough to support traceability. [HYPOTHESIS] [LAB-PLANNED]
3. Conformance layer
   - Use replay traces and property-based tests to check that implementation behavior conforms to the modeled invariants under normal, adversarial, and malformed inputs. [HYPOTHESIS] [LAB-PLANNED]

The initial proof targets are narrow and practical: policy non-bypass for protected tool execution, trust monotonicity across servers and tainted outputs, roots or capability confinement for protected resources, and fail-closed handling when provenance is missing, malformed, or ambiguous. No machine-checked model has been produced yet, so the manuscript can describe this as a formal-core validation plan only. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

## 7.7 Evidence boundaries for this draft

The draft can already make some bounded claims, but only at the right evidence level. It cannot yet make lab-backed efficacy claims. [SPEC] [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]

| Claim type | This draft can say now | This draft cannot say yet |
|---|---|---|
| Specification facts | The latest MCP specification defines security-relevant surfaces such as authorization, Streamable HTTP guidance, roots, elicitation constraints, and sampling/tool interactions. [SPEC] | That these mechanisms are consistently implemented correctly or effective in production. [HYPOTHESIS] [LAB-PLANNED] |
| Preliminary literature observations | Multiple sources preliminarily indicate attack-surface expansion, malicious metadata/tool-description risk, and cross-server trust problems. [CITED-PRELIM] | Ecosystem-wide prevalence rates, benchmark-grade effect sizes, or settled consensus about defensive efficacy. [HYPOTHESIS] [LAB-PLANNED] |
| Enterprise control guidance | The paper may recommend bounded controls such as policy gateways, scoped authorization, provenance handling, trust tiering, and auditability as design guidance. [SPEC] [CITED-PRELIM] [HYPOTHESIS] | That any one of these controls already reduces risk by a measured amount in this repository. [HYPOTHESIS] [LAB-PLANNED] |
| Quantitative defense claims | The paper may publish provisional thresholds as evaluation targets and falsification criteria. [HYPOTHESIS] [LAB-PLANNED] | The paper cannot yet claim measured block rates, false-positive rates, latency numbers, or operator-burden reductions. [HYPOTHESIS] [LAB-PLANNED] |
| Formal assurance claims | The paper may describe a narrow formalization strategy for the broker core. [HYPOTHESIS] [LAB-PLANNED] | The paper cannot yet claim machine-checked proofs, verified conformance, or mathematically proven end-to-end MCP security. [HYPOTHESIS] [LAB-PLANNED] |

In short, this section contributes a reproducible evaluation design and an explicit evidence boundary, not experimental findings. That distinction is necessary if the manuscript is to remain useful to enterprise defenders without overstating what the repository has already demonstrated. [CITED-PRELIM] [HYPOTHESIS] [LAB-PLANNED]
