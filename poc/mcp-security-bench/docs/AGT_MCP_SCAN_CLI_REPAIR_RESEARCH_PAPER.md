# Repairing an MCP Metadata Scanner: A ProjectOpenHandMonk Research Analysis of the AGT `mcp-scan` CLI Contribution

**Project:** ProjectOpenHandMonk `poc/mcp-security-bench`  
**Document type:** Research-style analysis of an open-source contribution repair  
**Primary source artifact:** `/home/sealjitha/projects/agent-governance-toolkit/docs/tutorials/27-mcp-scan-cli-case-study.md`  
**Status:** Evidence-grounded writing pass; not an upstream AGT tutorial

## Abstract

This paper analyzes a focused repair to the Agent Governance Toolkit (AGT) MCP Scan CLI as a case study in aligning security-tooling claims, executable behavior, and regression evidence. The central claim is narrow: the repair described in the AGT case study converted an MCP scan user journey from a drifted tutorial/CLI contract into a tested metadata-inspection workflow that can enumerate advertised MCP primitives and pass their normalized metadata into AGT's existing `MCPSecurityScanner`.

The source artifact reports that the baseline tutorial described a user-facing MCP scanner, while the package exposed no matching `mcp-scan` console script, the old implementation scanned only static launch/configuration metadata, and the regression test file was skipped because expected helpers did not exist. The repaired design added a packaged `mcp-scan` entry point, implemented metadata-only MCP inspection across stdio, Streamable HTTP, and legacy HTTP+SSE transports, restored regression coverage, and documented conservative operational behavior such as `--static-only`, sanitized child environments for stdio inspection, fail-closed inspection errors, and CI-relevant exit codes.

This analysis treats the AGT case study as evidence for a specific contribution repair, not as proof of general MCP safety, not as certification of full OWASP MCP Top 10 coverage, and not as ProjectOpenHandMonk documentation to upstream into AGT. The contribution is best understood as a practical security-engineering alignment: the CLI, documentation, tests, and scanner integration were brought into closer correspondence around MCP primitive metadata inspection.

## Introduction

MCP servers advertise tools, resources, resource templates, and prompts to clients. Those advertised definitions are security-relevant because names, descriptions, URIs, templates, and schemas may become planning context for an LLM-driven agent. A scanner that claims to assess MCP poisoning risk but never connects to a server to inspect its advertised primitives can create a misleading sense of coverage.

ProjectOpenHandMonk's `mcp-security-bench` work studies MCP trust-boundary risks through benchmark and documentation artifacts. The AGT `mcp-scan` repair case study is relevant to this project because it describes a concrete open-source tooling repair aimed at making MCP metadata inspection executable, test-backed, and honest about its limits.

Research question:

Can a drifted MCP scan CLI/tutorial contract be repaired into a bounded, test-backed workflow where a user can install a command, scan an MCP configuration, enumerate advertised MCP primitive metadata, and obtain findings from an existing scanner without claiming broader MCP safety than the evidence supports?

The answer supported by the source artifact is yes, within explicit limits. The repair does not make the scanner a runtime prevention layer. It does not validate every possible MCP attack. It does not prove that a server is benign. It aligns a specific CLI workflow with live metadata enumeration, static-only review mode, fingerprinting over normalized primitive metadata, and regression tests.

## Background/Problem

### MCP metadata as a security surface

The broader ProjectOpenHandMonk EvilBench documentation frames hostile MCP metadata and hostile MCP outputs as distinct trust-boundary risks. In `docs/EVILBENCH_RESEARCH_REPORT.md`, the benchmark report describes tool descriptions as server-provided context that can embed instructions attempting credential access, exfiltration, or behavioral override. That framing matters for the AGT repair because `mcp-scan` is concerned with metadata inspection rather than runtime tool execution.

Observed fact from ProjectOpenHandMonk context:

- `docs/EVILBENCH_RESEARCH_REPORT.md` identifies hostile tool metadata as a repeatable MCP attack surface.
- `docs/HERMES_KLIVE_E2E_SUMMARY_FOR_MIRA.md` emphasizes that malicious instructions in tool metadata are not user prompts; they are MCP-native trust-boundary inputs.

