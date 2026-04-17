"""Command Injection Attack — Shell injection via network diagnostic tools.

Network utility tools that pass user input directly into shell commands
with shell=True, enabling command injection through crafted hostnames
and parameters.
"""

from __future__ import annotations

import platform
import subprocess
from typing import TYPE_CHECKING

from evil_server.demo_artifacts import log_event

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP
    from evil_server.config import AttackConfig


def _is_windows() -> bool:
    return platform.system().lower().startswith("win")


def _build_ping_command(host: str, count: int = 4) -> str:
    count_flag = "-n" if _is_windows() else "-c"
    return f"ping {count_flag} {count} {host}"


def _build_traceroute_command(host: str) -> str:
    command = "tracert" if _is_windows() else "traceroute"
    return f"{command} {host}"


def _build_dns_lookup_command(host: str) -> str:
    return f"nslookup {host}"


def _suspicious(value: str) -> bool:
    return any(token in value for token in [";", "&&", "||", "|", "&", ">", "<"])


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

        Example injection: host=\"8.8.8.8; cat /etc/passwd\"
        """
        try:
            command = _build_ping_command(host, count)
            result = subprocess.run(
                command,
                shell=True,  # noqa: S602 — deliberately vulnerable
                capture_output=True,
                text=True,
                timeout=30,
            )
            if _suspicious(host):
                log_event("command_injection_attempt", tool="ping_host", command=command)
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
            command = _build_traceroute_command(host)
            result = subprocess.run(
                command,
                shell=True,  # noqa: S602 — deliberately vulnerable
                capture_output=True,
                text=True,
                timeout=60,
            )
            if _suspicious(host):
                log_event("command_injection_attempt", tool="traceroute", command=command)
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
            if _suspicious(host):
                log_event("command_injection_attempt", tool="port_scan", command=f"nc -zv -w 2 {host} {port}")
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
            if _suspicious(tool) or _suspicious(target) or _suspicious(options):
                log_event("command_injection_attempt", tool="network_diagnostic", command=cmd)
            output = result.stdout + result.stderr
            return f"Diagnostic results ({tool}):\n{output}"
        except subprocess.TimeoutExpired:
            return f"Diagnostic timed out."
        except Exception as e:
            return f"Diagnostic error: {e}"

    @mcp.tool(
        name="dns_lookup",
        description=(
            "Look up DNS records for a host.\n\n"
            "Resolve a hostname using the platform DNS utility. This alias exists "
            "to keep older demo scripts and guidance working."
        ),
    )
    async def dns_lookup(host: str) -> str:
        """Compatibility alias for Windows-friendly DNS lookup demos."""
        try:
            command = _build_dns_lookup_command(host)
            result = subprocess.run(
                command,
                shell=True,  # noqa: S602 — deliberately vulnerable
                capture_output=True,
                text=True,
                timeout=30,
            )
            if _suspicious(host):
                log_event("command_injection_attempt", tool="dns_lookup", command=command)
            output = result.stdout + result.stderr
            return f"DNS lookup results:\n{output}"
        except subprocess.TimeoutExpired:
            return f"DNS lookup for {host} timed out."
        except Exception as e:
            return f"DNS lookup error: {e}"
