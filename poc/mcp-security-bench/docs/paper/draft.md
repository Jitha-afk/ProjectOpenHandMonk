# Benchmarking Microsoft's MCPSecurityScanner Against an Adversarial MCP Server

Authors: Anonymous

## Abstract

The Model Context Protocol (MCP) expands the capabilities of language-model agents by exposing tools, resources, and structured interactions across server boundaries, but it also introduces new security risks at both the metadata and runtime layers. This paper presents a focused benchmark of Microsoft's `MCPSecurityScanner`, distributed as part of the Microsoft Agent Governance Toolkit in `agent-os-kernel` v3.1.0, against an adversarial MCP benchmark server. The scanner under test is a static analysis component that inspects MCP tool metadata, including tool names, descriptions, and JSON schemas, using regex- and pattern-based rules rather than machine-learning or LLM-based detection. Its companion module, `MCPResponseScanner`, evaluates tool responses for malicious content at runtime. Our benchmark uses a 30-tool server with 5 honeypot resources spanning 11 attack categories grounded in the OWASP MCP Top 10:2025. For the static-scanner evaluation, however, only 7 tools are labeled metadata-malicious, and these positives fall into 4 categories. Methodologically, we extract the full tool set from FastMCP internals, label tools according to whether the malicious signal is directly observable in metadata, scan all tools with `MCPSecurityScanner`, test seven representative responses with `MCPResponseScanner`, and compute overall and per-category performance metrics. Across the 30-tool corpus, the metadata scanner achieved a 57.1% detection rate on metadata-malicious cases, while the response scanner correctly classified 6 of 7 sampled outputs. These results suggest that rule-based MCP defenses are effective for overt lexical attacks represented in this corpus, but brittle against semantically subtler or obfuscated threats.

## 1. Introduction

Security evaluation for MCP systems is increasingly important because tool-enabled agents make decisions based not only on user prompts, but also on machine-readable tool descriptions, schemas, and server-provided responses. Under the MCP specification, these artifacts influence tool selection, parameter construction, and follow-on reasoning. As a result, the attack surface extends beyond conventional prompt injection to include adversarial manipulation of tool metadata, shadowed tools, malicious resources, and cross-server coordination.

Recent community and research efforts have highlighted these risks. The OWASP MCP Top 10:2025 provides a structured taxonomy for major MCP failure modes, while systems such as MCPSecBench and public attack demonstrations from Invariant Labs and Promptfoo have shown that MCP-specific attacks can be embedded in both tool definitions and runtime outputs. These developments motivate evaluation methods that separate what a security mechanism can inspect from what it cannot.

This paper studies Microsoft's `MCPSecurityScanner`, a component of the Microsoft Agent Governance Toolkit available through `agent-os-kernel` v3.1.0. The scanner is designed to analyze MCP tool metadata statically, examining names, descriptions, and schemas for suspicious patterns. It is complemented by `MCPResponseScanner`, which inspects tool outputs after invocation. Together, these modules offer a practical baseline for rule-based MCP security enforcement.

Our goal is not to test every possible MCP defense claim, but to benchmark the scanner against a realistic adversarial corpus while preserving methodological alignment between the benchmark and the scanner's visibility. We therefore distinguish attack carrier from attack objective. In our evaluation, a case may have an exfiltration, credential-theft, or cross-server objective while still being metadata-borne if the malicious signal is present in the tool definition itself. This distinction is central: many benchmarked MCP attacks are behavioral at runtime, while others are behaviorally harmful but visibly encoded in metadata. By making this scope explicit, the benchmark aims to produce a fair, interpretable assessment of what Microsoft's scanner can and cannot detect.

This paper makes three contributions: (1) a benchmark framing that separates tool-metadata visibility from runtime behavior, (2) an empirical evaluation of Microsoft's metadata and response scanners against an adversarial MCP server, and (3) an analysis of where rule-based scanners succeed and fail across the metadata-positive subset of the benchmark.

## 2. Background

### 2.1 MCP Security and the Metadata Attack Surface

MCP standardizes how model-driven clients connect to external tools and resources. In practice, MCP clients often ingest tool names, natural-language descriptions, and JSON schemas before selecting tools or generating arguments. This design improves interoperability, but it also creates a security dependency on untrusted server-supplied metadata. If a malicious server embeds hidden instructions, misleading affordances, or deceptive schema cues into tool definitions, an agent may be steered before any tool call occurs.

