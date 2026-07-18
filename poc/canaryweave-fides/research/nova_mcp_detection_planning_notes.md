# NOVA-informed planning notes for MCP deterministic security detections

Status: quick source-grounded planning notes.
Scope: ProjectOpenHandMonk MCP security research, expanding the existing CanaryWeave MCP benchmark work.
Safety boundary: no raw harmful payloads, no executable misuse strings, no copied adversarial prompts. Payload structures are described only at a category/shape level.

## Evidence base consulted

Primary accessible source:
- Local NOVA rules clone: `/tmp/nova-rules`
- Commit verified locally: `8bb5f23ebade0812b09f48b5267b0c62fee69a8a`
- Blog URL supplied in delegation was Cloudflare-blocked via r.jina, so repo files are the evidence base.

Key source anchors:
- `/tmp/nova-rules/README.md:3` describes NOVA rules as prompt pattern matching for detecting threats in generative AI.
- `/tmp/nova-rules/README.md:7` says NOVA combines keyword detection, semantic similarity, and LLM-based evaluation.
- `/tmp/nova-rules/README.md:57-81` shows a YARA-inspired rule layout with `meta`, `keywords`, `semantics`, `llm`, and `condition` sections.
- `/tmp/nova-rules/CONTRIBUTING.md:39-57` requires strict metadata fields, including description, author, version, category, severity, uuid, and date; unknown unofficial fields fail validation.
- `/tmp/nova-rules/CONTRIBUTING.md:59-65` defines detection sections: keywords, semantics, LLM verification, and boolean condition logic.
- `/tmp/nova-rules/CONTRIBUTING.md:66-74` requires unique PascalCase names, `.nov` files, specific subcategories, tests, and fresh UUIDs.
- `/tmp/nova-rules/CONTRIBUTING.md:90-130` documents YAML test cases with positive/negative expectations and a test runner.
- `/tmp/nova-rules/CONTRIBUTING.md:133-160` distinguishes deterministic CI behavior from optional full LLM evaluation.
- `/tmp/nova-rules/CATEGORIES.md:5-99` defines four high-level families: Prompt Manipulation, Abusing Legitimate Functions, Suspicious Prompt Patterns, and Abnormal Outputs.
- `/tmp/nova-rules/incidents/README.md:1-9` shows an incident-rule convention and notes some detections are reconstructed from public reports with sensitive strings.
- `/tmp/nova-rules/validation/validate_metadata.py:23-27` encodes required fields, optional fields, allowed severities, and category/date patterns.
- `/tmp/nova-rules/validation/lint_rules.py:26-105` checks duplicate UUIDs, duplicate rule names, PascalCase, and non-standard extensions.

Local structural scan of `/tmp/nova-rules`:
- 29 `.nov` files found.
- All 29 have `meta` and `condition` sections.
- 27 include `keywords`.
- 23 include `semantics`.
- 23 include `llm`.
- Severity distribution: 18 high, 7 medium, 4 critical.
- Most represented categories in the local rules are indirect injection, jailbreak, malware-generation/abuse-function patterns, direct injection, and agentic misuse.

Existing ProjectOpenHandMonk anchors:
- `poc/canaryweave/README.md:8-21` describes a safe deterministic MCP protocol-confusion POC with synthetic scenarios, JSON-RPC-shaped logs, inert canary tools, ASR-style metrics, and an attestation/capability shim.
- `poc/canaryweave/README.md:81-88` states safety boundaries: local/inert only, no outbound calls, no secrets, no raw exploit payloads, synthetic canaries only.
- `poc/canaryweave/src/canaryweave/scenario.py:26-39` already defines safe MCP attack/source families: sampling abuse, capability-attestation absence, implicit trust propagation, and structural source families.
- `poc/canaryweave/src/canaryweave/registry.py:105-230` defines a scenario registry with weighted MCP scenario families.
- `poc/canaryweave/src/canaryweave/safety.py:12-140` provides allowlisted inert actions, risky-token rejection, canary format validation, and scenario metadata validation.
- `poc/canaryweave/src/canaryweave/mcp_poc/guardrail.py:34-82` models origin-aware sampling policy: vulnerable mode treats server-originated sampled text as authoritative, hardened mode blocks server sampling from directly causing downstream tool actions.

