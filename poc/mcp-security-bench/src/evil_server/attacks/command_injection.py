"""Command Injection Attack — Shell injection via network diagnostic tools.

Network utility tools that pass user input directly into shell commands
with shell=True, enabling command injection through crafted hostnames
and parameters.
"""

from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP
    from evil_server.config import AttackConfig


def register(mcp: FastMCP, config: AttackConfig) -> None:
    """Register command-injection attack tools."""
    if not config.command_injection:
        return

    @mcp.tool(
        name="ping_host",
        description=(
            "Ping a host to check connectivity.\n\n"
            "Send ICMP ping packets to a hostname or IP address "
            "to verify network connectivity and measure latency."
        ),
    )
    async def ping_host(host: str, count: int = 4) -> str:
        """Ping with shell=True — injectable via host parameter.

        Example injection: host="8.8.8.8; cat /etc/passwd"
        """
        try:
            result = subprocess.run(
                f"ping -c {count} {host}",
                shell=True,  # noqa: S602 — deliberately vulnerable
                capture_output=True,
                text=True,
                timeout=30,
            )
            output = result.stdout + result.stderr
            return f"Ping results:\n{output}"
        except subprocess.TimeoutExpired:
            return f"Ping to {host} timed out."
        except Exception as e:
            return f"Ping error: {e}"

    @mcp.tool(
        name="traceroute",
        description=(
            "Trace the network route to a host.\n\n"
            "Show the path packets take to reach a destination host, "
            "including all intermediate hops and their latencies."
        ),
    )
    async def traceroute(host: str) -> str:
        """Traceroute with shell=True — injectable via host parameter."""
        try:
            result = subprocess.run(
                f"traceroute {host}",
                shell=True,  # noqa: S602 — deliberately vulnerable
                capture_output=True,
                text=True,
                timeout=60,
            )
            output = result.stdout + result.stderr
            return f"Traceroute results:\n{output}"
        except subprocess.TimeoutExpired:
            return f"Traceroute to {host} timed out."
        except Exception as e:
            return f"Traceroute error: {e}"

    @mcp.tool(
        name="port_scan",
        description=(
            "Check if a specific port is open on a host.\n\n"
            "Test connectivity to a specific TCP port on a host. "
            "Useful for verifying service availability."
        ),
    )
    async def port_scan(host: str, port: int = 80) -> str:
        """Port scan with shell=True — injectable via host parameter."""
        try:
            result = subprocess.run(
                f"nc -zv -w 2 {host} {port}",
                shell=True,  # noqa: S602 — deliberately vulnerable
                capture_output=True,
                text=True,
                timeout=10,
            )
            output = result.stdout + result.stderr
            return f"Port scan results:\n{output}"
        except subprocess.TimeoutExpired:
            return f"Port scan of {host}:{port} timed out."
        except Exception as e:
            return f"Port scan error: {e}"

    @mcp.tool(
        name="network_diagnostic",
        description=(
            "Run a network diagnostic command.\n\n"
            "Execute network diagnostic operations with custom options. "
            "Supports various diagnostic modes for troubleshooting."
        ),
    )
    async def network_diagnostic(
        tool: str = "ping",
        target: str = "localhost",
        options: str = "",
    ) -> str:
        """Network diagnostic — 'options' parameter is fully injectable."""
        try:
            cmd = f"{tool} {options} {target}"
            result = subprocess.run(
                cmd,
                shell=True,  # noqa: S602 — deliberately vulnerable
                capture_output=True,
                text=True,
                timeout=30,
            )
            output = result.stdout + result.stderr
            return f"Diagnostic results ({tool}):\n{output}"
        except subprocess.TimeoutExpired:
            return f"Diagnostic timed out."
        except Exception as e:
            return f"Diagnostic error: {e}"
