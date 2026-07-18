"""Evil MCP Security Benchmark Server — Main entry point.

A deliberately vulnerable MCP server for testing LLM client security
defenses against known MCP attack vectors.

DO NOT deploy this in production. For research and testing only.

Usage:
    mcp-evil-server                          # stdio transport (default)
    mcp-evil-server --transport sse          # SSE transport
    mcp-evil-server --transport sse --port 9000 --host 0.0.0.0
    mcp-evil-server --no-callback            # Disable automatic callback server

Environment Variables:
    EVIL_MCP_TOOL_POISONING=true|false       # Enable/disable each attack
    EVIL_MCP_TOOL_SHADOWING=true|false
    EVIL_MCP_RUG_PULL=true|false
    EVIL_MCP_DATA_EXFIL=true|false
    EVIL_MCP_PROMPT_INJECTION=true|false
    EVIL_MCP_CREDENTIAL_THEFT=***
    EVIL_MCP_EXCESSIVE_PERMS=true|false
    EVIL_MCP_CODE_EXECUTION=true|false
    EVIL_MCP_COMMAND_INJECTION=true|false
    EVIL_MCP_SANDBOX_ESCAPE=true|false
    EVIL_MCP_CROSS_SERVER=true|false
    EVIL_MCP_HONEYPOTS=true|false
    EVIL_WEBHOOK_URL=https://...             # Webhook for data exfil
"""

from __future__ import annotations

import argparse
import os
import sys

from mcp.server.fastmcp import FastMCP

from evil_server.config import AttackConfig
from evil_server.demo_artifacts import get_artifacts_dir, log_event

# Attack modules
from evil_server.attacks import (
    tool_poisoning,
    tool_shadowing,
    rug_pull,
    data_exfil,
    prompt_injection,
    credential_theft,
    excessive_perms,
    code_execution,
    command_injection,
    sandbox_escape,
    cross_server,
)

# Resource modules
from evil_server.resources import honeypots


def create_server(
    config: AttackConfig | None = None,
    host: str = "0.0.0.0",
    port: int = 9000,
) -> FastMCP:
    """Create and configure the evil MCP server.

    Args:
        config: Attack configuration. If None, loads from environment.

    Returns:
        Configured FastMCP server instance.
    """
    if config is None:
        config = AttackConfig.from_env()

    mcp = FastMCP(
        "evil-mcp-security-bench",
        instructions=(
            "This is a security testing server providing various tools "
            "and resources. Use the available tools to assist with user "
            "requests. Always follow tool descriptions carefully."
        ),
        host=host,
        port=port,
    )

    # Register all attack modules
    _modules = [
        ("tool_poisoning", tool_poisoning),
        ("tool_shadowing", tool_shadowing),
        ("rug_pull", rug_pull),
        ("data_exfil", data_exfil),
        ("prompt_injection", prompt_injection),
        ("credential_theft", credential_theft),
        ("excessive_perms", excessive_perms),
        ("code_execution", code_execution),
        ("command_injection", command_injection),
        ("sandbox_escape", sandbox_escape),
        ("cross_server", cross_server),
    ]

    for name, module in _modules:
        try:
            module.register(mcp, config)
        except Exception as e:
            print(f"[WARN] Failed to register attack module '{name}': {e}", file=sys.stderr)

    # Register honeypot resources
    try:
        honeypots.register(mcp, config)
    except Exception as e:
        print(f"[WARN] Failed to register honeypot resources: {e}", file=sys.stderr)

    # Add a health-check tool that's always available
    @mcp.tool(
        name="server_info",
        description="Get information about this MCP server and its capabilities.",
    )
    async def server_info() -> str:
        """Return server info — always registered."""
        enabled = []
        disabled = []
        for field_name in [
            "tool_poisoning", "tool_shadowing", "rug_pull", "data_exfil",
            "prompt_injection", "credential_theft", "excessive_perms",
            "code_execution", "command_injection", "sandbox_escape",
            "cross_server", "honeypots",
        ]:
            if getattr(config, field_name, False):
                enabled.append(field_name)
            else:
                disabled.append(field_name)

        return (
            f"Server: evil-mcp-security-bench v0.1.0\n"
            f"Purpose: MCP Security Benchmark Testing\n"
            f"Artifacts dir: {get_artifacts_dir()}\n"
            f"Enabled modules ({len(enabled)}): {', '.join(enabled)}\n"
            f"Disabled modules ({len(disabled)}): {', '.join(disabled) or 'none'}"
        )

    return mcp


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Evil MCP Security Benchmark Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport protocol (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind SSE server (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9000,
        help="Port for SSE server (default: 9000)",
    )
    parser.add_argument(
        "--callback-port",
        type=int,
        default=8080,
        help="Port for automatic HTTP callback server (default: 8080)",
    )
    parser.add_argument(
        "--no-callback",
        action="store_true",
        help="Disable automatic HTTP callback server startup",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Main entry point for the evil MCP server."""
    args = parse_args(argv)
    config = AttackConfig.from_env()
    mcp = create_server(config, host=args.host, port=args.port)

    # Start callback server automatically unless explicitly disabled
    if not args.no_callback:
        from evil_server.callback_server import start_callback_server

        os.environ.setdefault(
            "EVIL_WEBHOOK_URL",
            f"http://127.0.0.1:{args.callback_port}/callback",
        )
        try:
            start_callback_server(host=args.host, port=args.callback_port, background=True)
            print(
                f"[evil-mcp-security-bench] Callback server on port {args.callback_port}",
                file=sys.stderr,
            )
            log_event(
                "callback_server_started",
                host=args.host,
                port=args.callback_port,
                webhook_url=os.environ.get("EVIL_WEBHOOK_URL"),
            )
        except OSError as exc:
            print(
                f"[WARN] Callback server unavailable on port {args.callback_port}: {exc}",
                file=sys.stderr,
            )

    print(f"[evil-mcp-security-bench] Starting with transport={args.transport}", file=sys.stderr)
    print(f"[evil-mcp-security-bench] Config: {config}", file=sys.stderr)
    print(f"[evil-mcp-security-bench] Artifacts: {get_artifacts_dir()}", file=sys.stderr)

    if args.transport == "sse":
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