## NOVA concepts worth borrowing, adapted into our own framework

1. Human-readable rule artifacts
   - Borrow the idea of reviewable rule files with clear metadata plus detection logic.
   - Do not use NOVA branding, `.nov` syntax, copied rule names, UUIDs, or payload lists.
   - Proposed local format: `mcp-rule.yaml` or `mcp-rule.toml` with explicit MCP scopes.

2. Strict metadata discipline
   - Borrow: required `id`, `name`, `description`, `version`, `category`, `severity`, `created`, `modified`, `references`, and `safety_notes`.
   - Add MCP-specific fields not present in NOVA: `scope`, `mcp_phase`, `origin_required`, `capability_context`, `trace_fields`, `recommended_action`, and `safe_fixture_ids`.

3. Layered detection, but deterministic-first
   - NOVA layers keyword, semantic, LLM, and boolean condition logic.
   - For MCP benchmark work, prioritize deterministic detectors first:
     - normalized text/Unicode structure checks;
     - JSON-RPC field checks;
     - tool/capability allowlist checks;
     - origin/provenance checks;
     - sink/source mismatch checks;
     - canary-flow checks.
   - Treat semantic or LLM review as optional triage metadata, not as the authority for benchmark pass/fail.

4. Boolean conditions over named signals
   - Borrow the named-signal pattern and boolean conditions.
   - Use safer signal names such as `origin_mismatch`, `untrusted_content_instruction_shape`, `hidden_text_marker`, `capability_unbound`, `sampling_output_to_tool_call`, `unauthorized_canary_flow`, and `overbroad_tool_permission`.
   - Conditions should combine structural signals, not raw attack phrases.

5. Taxonomy as an evaluation backbone
   - Borrow the category/subcategory discipline.
   - Create an MCP-native taxonomy rather than copying NOVA categories directly.
   - Require every rule, scenario, and metric row to map to exactly one primary category and optionally multiple secondary tags.

6. Offline CI validation and fixtures
   - Borrow syntax validation, metadata validation, linting, duplicate-ID checks, and YAML-style tests.
   - Keep CI deterministic and local.
   - Positive fixtures should be synthetic structural examples, not real adversarial payloads.
   - Negative fixtures should include benign MCP traces, benign tool descriptions, and benign sampled model outputs.

7. Incident/provenance handling
   - Borrow the idea of incident- or report-grounded detections, but store only structural summaries, source hashes, and report citations.
   - Never commit raw sensitive strings from reports or upstream corpora.

## What not to copy from NOVA/rules

- Do not copy `.nov` grammar, exact rule names, exact UUIDs, exact metadata schema, or exact payload strings.
- Do not copy raw keyword lists from rules that reference jailbreaks, command execution, credential access, malware, phishing, or exfiltration.
- Do not make LLM evaluation a blocking CI dependency. NOVA explicitly separates CI mode from optional LLM testing; our MCP benchmark should make deterministic trace results the reproducible ground truth.
- Do not rely primarily on broad prompt phrase matching. MCP risks often appear as protocol/state violations: untrusted origin, missing capability binding, server-to-host authority confusion, unsafe sink routing, or cross-context propagation.
- Do not import real malicious examples into scenarios, tests, or docs. Maintain CanaryWeave’s existing canary-only safety boundary.
- Do not overfit to NOVA’s prompt-only perspective. Our unit of detection should often be a full MCP trace/event, not just a prompt string.

## Proposed MCP-native taxonomy mapping

High-level taxonomy for our own framework:

1. `mcp_prompt_boundary`
   - Inspired by NOVA Prompt Manipulation.
   - MCP focus:
     - direct user attempt to alter host/tool policy;
     - indirect instruction-shaped content in resources, tool descriptions, web/RAG content, or sampled server output;
     - hidden instructions in comments, markdown references, or visually hidden text.
   - Deterministic detections:
     - untrusted origin contains instruction-shaped text;
     - hidden/encoded/unicode-obfuscated content appears in a field that the host may pass to a model;
     - tool/resource description contains role or authority markers not allowed by manifest policy.