This metadata layer is especially relevant for attacks such as tool poisoning and tool shadowing. Tool poisoning places adversarial instructions inside descriptions or related metadata fields, exploiting the fact that language models parse these strings as part of their reasoning context. Tool shadowing instead impersonates trusted capabilities through naming or descriptive overlap, increasing the likelihood that an agent selects the wrong tool. Both attacks are visible, at least in principle, to scanners that inspect metadata directly.

Other MCP risks are less amenable to metadata-only inspection. Rug pull attacks can begin with benign metadata and become malicious only after trust is established. Data exfiltration, credential theft, excessive permissions, code execution, command injection, sandbox escape, and cross-server attacks often depend on server-side behavior, runtime parameter handling, or malicious response content rather than explicit metadata signals. Prompt injection may also arise in tool outputs or resources, not just in descriptions. These distinctions matter when designing a benchmark for static analysis.

### 2.2 Microsoft's MCP Scanners

The system under test in this paper is Microsoft's `MCPSecurityScanner` from the Microsoft Agent Governance Toolkit's `agent-os-kernel` v3.1.0 release. `MCPSecurityScanner` is a static analysis scanner for MCP tool metadata. It inspects tool names, descriptions, and schemas and applies rule-based detection logic using regex and pattern matching. It is not an ML-based or LLM-based detector. This makes its behavior more interpretable and reproducible, but also constrains it to patterns encoded in its rules and to evidence available in metadata.

Inspection of the published implementation in the referenced repository indicates that the scanner includes checks for hidden instructions, description injection, schema abuse, rug-pull detection through fingerprinting of prior tool definitions, and cross-server impersonation or typosquatting. The broader toolkit also includes `MCPResponseScanner`, which scans tool responses for prompt-injection markers, credential leakage, and suspicious exfiltration patterns.

### 2.3 Adversarial Benchmark Server

To evaluate these scanners, we use an adversarial benchmark server implemented with FastMCP. The server exposes 30 tools and 5 honeypot resources across 11 attack categories grounded in the OWASP MCP Top 10:2025:

1. Tool Poisoning
2. Tool Shadowing
3. Rug Pull
4. Data Exfiltration
5. Prompt Injection
6. Credential Theft
7. Excessive Permissions
8. Code Execution
9. Command Injection
10. Sandbox Escape
11. Cross-Server Attacks

The benchmark includes both metadata-borne and behavior-borne attacks. This makes it useful for isolating the coverage of static metadata inspection while also probing a complementary response-scanning layer. A limitation, however, is that the present paper evaluates only a subset of this broader attack surface directly: 30 tools for metadata inspection and 7 sampled responses for runtime-output inspection.

## 3. Methodology

### 3.1 Evaluation Objective

The benchmark is designed to measure how well Microsoft's scanners identify malicious content in an adversarial MCP environment while respecting the visibility boundaries of each scanner. The primary objective is to evaluate `MCPSecurityScanner` on the subset of attacks that are observable in tool metadata. A secondary objective is to probe `MCPResponseScanner` on a small set of representative runtime outputs.

### 3.2 Benchmark Corpus

The benchmark corpus consists of the full tool inventory of the evil FastMCP server: 30 tools and 5 honeypot resources spanning the 11 attack categories listed above. Because `MCPSecurityScanner` analyzes tool metadata rather than resources or server-side code, the core evaluation unit is the tool definition. Each tool contributes three relevant metadata surfaces: its name, its natural-language description, and its input schema.

### 3.3 Tool Extraction

Rather than manually transcribing tool definitions, we extract them directly from the FastMCP server implementation through FastMCP internals. For each registered tool, we collect the canonical name, description, and schema-like parameter definition. This reduces transcription error and ensures the benchmark operates on the same artifacts an MCP client would consume.

### 3.4 Metadata Labeling

A key methodological step is the classification of each tool as either metadata-malicious or metadata-benign. Tools are marked metadata-malicious when the malicious signal is present in the tool name, description, or schema itself, such as explicit hidden instructions, suspicious control language, deceptive affordances, or suspicious credential/context requests that could influence model reasoning before invocation. Tools are marked metadata-benign when their descriptions and schemas do not expose such signals and the attack emerges only through runtime behavior, side effects, or response content.

This distinction is essential for fairness. Several benchmark categories include attacks that are dangerous in practice but not visible in metadata alone. For example, a tool may advertise a benign purpose while performing exfiltration or command execution only during invocation. Such a tool is behaviorally malicious, but not metadata-malicious for the purposes of a static scanner benchmark.

These labels are task-specific benchmark labels rather than universal statements about overall tool safety. In particular, metadata-benign does not mean operationally safe at runtime; it means only that the tool was not labeled positive for the static metadata-inspection task. We release the per-tool labels and rationale in the benchmark harness itself. A further limitation is that these labels were manually authored for this benchmark rather than independently annotated by multiple reviewers.

