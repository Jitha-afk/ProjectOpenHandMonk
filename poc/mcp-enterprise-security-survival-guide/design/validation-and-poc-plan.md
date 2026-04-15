# MCP Enterprise Security Survival Guide: Validation and POC Plan

## Purpose
This document turns issue #6 from a broad research request into a concrete validation program. The output of the project should not be a list of security opinions; it should be a set of testable claims, reproducible attack cases, small defense prototypes, and a narrow set of formally specified security properties for the most security-critical control points in an MCP deployment.

## Validation standard
A research claim is only considered validated in this repo when it is backed by all of the following:

1. A clearly stated threat model.
2. A falsifiable hypothesis about a defense.
3. A reproducible test harness or corpus that exercises the threat.
4. Measurable success criteria with thresholds.
5. A recorded failure condition showing what would disprove or weaken the claim.

Claims that cannot be converted into this structure should be labeled as guidance or design rationale, not evidence-backed conclusions.

## Claim-to-artifact workflow
For each major claim in the survival guide, use this pipeline:

1. Extract the claim
   - Example: "Per-tool policy gating reduces dangerous cross-domain tool execution."
2. Define the attacker action
   - Example: a prompt injection causes the model to invoke a high-risk tool without user intent.
3. Define the system boundary
   - Host application, MCP client, MCP broker/router, one or more MCP servers, tool implementations, and result rendering layer.
4. Create a minimal adversarial fixture
   - Example: crafted tool descriptions, malicious tool outputs, deceptive server metadata, or forged provenance fields.
5. Build a measurable defense artifact
   - Policy engine, trust scoring module, integrity wrapper, isolation layer, response normalizer, or multi-server trust broker.
6. Evaluate under both positive and negative cases
   - Positive: legitimate workflows still succeed.
   - Negative: attack cases are blocked, downgraded, sandboxed, or surfaced for approval.
7. Record falsification conditions
   - Example: the defense blocks less than 95% of attack fixtures, or introduces more than 10% false denials on benign workflows.

## Required validation assets
The project should eventually produce these artifact classes:

- Attack corpus
  - Prompt injection cases aimed at tool invocation.
  - Tool output injection cases aimed at follow-on actions.
  - Confused-deputy and cross-server escalation cases.
  - Metadata tampering and provenance forgery cases.
  - Benign baseline tasks for false-positive measurement.

- Execution harness
  - Deterministic replay of MCP requests/responses.
  - Synthetic multi-server scenarios with trusted and untrusted servers.
  - Structured logs capturing tool requests, policy decisions, risk scores, provenance state, and normalization output.

- Evaluation metrics
  - Attack success rate.
  - Defense block rate.
  - False-positive / false-denial rate on benign tasks.
  - Latency overhead per control.
  - Human approval burden where applicable.
  - Policy coverage: percentage of tool calls matched by explicit policy.

- Formal artifacts for the critical core
  - Small formal spec of the policy decision state machine and trust transitions.
  - Machine-checkable invariants for non-bypass properties.
  - Traceability from spec properties to implementation tests.

## Baseline experimental setup
Use a simple but representative MCP topology:

- One host application or broker that receives model tool intents.
- Three server classes:
  - Trusted internal server: low-risk read tools and approved write tools.
  - Semi-trusted external server: useful but not fully governed.
  - Adversarial or misconfigured server: deceptive descriptions, unsafe outputs, or forged metadata.
- Task sets:
  - Benign productivity tasks.
  - Security-sensitive tasks involving files, shell, network, or identity-bearing tools.
  - Multi-step workflows where one server can influence follow-on tool use.

This setup allows testing of both single-tool and multi-hop failure modes.

## POC tracks

The six tracks below are the full candidate space for this project, not the first implementation wave.

Recommended first-wave implementation subset for this repo:
1. Track 1: Policy enforcement gateway
2. Track 2: Provenance and integrity envelope
3. Track 6: Multi-server trust controls and cross-server taint tracking

These three are prioritized because they align most directly with the issue's enterprise focus, are testable with replay-style fixtures, and create a credible path toward a later narrow formal model of enforcement and trust transitions. Tracks 3-5 should remain in scope as follow-on work unless the first wave proves too narrow or infeasible.