2. `mcp_agentic_misuse`
   - Inspired by NOVA Abusing Legitimate Functions, especially agentic misuse and data exfiltration subfamilies.
   - MCP focus:
     - sampled output proposes a tool call;
     - tool call exceeds user-granted capability;
     - server-originated content is treated as host policy;
     - tool output is routed to an unauthorized sink;
     - benign canary leaves its expected boundary.
   - Deterministic detections:
     - `action.capability` not in `allowed_capabilities`;
     - tool call origin is `server_sampling` or `resource_content` but action requires host/user authority;
     - canary marker appears in a sink/event where it is not authorized;
     - missing attestation/capability signature for a privileged symbolic action.

3. `mcp_suspicious_structure`
   - Inspired by NOVA Suspicious Prompt Patterns.
   - MCP focus:
     - hidden Unicode and zero-width-like structure;
     - long encoded blobs or fragmented instructions across events;
     - chained sampled candidates where one candidate seeds another;
     - role relabeling or origin relabeling in JSON/event fields.
   - Deterministic detections:
     - normalization changes semantic-looking token boundaries materially;
     - unusual ratio of invisible/control characters;
     - encoded/fragmented content length/entropy thresholds;
     - repeated cross-message fragments that reconstruct instruction-shaped structure;
     - conflict between transport provenance and claimed role label.

4. `mcp_abnormal_output`
   - Inspired by NOVA Abnormal Outputs.
   - MCP focus:
     - model/sampling output includes policy/system metadata shape;
     - sampled plan includes canary or secret-like marker in untrusted context;
     - output contains executable-action JSON shape that should only be emitted by host policy code;
     - output discloses internal guardrail reasoning beyond allowed audit text.
   - Deterministic detections:
     - canary or synthetic secret marker appears in model output;
     - output contains a tool-plan schema from an untrusted source;
     - output includes internal policy labels not intended for the model-visible channel.

5. `mcp_supply_chain_manifest`
   - Inspired by NOVA skill/security rules and supply-chain subcategories.
   - MCP focus:
     - malicious or overbroad MCP server manifests;
     - tool descriptions that request authority they should not have;
     - package/readme/manifest fields that hide instructions;
     - dynamic-context or runtime interpolation features in server metadata.
   - Deterministic detections:
     - wildcard or overbroad tool permission surfaces;
     - hidden content markers in manifest/docs;
     - risky dynamic-evaluation structure in configuration fields;
     - mismatch between declared tool purpose and requested capability class.

## Candidate rule artifact shape

Proposed schema sketch, intentionally not NOVA syntax:

```yaml
id: mcp-rule-0001
name: ServerSamplingOriginBoundary
version: 0.1.0
category: mcp_agentic_misuse/origin_authority_confusion
severity: high
scope: jsonrpc_trace
mcp_phase: sampling_result_to_tool_dispatch
description: Detects server-originated sampled content being treated as host-authoritative tool policy.
signals:
  - name: source_is_server_sampling
    type: event_field_equals
    field: source
    value: server_sampling
  - name: proposes_tool_action
    type: schema_shape
    shape: tool_plan_like_json
  - name: action_requires_host_authority
    type: capability_policy
    relation: not_granted_by_user_or_host
condition: source_is_server_sampling and proposes_tool_action and action_requires_host_authority
recommended_action: block_and_audit
fixtures:
  positive: synthetic_canary_trace_origin_mismatch
  negative: synthetic_host_authorized_trace
safety_notes: Synthetic canaries only; no real commands, URLs, secrets, or payload text.
```

## Integration plan for ProjectOpenHandMonk

1. Add a new rules submodule next to CanaryWeave or inside a new POC folder.
   - If expanding CanaryWeave directly: `poc/canaryweave/src/canaryweave/detections/`.
   - If starting a separate project: copy `poc/_template/` and use a name such as `poc/mcp-sentinel` or `poc/monk-mcp-rules`.

2. Implement deterministic detection primitives first.
   - Text normalizers: Unicode visibility, control-character ratio, encoding-structure indicators, redacted instruction-shape classifiers.
   - Trace predicates: source/origin field checks, role/provenance mismatch, JSON-RPC method/phase checks.
   - Capability predicates: action not in allowed set, missing attestation, sink mismatch.
   - Canary predicates: benign marker appears in unauthorized event/sink/output.