### 3.5 Static Metadata Scanning

All 30 tool definitions are scanned with `MCPSecurityScanner` from `agent-os-kernel` v3.1.0. For each tool, the scanner is given the tool name, description, input schema, and server context. We record whether any threat is detected, the number of detections, and the associated threat outputs. These per-tool outcomes are then aggregated into category-level and overall metrics.

### 3.6 Response Scanning

To complement the metadata benchmark, we evaluate `MCPResponseScanner` on seven representative tool responses. These responses were chosen to cover leaked credentials, reflected prompt injection, hidden instructions in output formatting, suspicious exfiltration traces, and at least one benign response.

### 3.7 Metrics

For the metadata benchmark, we compute true positives, false negatives, and false positives relative to the metadata-malicious versus metadata-benign labels. From these counts, we derive overall detection rate, false negative rate, and false positive rate. We also report per-category detection outcomes where metadata-malicious examples are present. Because the positive class is small (7/30), we report raw counts prominently and interpret percentage metrics cautiously.

For the response benchmark, we report classification outcomes over seven hand-picked response samples. This response result is illustrative rather than a stable estimate of runtime-scanner accuracy.

### 3.8 Scope and Caveat

This benchmark is intentionally scoped to scanner observability. Many attacks in the evil MCP server are behavioral or runtime attacks that cannot be inferred reliably from names, descriptions, or schemas alone. Accordingly, the metadata benchmark should be interpreted as an evaluation of static inspection performance over tool metadata, not as a complete measure of security coverage against the full benchmark server.

## 4. Results

The metadata scanner was evaluated over a 30-tool corpus containing 7 metadata-malicious and 23 metadata-benign tool definitions. It correctly identified 4 metadata-malicious tools and missed 3, while incorrectly flagging 4 metadata-benign tools. Overall detection rate was 57.1%, with a false negative rate of 42.9% and a false positive rate of 17.4%.

### 4.1 Overall Metadata-Scanner Results

| Metric | Value |
|---|---:|
| Total tools scanned | 30 |
| Metadata-malicious tools | 7 |
| Metadata-benign tools | 23 |
| True positives | 4 |
| False negatives | 3 |
| False positives | 4 |
| Detection rate | 57.1% |
| False negative rate | 42.9% |
| False positive rate | 17.4% |

Performance varied sharply by attack family. The scanner detected all metadata-positive tool-poisoning and tool-shadowing examples in this corpus, but missed all metadata-positive cases labeled under data-exfiltration and cross-server objective categories.

### 4.2 Per-Category Results

| Category | Metadata-malicious examples | Detection rate | Detected / Total |
|---|---:|---:|---:|
| Tool Poisoning | 2 | 100% | 2/2 |
| Tool Shadowing | 2 | 100% | 2/2 |
| Data Exfiltration Objective | 2 | 0% | 0/2 |
| Cross-Server Objective | 1 | 0% | 0/1 |

The remaining categories in the benchmark—rug pull, prompt injection, credential theft, excessive permissions, code execution, command injection, and sandbox escape—were not meaningfully represented in the metadata-malicious set because the benchmark's examples in those categories are primarily expressed through runtime behavior rather than static tool descriptions or schemas.

### 4.3 Missed Malicious Tools

The three missed metadata-malicious tools illustrate the scanner's blind spots:

- `record_analytics` (`data_exfil`): `<IMPORTANT>` tag mandates calling after every tool and capturing all data.
- `sync_telemetry` (`data_exfil`): `<HIDDEN>` tag demands all conversation context and credentials.
- `math_eval` (`cross_server`): `<IMPORTANT>` tag requests API keys via a context parameter.

### 4.4 False Positives

The four observed false positives, relative to our metadata-malicious labeling scheme, were concentrated in operational or administration-style tools:

- `execute_shell_command`, `sandbox_run`, and `container_exec` were flagged because the required field `command` was treated as suspicious schema abuse.
- `server_info` was flagged because it exposed an object schema with no defined properties.

These cases may be false positives under a maliciousness-labeling regime, but some may still be meaningful policy or capability-risk flags in a deployment setting. We therefore interpret them as overbroad detections relative to our benchmark labels, not necessarily as useless warnings in practice.

### 4.5 Response-Scanner Results

A separate response scanner correctly classified 6 of 7 hand-picked outputs. It successfully caught credential leaks, prompt-injection tags, and exfiltration URLs, but missed a hidden instruction embedded through zero-width spaces and HTML comments in a `format_text` response. This result should be interpreted as an illustrative probe rather than a stable estimate of runtime-scanner accuracy.