Threshold note:
All quantitative thresholds below are provisional kickoff targets for experiment design, not validated expectations. They should be tightened, relaxed, or replaced once the baseline corpus and benign-task set are defined empirically.

### Track 1: Policy enforcement gateway
Threat addressed
- Prompt injection or model error causes invocation of tools outside user intent, outside least privilege, or outside approved server boundaries.

Hypothesis
- A policy gateway placed between model intent and MCP tool execution can reduce unsafe tool invocations without materially harming benign task completion.

Candidate implementation shape
- A broker-side decision function that evaluates each proposed tool call against:
  - allowed server list,
  - allowed tool list,
  - argument constraints,
  - required approval level,
  - task context labels such as read-only, write, networked, secret-bearing, or identity-impacting.
- Deny, allow, or require confirmation before execution.
- Policy rules should be explicit and machine-readable rather than hidden in prompts.

Measurable success criteria
- Blocks at least 95% of attack fixtures involving unauthorized tool/server selection.
- Allows at least 90% of benign tasks in the baseline set without manual override.
- Provides deterministic policy decision logs for 100% of attempted tool calls.
- Adds less than 50 ms median decision latency in replay mode.

Falsification
- Attack block rate stays below 95% after policy tuning.
- False denials exceed 10% on benign tasks.
- Equivalent attacks bypass the gateway through argument reshaping, aliasing, or tool-description manipulation.

### Track 2: Provenance and integrity envelope
Threat addressed
- Untrusted MCP servers forge, omit, or blur the source of tool outputs; downstream components cannot distinguish trustworthy observations from attacker-controlled content.

Hypothesis
- Attaching verifiable provenance metadata and integrity checks to tool responses will reduce unsafe trust in attacker-controlled outputs and enable policy decisions based on source trust.

Candidate implementation shape
- A response envelope containing:
  - server identity,
  - tool identity,
  - timestamp,
  - request hash,
  - response hash,
  - trust tier,
  - optional signature or keyed attestation for controlled environments.
- Downstream components reject or downgrade responses missing required provenance fields.
- Replay harness includes tampered, replayed, and metadata-stripped responses.

Measurable success criteria
- Detects 100% of intentionally tampered replay fixtures.
- Distinguishes trusted vs untrusted origin for 100% of responses in test harness logs.
- Prevents at least 90% of follow-on privileged actions triggered solely by untrusted output when provenance policy requires trusted origin.
- Overhead remains acceptable, for example less than 10% increase in serialized payload size in the reference prototype.

Falsification
- A forged or stripped provenance record is accepted as trusted.
- Downstream policy cannot actually consume the provenance data to alter execution outcomes.
- Integrity metadata exists but does not change attack success rate in follow-on workflows.

### Track 3: Tool-risk scoring and execution budgeting
Threat addressed
- All tools are treated as equivalent, so high-risk actions such as shell, network, filesystem writes, or identity-bearing operations are executed with the same friction as safe read operations.

Hypothesis
- A simple, explainable risk-scoring layer can meaningfully reduce dangerous tool execution by requiring stronger controls for higher-risk tools and argument patterns.

Candidate implementation shape
- Score each tool call using features such as:
  - capability class: read, write, execute, network, secret access,
  - external side effects,
  - scope breadth,
  - irreversible action potential,
  - argument risk markers such as wildcard paths, external URLs, or shell metacharacters,
  - provenance and trust tier of prior steps in the chain.
- Map score bands to actions: allow, allow with logging, require confirmation, require trusted provenance, or deny.

Measurable success criteria
- High-risk attack scenarios see at least 80% reduction in successful execution relative to a no-scoring baseline.
- Benign low-risk tasks preserve at least 95% completion.
- Score explanations are generated for 100% of calls and are stable across replay.
- Review burden for human approvals stays below a predefined threshold on benign task sets, for example fewer than 0.2 approvals per benign task on average.

Falsification
- Risk score has weak separation between benign and malicious cases.
- Most unsafe calls still fall into low or medium bands.
- Human approval burden becomes operationally impractical.

### Track 4: Capability isolation and constrained execution
Threat addressed
- Compromise or misuse of one server/tool grants broad host capabilities, enabling lateral movement or destructive side effects.