Interpretation:

- A scanner that inspects only local launch configuration is materially different from a scanner that enumerates server-advertised MCP primitives. The former can find risky command shapes; the latter can also expose metadata-level poisoning patterns.

### Baseline AGT contract drift

The AGT case study reports a baseline mismatch among documentation, packaging, implementation, and tests.

Observed facts from the AGT source artifact:

- The old Tutorial 27 instructed users to run `agentos mcp-scan ...`.
- Package metadata exposed only `agent-os = "agent_os.cli:main"`; no matching `mcp-scan` console script was available.
- The main `agent-os` router did not contain an `mcp-scan` subcommand.
- The standalone module could be run with `python -m agent_os.cli.mcp_scan`, but that was not the documented user journey.
- Baseline reproduction reported `python -m pytest tests/test_mcp_scan_cli.py -q --tb=short` as `collected 0 items / 1 skipped`.
- The old `scan_config()` checked launch/configuration properties such as environment key names, `sudo`, `/tmp` commands, and suspicious absolute paths in arguments.
- The old implementation did not inspect `tools/list`, `resources/list`, `resources/templates/list`, or `prompts/list`, did not parse discovered primitive metadata, and did not call `MCPSecurityScanner.scan_server()`.
- The skipped regression file encoded desired behavior for config loading, parsing, scanning, output formatting, fingerprinting, fingerprint drift detection, and exit codes.
- AGT already contained `MCPSecurityScanner.scan_tool()`, `MCPSecurityScanner.scan_server()`, `MCPThreatType`, `MCPSeverity`, and fingerprint/rug-pull helpers in `agent-governance-python/agent-os/src/agent_os/mcp_security.py`.

Interpretation:

- The defect was not a single isolated bug. It was a contract drift: documentation promised a user journey and scanner behavior that the package, CLI, and active tests did not substantiate.
- The least disruptive repair path was to connect the CLI to AGT's existing scanner rather than invent a new scanner in parallel.

## Methodology

This paper is a research-style transformation of the AGT case study into a ProjectOpenHandMonk analysis document. The method was document-centered and evidence-mapped:

1. Read the primary AGT case study at `/home/sealjitha/projects/agent-governance-toolkit/docs/tutorials/27-mcp-scan-cli-case-study.md`.
2. Consult ProjectOpenHandMonk context artifacts for narrative posture and MCP trust-boundary framing:
   - `docs/EVILBENCH_RESEARCH_REPORT.md`
   - `docs/MIRA_DOCUMENTATION_KICKOFF.md`
   - `docs/HERMES_KLIVE_E2E_SUMMARY_FOR_MIRA.md`
3. Extract observed facts from the AGT case study separately from interpretation.
4. Reframe the case study as ProjectOpenHandMonk research/analysis of an open-source contribution repair, not as AGT user documentation.
5. Preserve narrow evidence boundaries: metadata inspection, regression tests, saved evaluation artifacts, and explicit limitations.

No AGT files were modified for this writing pass. No new AGT tests were run during this writing pass. Claims about test outcomes and evaluation counts are therefore cited as reported by the AGT case study, not as independently re-executed results in this document.

## Implementation Findings

### 1. Packaged CLI entry point restored the documented command shape

Observed fact:

The AGT case study reports that the repair added a direct console script:

```toml
[project.scripts]
agent-os = "agent_os.cli:main"
mcp-scan = "agent_os.cli.mcp_scan:main"
```

Interpretation:

This change matters because it makes the command users are instructed to run discoverable as a packaged entry point. It also avoids coupling this focused scanner to unrelated `agent-os` router imports that may fail before help text is displayed.

Evidence boundary:

This supports the claim that the CLI command contract was repaired. It does not, by itself, support any claim about scanner accuracy.

### 2. The CLI became a metadata-only MCP inspection client

Observed fact:

The source artifact reports that the repaired CLI performs metadata-only live inspection using the MCP 2025-11-25 lifecycle:

1. For stdio, launch the configured server with `subprocess.Popen([command, *args], shell=False)` and a sanitized child environment.
2. For Streamable HTTP, send JSON-RPC POST requests to the configured MCP endpoint with `Mcp-Protocol-Version: 2025-11-25`, accepting JSON or `text/event-stream` responses.
3. For legacy HTTP+SSE, open the SSE stream, read the server's message endpoint event, and POST JSON-RPC requests to that endpoint.
4. Send `initialize` with `protocolVersion: "2025-11-25"`.
5. Send `notifications/initialized`.
6. Send `tools/list`, `resources/list`, `resources/templates/list`, and `prompts/list` when the server advertises corresponding capabilities, following `nextCursor` pagination if present.
7. Normalize each discovered primitive into scanner-visible `{name, description, inputSchema}` metadata while preserving primitive prefixes such as `resource:`, `resource_template:`, and `prompt:`.
8. Close the process, HTTP stream, or SSE connection after inspection.

Interpretation:

The key repair was not merely adding a command wrapper. It changed the scanner's evidence source from local launch/configuration metadata to advertised MCP primitive metadata, while still keeping the scan metadata-only. That distinction is important: the scanner enumerates metadata; it does not execute tools, read resources, or render prompts.

Evidence boundary:

This supports a claim about primitive metadata enumeration. It does not support a claim that runtime tool behavior is safe or that remote server authentication posture is validated.

### 3. Existing AGT scanner logic was reused instead of replaced

Observed fact:

The source artifact states that the repaired CLI feeds normalized discovered metadata into AGT's existing `MCPSecurityScanner`, including `MCPSecurityScanner.scan_server()`.

Interpretation:

This is a scoped contribution strategy. Reusing `agent-governance-python/agent-os/src/agent_os/mcp_security.py` keeps the change focused on CLI inspection and contract repair rather than creating a second detection engine with separate semantics.

Evidence boundary:

This supports scanner-integration claims only to the extent that `MCPSecurityScanner` already covers the relevant metadata patterns. It does not imply comprehensive MCP threat detection.

### 4. Static mode preserved a safer review path for untrusted configs

Observed fact:

The source artifact reports a `--static-only` mode:

```bash
mcp-scan scan mcp-config.json --static-only
```

It also states that static mode scans inline tool arrays and launch metadata already present in the config, while avoiding command execution and network connections.

Interpretation:

This is an important safety distinction. Live inspection intentionally executes configured local commands or connects to endpoints in order to enumerate advertised primitives. Static-only mode is therefore better suited for CI jobs reviewing untrusted repository-supplied configs.

Evidence boundary:

Static-only mode should not be represented as equivalent to live inspection. It intentionally gives up live primitive enumeration in exchange for lower side-effect risk.

### 5. Fingerprinting shifted to normalized primitive metadata

Observed fact:

The source artifact reports that fingerprinting changed from a simulated command/args hash to per-primitive SHA-256 hashes over normalized scanner-visible description and schema. For non-tool primitives, resources, resource templates, and prompts are normalized into the existing scanner-visible shape. The compare path reports changed descriptions, changed schemas, new metadata entries, and removed metadata entries.

Interpretation:

This aligns fingerprinting with MCP metadata rug-pull concerns: changes in descriptions or schemas are often more relevant to metadata poisoning than changes in process launch arguments alone.

Evidence boundary:

This supports drift detection over normalized primitive metadata. It does not prove that all malicious semantic changes are detectable by hashing description/schema fields.

### 6. Exit codes became CI-relevant for critical outcomes

Observed fact:

The source artifact reports these exit-code meanings:

| Exit code | Meaning |
|---|---|
| 0 | Success, no critical scan findings / no fingerprint drift |
| 1 | Config, usage, or file error |
| 2 | Critical scan findings, critical config/inspection findings, or fingerprint drift |

It also reports stable JSON output fields: `servers`, `summary`, `config_findings`, `inspection_errors`, and `inspections`.

Interpretation:

The repair made the CLI more suitable for automation by distinguishing ordinary usage/config errors from security-relevant critical findings and fingerprint drift.

Evidence boundary:

A deterministic exit code is automation evidence, not a guarantee that every dangerous MCP condition is detected.

### 7. Documentation was rewritten around tested behavior

Observed fact:

The source artifact states that Tutorial 27 was rewritten around the packaged `mcp-scan` command and now explains live stdio inspection, sanitized child environments, fail-closed inspection failures, `--static-only`, CI use, remote transport behavior, MCP Inspector's role, `MCPSecurityScanner` findings, fingerprinting, and exit code 2 for critical primitive metadata/config/inspection findings or fingerprint drift.

Interpretation:

The documentation repair is part of the engineering repair. For security tooling, a tutorial that overclaims behavior can be as harmful as a missing feature because it shapes user expectations and CI assumptions.

Evidence boundary:

This paper does not reproduce AGT's tutorial as upstream documentation. It analyzes the tutorial repair as an artifact of the contribution.

## Evaluation

### Regression-test restoration

Observed fact:

The AGT case study reports that before the fix, the CLI regression target produced:

```text
collected 0 items / 1 skipped
```

After the repair, `tests/test_mcp_scan_cli.py` was no longer a module-level skip and contained active pytest coverage for config loading, parsing, static scanning, output formatting, fingerprint comparison, CLI exit codes, live stdio fake-server inspection, and hardening regressions.

Interpretation:

Restoring tests converts the desired CLI contract from dormant specification into executable regression evidence.

### Fake-server evidence for live stdio inspection

Observed fact:

The source artifact reports fake stdio MCP server tests that read JSON-RPC messages from stdin and respond to the handshake and list methods used by the CLI:

- `initialize`
- `notifications/initialized`
- `tools/list`
- `resources/list`
- `resources/templates/list`
- `prompts/list`

The cited tests include:

- `test_inspect_stdio_server_lists_tools`
- `test_run_security_scan_inspects_live_stdio_and_uses_mcp_security`

The second test configures a fake server whose primitive metadata contains hidden comments and exfiltration language, then asserts that the scan records live inspection, scans four discovered metadata entries, and reports critical scanner findings including the hidden-comment finding.

Interpretation:

These tests are strong evidence for the repaired stdio user journey at the regression level: config -> MCP client inspection -> primitive enumeration -> scanner findings -> CI-relevant exit code.

Evidence boundary:

A fake-server regression test is not equivalent to broad live ecosystem testing. It validates the intended protocol path under controlled conditions.

### Transport and protocol coverage

Observed fact:

The AGT case study reports additional tests for:

- MCP 2025-11-25 protocol version negotiation and initialized notification ordering.
- Stdio primitive-list flows.
- Streamable HTTP POST JSON-RPC, JSON responses, SSE POST responses, request-id filtering, protocol headers, and session-id reuse.
- Fail-closed behavior for mismatched protocol versions, missing inspectable capabilities, and malformed remote headers.
- Legacy HTTP+SSE endpoint discovery, POST delivery, SSE response reading, URL-only fallback on 405, and primitive enumeration.
- Static-only remote safety, including no network request in static-only mode.
- Remote transport scan tests that normalize tools, resources, resource templates, and prompts into `MCPSecurityScanner` input.

Interpretation:

The repair expanded the CLI from a local static checker into a transport-aware metadata enumerator across the transport families named in the source artifact.

Evidence boundary:

This should be cited as regression coverage reported by the AGT case study. It should not be generalized to every server implementation, every deployment, or every protocol edge case.

### Hardening evidence

Observed fact:

The source artifact reports post-review hardening tests for:

- Not inheriting a parent-only secret variable into launched fake MCP servers.
- Treating failed live inspection as a critical inspection finding.
- Returning the critical-finding exit code for failed inspection.
- Returning the critical-finding exit code for critical launch/config findings.
- Avoiding creation of a trusted fingerprint baseline when live inspection fails.

Interpretation:

These hardening points are significant because live inspection carries operational risk: it launches configured processes or contacts remote endpoints. The repair does not eliminate that risk, but it adds conservative failure behavior and documents a static-only alternative.

### Evil MCP 30-case evaluation loop

Observed fact:

The AGT case study reports a deterministic evaluation script at `.hermes/scripts/run_evil_mcp_eval.py` and saved raw artifact `.hermes/evals/evil-mcp-30-loop.json`. It reports a run generated at `2026-04-30T13:18:05Z` on Python 3.12.3 with:

| Metric | Value |
|---|---:|
| Cases requested | 30 |
| Cases skipped | 0 |
| Cases with at least one finding | 30 |
| Cases with critical findings | 28 |
| Total scanner findings | 60 |
| Critical scanner findings | 53 |
| Warning scanner findings | 7 |

It also reports that Klive re-ran the loop and recorded a PASS review in `.hermes/evals/klive-evil-mcp-30-loop-review.md`, with deterministic aggregate results across consecutive runs and a warning that the artifact is safe to cite only with qualifications.

Interpretation:

This evaluation supports a narrow claim: the repaired scanner detected the tested metadata-poisoning fixtures across tools and non-tool primitives. It does not support claims about full OWASP MCP Top 10 coverage, false-positive rate, runtime prevention, or all possible MCP attack patterns.

## Limitations

1. This paper is a document transformation and analysis, not an independent re-execution of the AGT test suite.
2. Claims about AGT implementation behavior are grounded in the AGT case study, not direct source-code diffs reproduced here.
3. The repair concerns metadata enumeration and scanner integration. It does not execute tools, read resources, render prompts, validate authentication posture, or prove that a remote MCP server is benign.
4. Non-tool primitives are normalized into an existing tool-shaped scanner-visible representation. That is a pragmatic compatibility strategy, but it is not equivalent to a full semantic validator for resources, resource templates, or prompts.
5. Static-only mode and live mode have different evidence properties. Static-only mode avoids command execution and network connections but cannot enumerate live advertised primitives.
6. The reported 30-case loop demonstrates detection over tested metadata-poisoning fixtures. It does not measure false-positive rate and does not prove coverage for every OWASP MCP Top 10 category.
7. This document is ProjectOpenHandMonk research/analysis. It is not an AGT tutorial and should not be treated as content to upstream into AGT without separate maintainer review.

## Conclusion

The AGT `mcp-scan` repair is best understood as a security-tooling alignment case study. The reported contribution repaired a drifted contract between documentation, package entry points, CLI behavior, scanner integration, and tests. The resulting workflow is narrower and stronger than the baseline: users can invoke a packaged `mcp-scan` command, choose live or static inspection, enumerate advertised MCP primitive metadata when live inspection is used, feed normalized metadata into `MCPSecurityScanner`, obtain CI-relevant exit codes, and compare metadata fingerprints for drift.

The strongest supportable claim is not that AGT now provides general MCP safety or exhaustive OWASP coverage. The strongest claim is that a misleading static/config-only scanner journey was repaired into a bounded, test-backed MCP metadata inspection workflow. That claim is useful for ProjectOpenHandMonk because it shows how benchmark-driven MCP security concerns can translate into concrete open-source tooling repairs while still preserving honest limitations.

## Evidence Matrix