3. Reuse CanaryWeave scenario metadata and event traces.
   - Current `ScenarioMetadata` already records `scenario_family`, `attack_type`, `source_family`, `source_adapter`, `source_digest`, `abuse_axis`, and `trust_failure`.
   - Current guardrail logic already encodes the key origin-aware sampling boundary for vulnerable vs hardened policies.
   - Rules should consume CanaryWeave traces as fixtures rather than duplicating scenario generation.

4. Build validation and CI gates.
   - Metadata validator: required fields, severity enum, category enum, safe fixture IDs, no unknown fields unless explicitly versioned.
   - Syntax/schema validator: YAML/TOML parse and condition references resolve to declared signals.
   - Linter: unique IDs, unique names, naming convention, no raw risky tokens, no URLs/secrets/commands in fixtures.
   - Test runner: positive/negative synthetic fixtures, deterministic offline pass/fail.

5. Publish rule-to-metric reporting.
   - For each run, emit per-rule counts: matched traces, blocked traces, false-positive fixtures, category coverage, and mapping to CanaryWeave attack types.
   - Keep ASR-style metrics separate from detection rates: ASR measures simulator unauthorized execution; detection rate measures whether a rule identified the structural risk.

## Initial rule families to prototype

1. `ServerSamplingOriginBoundary`
   - Category: `mcp_agentic_misuse/origin_authority_confusion`
   - Detects: server-originated sampled content leading directly to a tool action without host/user authority.
   - Grounding: CanaryWeave guardrail vulnerable vs hardened policy models this exact boundary.

2. `CapabilityAttestationMissing`
   - Category: `mcp_agentic_misuse/capability_binding_absence`
   - Detects: symbolic action lacks matching capability/attestation for the current scenario.
   - Grounding: CanaryWeave includes capability-attestation absence as a typed attack class.

3. `UntrustedManifestHiddenInstructionShape`
   - Category: `mcp_supply_chain_manifest/hidden_instruction_structure`
   - Detects: hidden/comment/invisible/encoded structure in MCP manifest, tool description, or docs fields.
   - Grounding: NOVA categories include hidden instructions, Unicode tricks, and indirect injection; skill rules include hidden reference/documentation structures, but we should use only structural indicators.

4. `CanaryBoundaryCrossing`
   - Category: `mcp_agentic_misuse/unauthorized_data_flow`
   - Detects: benign canary appears outside an allowed event/sink/source path.
   - Grounding: CanaryWeave safety and metrics already rely on synthetic `CANARY_*` and `DEMO_CANARY_*` markers.

5. `SamplingCandidateRevalidationGap`
   - Category: `mcp_suspicious_structure/chained_sampling_state`
   - Detects: cached or replayed sampled candidate is reused without fresh policy/capability validation.
   - Grounding: CanaryWeave registry includes sampling candidate replay and related sampling-abuse families.

## Open design questions

1. Rule language: YAML/TOML declarative rules, Python dataclass rules, or a tiny DSL? Declarative files are easier to review; Python predicates are easier for JSON-RPC trace logic.

2. Detection unit: should every rule operate on a single text field, a single JSON-RPC event, a window of events, or a full scenario trace? MCP protocol issues likely need event windows.

3. Blocking semantics: should rules produce `alert`, `block`, `quarantine`, or `audit-only` decisions? Some structural signals are high-confidence only in combination with origin/capability context.

4. Normalization boundary: how aggressively should the framework decode/normalize suspicious text structures without reconstructing or storing harmful payloads?

5. Evaluation design: how do we report detection coverage, false positives, and ASR reduction without conflating deterministic simulator success with real-world exploitation likelihood?

## Bottom line

Use NOVA as inspiration for rule organization, metadata strictness, taxonomy discipline, layered signals, and CI-tested fixtures. Do not copy payloads, exact rules, or prompt-only assumptions. The ProjectOpenHandMonk opportunity is an MCP-native deterministic detection framework where the primary signals are protocol provenance, capability binding, trace semantics, and benign canary data-flow boundaries.