Hypothesis
- Narrow execution sandboxes and per-tool capability isolation reduce blast radius even when invocation controls fail.

Candidate implementation shape
- Run selected high-risk tools in constrained environments with minimal filesystem, network, process, and secret access.
- Associate each tool with an explicit capability manifest.
- Enforce separate sandboxes for read-only tools, write tools, and execution/network tools.
- Use tests that simulate compromise of a tool implementation and attempt disallowed actions.

Measurable success criteria
- 100% of sandbox escape test fixtures fail within the prototype threat model.
- High-risk tools cannot access undeclared files, network destinations, or secrets in any isolation test.
- Benign tasks that stay within declared capabilities succeed at least 90% of the time.
- All sandbox denials are observable in audit logs.

Falsification
- Any fixture performs a disallowed action outside its declared capability set.
- Capability manifests are too coarse to preserve benign task usefulness.
- Isolation only protects direct calls but not helper subprocesses or inherited environment state.

### Track 5: Response normalization and instruction/data separation
Threat addressed
- Tool outputs contain attacker-controlled text that is reinterpreted by the model as fresh instructions, causing tool-output prompt injection and confused-deputy behavior.

Hypothesis
- Normalizing tool responses into typed data structures and separating executable instructions from untrusted content will reduce follow-on exploitation from malicious tool output.

Candidate implementation shape
- Parse tool responses into explicit schemas where possible.
- Attach trust labels to fields.
- Strip or quarantine instruction-like content from untrusted outputs before it is fed back into the model or routing logic.
- Provide a safe rendering mode for textual outputs that marks them as untrusted data.
- Test with malicious outputs that attempt to redirect the model to invoke new tools or exfiltrate secrets.

Measurable success criteria
- At least 90% of tool-output injection fixtures fail to trigger unauthorized follow-on actions.
- Schema-valid benign outputs retain at least 95% task utility.
- Untrusted text fields are tagged or quarantined in 100% of replay logs.
- Normalization failures are explicit and fail closed for high-risk workflows.

Falsification
- Malicious textual output still causes unauthorized tool execution after normalization.
- Normalization silently drops critical benign information too often.
- The system falls back to raw text in security-sensitive paths.

### Track 6: Multi-server trust controls and cross-server taint tracking
Threat addressed
- A weakly trusted server influences decisions involving a strongly trusted server, enabling cross-server privilege escalation or confused-deputy attacks.

Hypothesis
- Cross-server taint tracking plus trust-aware routing can prevent low-trust outputs from silently authorizing high-trust actions.

Candidate implementation shape
- Assign each server a trust tier and each response a taint label.
- Propagate taint through the workflow graph.
- Require trust upgrades, independent verification, or human approval before tainted data can trigger privileged actions on higher-trust servers.
- Add replay scenarios where one server recommends another tool action, supplies arguments, or claims identity/context that should not be trusted.

Measurable success criteria
- Blocks at least 90% of cross-server escalation fixtures.
- All privileged actions in test traces have explainable trust lineage.
- Benign multi-server workflows still complete at least 85% of the time with the initial prototype.
- Taint propagation is deterministic across replay runs.

Falsification
- Low-trust server output can still directly trigger privileged high-trust actions.
- Taint tracking is inconsistent or can be stripped during format conversions.
- Benign multi-server workflows become unusably fragile.

## Cross-track evaluation methodology
Each track should be evaluated with the same four test classes:

1. Unit-level control tests
   - Does the specific mechanism behave correctly on direct inputs?
2. Adversarial fixture tests
   - Does the mechanism stop known attack patterns?
3. End-to-end workflow tests
   - Does the mechanism change real execution outcomes in multi-step tasks?
4. Regression replay tests
   - Are results stable across code changes and policy updates?

Suggested scorecard per track:

- Threat coverage
- Attack block rate
- Benign task success rate
- False-positive rate
- Median latency overhead
- Auditability / explanation completeness
- Spec-to-test trace coverage for any formalized properties

## What "mathematically provable code" should mean here
It should not mean claiming that the entire MCP ecosystem, model behavior, or enterprise deployment is formally proven secure. That would be unrealistic and misleading.

A realistic meaning in this repo is:

1. Formally specify a small security-critical core
   - Example: the policy decision state machine, trust-tier transition rules, taint propagation rules, and non-bypass conditions for privileged tool execution.

2. Prove or model-check specific safety properties
   - Examples:
     - No privileged tool executes unless policy returns allow.
     - Untrusted or tainted outputs cannot directly authorize a higher-trust action without an explicit upgrade step.
     - Denied capabilities are never reachable from a tool with a smaller capability manifest.

3. Keep the proof surface small and implementation-adjacent
   - The smaller the trusted core, the more credible the proof effort.
   - Prefer proving the control logic around tool execution rather than the model, whole app, or every server.

4. Back formal properties with executable checks
   - Property-based tests, trace validation, and conformance tests should exercise the implementation against the formal model.

### Practical recommendation for this repo
Use a two-layer approach:

- Formal layer
  - Create a compact formal spec for the broker policy and trust state machine using a tool suitable for state exploration, such as TLA+ or Alloy.
  - Focus on invariants and forbidden states, not full protocol verification.

- Implementation layer
  - Build one small reference enforcement core whose inputs and outputs match the formal model.
  - Add property-based tests that generate random call sequences, provenance states, and trust transitions to check implementation conformance.

Recommended proof targets for first implementation
- Policy non-bypass: every executed call must have a corresponding allow decision.
- Trust monotonicity: low-trust or tainted data cannot silently gain high-trust status.
- Capability containment: tool executions cannot exceed declared capability manifests.
- Fail-closed behavior: malformed provenance or normalization failures on protected paths produce deny/quarantine outcomes.

What does not count as mathematically provable in this project
- Prompt instructions claiming the model will behave safely.
- Static analysis reports without stated invariants.
- Unit tests alone.
- Informal reasoning that is not machine-checkable.

## Minimal future directory/file plan
This is the minimum structure needed to implement and validate the plan while keeping the formal and empirical work traceable inside this project folder.

```text
poc/mcp-enterprise-security-survival-guide/
├── design/
│   ├── validation-and-poc-plan.md
│   ├── threat-model.md
│   └── formal-properties.md
├── research/
│   ├── claim-inventory.md
│   └── attack-taxonomy.md
├── src/
│   ├── broker/
│   │   ├── policy-engine.*
│   │   ├── trust-engine.*
│   │   └── normalization.*
│   └── sandbox/
│       └── capability-runner.*
├── tests/
│   ├── fixtures/
│   │   ├── benign/
│   │   ├── prompt-injection/
│   │   ├── tool-output-injection/
│   │   ├── provenance-tampering/
│   │   └── cross-server-escalation/
│   ├── replay/
│   │   └── baseline-scenarios.*
│   ├── properties/
│   │   └── conformance.*
│   └── metrics/
│       └── scorecard-template.md
└── docs/
    └── evaluation-results.md
```

Notes on the file plan
- `design/threat-model.md` should define actors, assets, trust boundaries, and assumptions used by every POC.
- `design/formal-properties.md` should map each invariant to both a formal spec section and an executable test.
- `tests/fixtures/` should be versioned and reusable across tracks so improvements can be measured on the same corpus.
- `docs/evaluation-results.md` should report both wins and failures; failed hypotheses are still useful findings.

## Recommended build order
1. Threat model and claim inventory.
2. Attack fixture corpus and deterministic replay harness.
3. Policy enforcement gateway POC.
4. Response normalization and provenance envelope.
5. Multi-server trust controls.
6. Capability isolation for highest-risk tools.
7. Narrow formal spec and conformance testing for the broker core.
8. Final scorecard tying research claims to observed evidence.

## Exit criteria for issue #6 validation work
The issue should be considered technically validated when the project has:

- A written threat model tied to enterprise MCP deployments.
- A reusable attack corpus covering prompt injection, tool-output injection, provenance tampering, and cross-server trust failures.
- At least two working defense prototypes evaluated against the same corpus.
- One narrow formal specification with machine-checked safety properties for the enforcement core.
- A results document that explicitly lists which claims were supported, weakened, or falsified.

This keeps the work grounded: the guide can make strong claims only where the repo contains corresponding evidence, test harnesses, and, for the narrow critical core, machine-checkable properties.
