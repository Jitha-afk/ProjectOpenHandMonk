# Source Memo: Microsoft MCP Security Pages

Purpose: concise extraction of reusable content updates from Microsoft’s MCP Azure security guidance. This memo is for deck/paper revision planning, not final talk copy.

## Reusable takeaways

- Microsoft frames MCP as a platform-security problem, not just a protocol feature: the reference architecture emphasizes trust boundaries, identity and gateway enforcement, private execution, data access controls, and centralized telemetry.
- The architecture guidance is explicitly layered. The source is clear that no single safeguard is enough; the message is defense in depth across identity, network isolation, execution environment, and monitoring.
- A strong design principle from the development page: optimize tools for agent success rather than endpoint completeness. For enterprise teams, that means exposing business tasks and workflows instead of mirroring every backend operation.
- The source warns that auto-generating one tool per REST endpoint is a common failure mode because too many granular tools increase reasoning burden and reduce reliability.
- The five design guidelines are presentation-ready: limit tool count, use task-focused naming, return decision-ready data, enforce guardrails server-side, and write clear descriptions.
- The schema guidance is more operational than many MCP explainers: every tool needs a valid `inputSchema`, and simple, self-describing schemas are treated as part of the control surface because they influence how agents invoke tools.
- Output design is security-relevant as well as usability-relevant. The source strongly favors structured JSON or other extractable fields over prose or HTML because agents reason better with explicit fields than with text they must parse.
- Output schemas are optional but strategically useful: they give validation, type expectations, and better integration discipline for downstream clients and platform tooling.
- Error handling is split into two classes with different security meaning: recoverable tool-execution errors versus protocol/JSON-RPC errors. This is a useful distinction for both agent builders and platform operators.
- The error-message guidance is especially relevant for enterprise decks: be actionable without leaking internals. Keep stack traces, file paths, schemas, credentials, and detailed architecture server-side; return sanitized business-level failure reasons and next steps to the agent.
- Microsoft recommends adding sanitized request or correlation IDs to agent-facing failures so operations teams can debug without exposing sensitive detail. This is a practical bridge between security and operability.
- The testing model is unusually strong and directly reusable: MCP quality should be validated at three layers: unit tests for tool logic, protocol tests for MCP compliance, and agent tests for real-world LLM behavior.
- The testing strategy is also rollout-friendly: run unit and protocol tests on every commit, and use agent tests on pull requests or nightly runs because they are slower but validate actual discoverability, selection, and workflow success.
- The top-level Azure guidance is refreshingly honest about maturity by risk area: some OWASP MCP risks map to production-ready Azure controls, others still require custom work, and some remain emerging patterns. That coverage framing is valuable for enterprise architecture discussions.
- The home page’s closing message is useful for an executive audience: good MCP security is not separate from usability. Clear identity boundaries, strong isolation, telemetry, and automated guardrails make systems easier to operate and audit, not just harder to attack.

## Strong principles / phrases to adapt later

- Design for agent use, not API exhaustiveness.
- Govern tasks, not raw backend operations.
- Return data an agent can act on, not prose it has to interpret.
- Keep guardrails on the server side, not in hopeful prompt instructions.
- Make errors recoverable for the agent but non-revealing for the attacker.
- Test MCP in three layers: logic, protocol, agent behavior.
- Treat MCP security as layered architecture, not a single control.
- Security controls should improve operability and auditability, not just block attacks.

## Checklist ideas to incorporate

- Tool design checklist: owner, business task, tool count rationalization, task-focused name, clear description, server-side guardrails, rate limits/quotas, and naming collision review.
- Schema/output checklist: valid `inputSchema`, optional `outputSchema` where useful, structured outputs with extractable fields, and no HTML/prose-only responses for machine-consumed workflows.
- Error-handling checklist: separate recoverable tool errors from protocol errors, provide next-step guidance, sanitize sensitive details, and attach a safe request/correlation ID.
- Validation/testing checklist: unit tests for tool logic, protocol tests for MCP compliance, agent tests for tool selection/parameter extraction/error recovery, with commit/PR/nightly ownership defined.
- Architecture readiness checklist: map each OWASP MCP risk to current platform capability as mature, partial, or emerging so teams know where Azure services help and where custom controls are still required.

## Ways to improve our current deck/paper with this source

- Add one explicit section or slide on secure tool/interface design. Our current material is strong on incidents and governance, but Microsoft adds a missing build-time message: bad tool shape itself is a security and reliability risk.
- Add a concise MCP testing pyramid visual or subsection. The current deck/paper would benefit from Microsoft’s logic/protocol/agent test split because it gives platform teams a concrete rollout model.
- Add a short error-handling and information-disclosure segment. This would sharpen the operational story by showing how to support agent recovery without leaking internals.
- Add an Azure maturity/coverage framing for the OWASP MCP Top 10. This would help enterprise architects distinguish where platform-native controls are ready now versus where custom engineering or governance is still needed.

## Citations

- Microsoft. "Development Best Practices for MCP Servers." OWASP MCP Top 10 Security Guidance for Azure. https://microsoft.github.io/mcp-azure-security-guide/adoption/development-best-practices/
- Microsoft. "OWASP MCP Top 10 Security Guidance for Azure." https://microsoft.github.io/mcp-azure-security-guide/#owasp-mcp-top-10
