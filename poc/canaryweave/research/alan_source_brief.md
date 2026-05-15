# Alan source brief: source paper MCP protocol-safety evaluation

Scope: source-grounded research brief for a controlled, non-harmful CanaryWeave implementation inspired by a local MCP security paper. This brief is for project folder `poc/canaryweave`.

Safety boundary: do not reproduce raw attack payloads, real exfiltration paths, credential strings, operational malware/abuse instructions, or source-paper adversarial examples. Use benign canaries and inert local actions only.

## Source and evidence boundary

Primary source: local extracted text from the paper PDF. The project retains only high-level source facts. The external benchmark artifact, raw scenario corpus, seeds, classifier code, adapters, and raw logs are not available locally.

Therefore CanaryWeave should claim only controlled reproducibility of the measurement shape, not exact reproduction of reported paper-scale numbers.

## Claims to model safely

The source paper claims three protocol-level MCP weaknesses:

1. No capability attestation.
2. Bidirectional sampling without origin authentication.
3. Implicit trust propagation in multi-server configurations.

It also describes an evaluation over 847 scenarios with benchmark adaptations from InjecAgent and AgentDojo plus novel sampling and cross-server cases. Reported values in the source paper should be treated as contextual targets only, not reproduced findings, unless original artifacts are released.

## Safe benchmark construction

CanaryWeave should preserve the following structure:

- matched direct-function baseline, MCP-like unprotected mode, and attested/protected mode;
- JSON-RPC-shaped local event traces;
- benign `CANARY_*` values as synthetic protected data;
- inert symbolic actions instead of real send, transfer, delete, credential, shell, or network effects;
- scenario metadata that records source family, adapter, digest, record counts, category labels, and trust-failure class;
- deterministic trace parsing for ASR-style metrics.

## Source-paper methodology elements to reference

- Injection surfaces: resource content, tool response payloads, and sampling request prompts.
- Measurement infrastructure: instrumented client traces with JSON-RPC-shaped events.
- Controlled variables: matched semantics between direct baseline and MCP-like mode.
- Main result categories: resource injection, tool-response manipulation, cross-server propagation, and sampling-based injection.
- Mitigation direction: capability attestation, message authentication, origin tagging, isolation enforcement, and replay protection.

## Missing artifacts

The local source text does not provide:

1. original benchmark source code;
2. raw payload corpus;
3. exact scenario adaptation rules;
4. host/client implementation and instrumentation schema;
5. custom adversarial server details;
6. surveyed server-installation-guide corpus;
7. model revision/configuration details;
8. raw traces or statistical scripts.

## Recommended safe scenario mix

Primary focus: sampling abuse.

- Sampling role/provenance confusion.
- Sampling-to-tool chain.
- Sampling-to-resource chain.
- Best-of-n or verifier-gap candidate selection.
- Self-consistency label drift.

Secondary focus:

- Capability attestation absence through unbound tool/action proposals.
- Implicit trust propagation through cross-context canary movement.

## Metrics

Use only deterministic metrics from local traces:

- unauthorized attempts;
- unauthorized executed;
- ASR-style rate;
- block rate;
- canary touch rate;
- amplification delta between MCP-like and direct baseline;
- protected-mode reduction relative to unprotected mode;
- grouped results by attack type, source family, and scenario family.

## Reporting guidance

Safe claim:

"CanaryWeave reconstructs a safe version of the protocol-safety measurement pattern using benign canaries, inert local actions, structural benchmark metadata, and deterministic trace parsing. It evaluates whether protocol-origin and capability boundaries are represented and enforced in a controlled harness."

Do not claim:

- exact reproduction of the source paper 847-scenario benchmark;
- reproduction of reported ASR percentages;
- use of raw adversarial payloads;
- real MCP host exploitation;
- live model/provider evaluation unless explicitly run later with safe provider controls.