| Evidence ID | Claim | Evidence artifact | Observed fact | Interpretation / boundary |
|---|---|---|---|---|
| E-001 | The baseline tutorial/CLI contract had drifted. | `/home/sealjitha/projects/agent-governance-toolkit/docs/tutorials/27-mcp-scan-cli-case-study.md` | Tutorial referenced an `agentos mcp-scan` journey; package metadata exposed only `agent-os`; router did not contain `mcp-scan`; standalone module was not the documented path. | Supports contract-drift claim; does not evaluate scanner accuracy. |
| E-002 | Baseline regression coverage was dormant. | AGT: `agent-governance-python/agent-os/tests/test_mcp_scan_cli.py` as described in the source artifact | Baseline pytest result reported `collected 0 items / 1 skipped`. | Supports claim that desired behavior was encoded but not active. |
| E-003 | Old CLI scanned launch/config metadata rather than advertised MCP primitives. | AGT: `agent-governance-python/agent-os/src/agent_os/cli/mcp_scan.py` as described in the source artifact | Old `scan_config()` checked environment key names, `sudo`, `/tmp`, and suspicious paths; it did not inspect primitive list methods or call `MCPSecurityScanner.scan_server()`. | Supports distinction between config scanning and MCP metadata enumeration. |
| E-004 | AGT already contained a detection engine. | AGT: `agent-governance-python/agent-os/src/agent_os/mcp_security.py` as described in the source artifact | `MCPSecurityScanner.scan_tool()`, `scan_server()`, severity/threat types, and fingerprint/rug-pull helpers existed. | Supports scoped repair strategy: wire CLI to existing scanner rather than inventing a parallel scanner. |
| E-005 | Packaged command was repaired. | AGT package metadata as quoted in the source artifact | `mcp-scan = "agent_os.cli.mcp_scan:main"` was added under `[project.scripts]`. | Supports install/discoverability claim for the CLI command. |
| E-006 | Live metadata inspection was implemented. | Source artifact implementation section | Repair sends `initialize`, `notifications/initialized`, and advertised primitive list calls for tools, resources, resource templates, and prompts. | Supports primitive-enumeration claim; not a runtime execution/prevention claim. |
| E-007 | Stdio inspection includes process-safety hardening. | Source artifact implementation and validation sections | Stdio servers launch with `shell=False` and a sanitized child environment; tests verify parent-only secret variables are not inherited. | Supports reduced exposure claim; does not make launching untrusted commands risk-free. |
| E-008 | Static-only mode avoids live side effects. | Source artifact static mode and transport validation sections | `--static-only` scans config-present metadata and avoids command execution/network connections; test asserts remote configs are not contacted. | Supports safer CI review path for untrusted config changes; static mode has less evidence than live inspection. |
| E-009 | Fingerprinting shifted to primitive metadata. | Source artifact fingerprinting section | SHA-256 hashes are computed over normalized scanner-visible description and schema; compare reports changed/new/removed metadata entries. | Supports rug-pull/drift workflow over metadata; not full semantic change detection. |
| E-010 | CI-relevant exit codes were defined. | Source artifact output and exit-code section | Exit code 2 covers critical scan findings, critical config/inspection findings, or fingerprint drift. | Supports automation claim; not a detection-completeness claim. |
| E-011 | Regression tests cover fake stdio MCP inspection. | AGT: `agent-governance-python/agent-os/tests/test_mcp_scan_cli.py` as described in the source artifact | Tests include `test_inspect_stdio_server_lists_tools` and `test_run_security_scan_inspects_live_stdio_and_uses_mcp_security`. | Supports controlled end-to-end regression path from config to scanner findings. |
| E-012 | HTTP-family transport behavior was regression-tested. | AGT: `agent-governance-python/agent-os/tests/test_mcp_scan_cli.py` as described in the source artifact | Tests cover Streamable HTTP and legacy HTTP+SSE request/response flows, headers, session reuse, endpoint discovery, fallback, and primitive enumeration. | Supports transport-aware metadata inspection within tested cases only. |
| E-013 | Inspection failures fail closed. | Source artifact hardening tests | Failed live inspection becomes a critical inspection finding and returns the critical-finding exit code; failed fingerprint inspection does not save a baseline. | Supports conservative failure behavior. |
| E-014 | 30-case evaluation detected tested metadata-poisoning fixtures. | AGT: `.hermes/evals/evil-mcp-30-loop.json` and `.hermes/evals/klive-evil-mcp-30-loop-review.md` as reported in the source artifact | 30 requested, 0 skipped, 30 with findings, 28 with critical findings, 60 total findings. | Supports narrow tested-fixture detection claim; not OWASP certification, false-positive measurement, or runtime prevention. |
| E-015 | ProjectOpenHandMonk context motivates metadata inspection. | `docs/EVILBENCH_RESEARCH_REPORT.md`; `docs/HERMES_KLIVE_E2E_SUMMARY_FOR_MIRA.md` | EvilBench documentation frames hostile tool metadata and hostile tool outputs as MCP trust-boundary surfaces. | Supports relevance of the AGT repair to `mcp-security-bench`; does not import EvilBench client-safety claims into AGT. |