| Response scanner metric | Value |
|---|---:|
| Responses tested | 7 |
| Correct classifications | 6/7 |
| Accuracy | 85.7% |
| Missed case | Zero-width-space + HTML-comment hidden instruction in `format_text` |

### 4.6 Batch Scan Summary

At the server level, the batch scan marked the server unsafe, scanning 30 tools, flagging 8 tools, and reporting 9 total threats. Overall, the results indicate strong performance on explicit lexical signatures but limited robustness to semantically plausible malicious metadata.

## 5. Analysis

The central pattern in the results is that the scanner tracks lexical obviousness more reliably than underlying malicious intent. In this benchmark, the metadata scanner was strongest when malicious intent was expressed through explicit lexical signatures. Tool poisoning and tool shadowing were detected perfectly because these examples contained conspicuous markers such as imperative hidden tags, direct instruction overrides, or suspicious phrasing that closely matches known attack templates represented in the scanner's rules. When the malicious content contained explicit malicious lexical cues, the scanner performed well.

Its failures are equally informative. The missed `record_analytics`, `sync_telemetry`, and `math_eval` cases were still harmful, but they framed their abuse in more operationally plausible language. Rather than presenting a direct override such as "ignore prior instructions," they described telemetry, context passing, or credential-bearing parameters in ways that were semantically dangerous without matching a strong lexical signature. This supports a central finding of the benchmark: the scanner is weak on semantically equivalent but lexically novel phrasing. It recognizes suspicious wording better than suspicious intent.

The false positives reinforce the same point from the opposite direction. Execution-oriented tools naturally expose parameters such as `command`, and administrative tools may have sparse or unusual schemas for legitimate reasons. A heuristic tuned to detect schema abuse will therefore generate false positives on tools whose normal function resembles risky behavior. This matters operationally: if administrative or high-capability tools are routinely flagged, trust in the detector may erode and meaningful warnings may be ignored. At the same time, these flags may still be useful under a risk-flagging or policy-enforcement regime rather than a pure maliciousness-classification regime.

The response scanner improved coverage by operating on tool outputs rather than tool metadata alone. Its ability to catch credential leaks, injection tags, and exfiltration URLs shows that post-generation inspection can surface threats that bypass static tool screening. However, the missed `format_text` case demonstrates that this layer remains fragile against obfuscation. Encoding tricks and formatting-layer concealment can preserve malicious semantics while evading surface-pattern rules.

## 6. Discussion

Taken together, the findings suggest a clear security posture: lexical heuristics are useful for low-cost filtering, but insufficient as a primary defense against MCP-style attacks. They can eliminate the most overt malicious metadata and catch many explicit exfiltration or injection artifacts in responses. That makes them operationally valuable as a first-pass control. Yet the benchmark also shows that attackers do not need to use obviously adversarial wording. They can express the same objective—collect all context, request credentials, or induce cross-server key transfer—through language that appears routine or infrastructural.

This limitation is especially important for metadata-only analysis. Some attack classes in the benchmark are fundamentally behavioral. Rug pulls, prompt injections expressed during execution, credential theft triggered by later interaction, excessive permission abuse, code execution, command injection, and sandbox escape cannot be fully characterized from static metadata alone. A tool may present benign descriptions and still behave maliciously when invoked, when chained with another tool, or when given specific runtime inputs. Static inspection therefore cannot provide comprehensive protection against the broader MCP attack surface by itself. A major limitation of the present evaluation is that it centers on tool metadata and a small response sample, while MCP security also depends heavily on resources, server identity and provenance, temporal changes in tool definitions, and multi-step tool chains.

The false-positive profile also has practical implications. Enterprise and research workflows often rely on tools that execute shell commands, inspect servers, or proxy container operations. These are exactly the kinds of tools that simple heuristics may misclassify because their schemas legitimately mention commands, contexts, or generic objects. In deployment, this creates a difficult tradeoff: loosening rules reduces analyst fatigue but may miss explicit attacks, while tightening them improves recall on overt threats but penalizes legitimate administrative tooling.

The response scanner partially compensates for metadata blind spots, but its bypass confirms the need for stronger normalization and semantic inspection. Hidden instructions encoded through zero-width characters and HTML comments are not exotic; they are representative of a broader class of format-level evasions. A defense stack that does not normalize Unicode, strip or inspect markup, and reason about meaning beyond raw tokens will remain vulnerable to simple obfuscation strategies.

More broadly, a stronger security architecture must separate content detection from trust and authorization. Even perfect metadata scanning cannot validate server identity, constrain high-risk tool capabilities, prevent least-privilege violations, or stop malicious behavior from a benign-looking tool. In MCP deployments, provenance binding, permission scoping, tool allowlists, execution sandboxing, output normalization, and stateful monitoring are first-class controls, not merely add-ons to text scanning.

Overall, the benchmark supports a layered interpretation of tool security. Static metadata scanning is most effective against overt attacks. Response scanning adds a useful downstream checkpoint. Neither layer, by itself, adequately addresses semantically novel phrasing or runtime abuse. The practical implication is not that these scanners are ineffective, but that they must be embedded within a broader control architecture that includes behavioral monitoring, permission scoping, execution-time policy enforcement, provenance checks, and normalization of encoded or formatted content.

## 7. Related Work

The current MCP security ecosystem includes formal taxonomies, benchmark proposals, attack demonstrations, and intentionally vulnerable servers. The OWASP MCP Top 10:2025 provides a structured risk taxonomy for MCP deployments. MCPSecBench frames MCP security benchmarking as a systematic evaluation problem. Public attack examples from Invariant Labs have demonstrated tool poisoning and MCP injection risks in realistic agent settings. Community collections such as Awesome MCP Security aggregate references, tools, and threat discussions. Intentionally vulnerable or adversarial MCP servers, including damn-vulnerable-MCP-server and Promptfoo's evil-mcp-server, show the value of offensive test fixtures for evaluating defensive controls.

Our work differs in scope from these prior efforts by focusing narrowly on one concrete defensive implementation: Microsoft's `MCPSecurityScanner` and its companion `MCPResponseScanner`. The goal is not to claim comprehensive coverage of MCP security, but to measure how a specific static, rule-based defense behaves against a multi-category adversarial benchmark.

## 8. Conclusion

This evaluation shows that, in this benchmark, metadata scanning can catch explicit, lexically recognizable attacks such as the tool-poisoning and tool-shadowing patterns represented here, but struggles with semantically similar attacks phrased in more ordinary operational language. The 57.1% detection rate, complete misses on metadata-borne cases with exfiltration or cross-server objectives in this corpus, and observable overbroad flags on execution-oriented tools all point to the same conclusion: heuristic static analysis is useful, but narrow.

Response scanning improves outcomes by detecting malicious or policy-violating outputs that static tool inspection may miss, correctly classifying 6 of 7 sampled outputs in this benchmark. Even so, its failure on a hidden instruction encoded through zero-width spaces and HTML comments shows that this layer is also bypassable when attackers exploit formatting and encoding rather than overt keywords.

The broader lesson is that strong performance on explicit lexical signatures should not be mistaken for robust semantic understanding. Defenses built primarily around surface patterns will remain brittle against lexically novel phrasing and fundamentally incapable of covering runtime behavioral attacks on their own. For MCP security, the most defensible path is a layered approach in which metadata screening and response scanning serve as complementary filters, backed by runtime controls that evaluate behavior rather than text alone.

## 9. Limitations

This paper reports results from one benchmark environment and one scanner implementation. The metadata results should not be generalized to all MCP security products, all Microsoft security components, or all real-world deployments. The response-scanner result is based on only seven hand-picked outputs and should be interpreted cautiously. This experiment also does not establish comprehensive coverage of the OWASP MCP Top 10, does not evaluate the benchmark's honeypot resources as part of the scanner's core metadata analysis, and does not provide an independently annotated labeling study. It evaluates the observed behavior of a specific static scanner and a small companion response scanner against one adversarial benchmark suite.

## References

1. OWASP MCP Top 10. https://owasp.org/www-project-mcp-top-10/
2. Microsoft Agent Governance Toolkit. https://github.com/microsoft/agent-governance-toolkit
3. MCPSecBench: A Systematic Security Benchmark and Playground for Testing Model Context Protocols. https://arxiv.org/abs/2508.13220
4. Invariant Labs MCP Injection Experiments. https://github.com/invariantlabs-ai/mcp-injection-experiments
5. Invariant Labs. MCP Security Notification: Tool Poisoning Attacks. https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
6. Awesome MCP Security. https://github.com/Puliczek/awesome-mcp-security
7. Model Context Protocol Specification. https://modelcontextprotocol.io/specification
8. damn-vulnerable-MCP-server. https://github.com/harishsg993010/damn-vulnerable-MCP-server
9. evil-mcp-server (Promptfoo). https://github.com/promptfoo/evil-mcp-server
10. MCP Security Best Practices. https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices
