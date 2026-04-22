"""Attack configuration for the evil MCP server.

Controls which attack modules are enabled/disabled.
Reads from environment variables with EVIL_MCP_ prefix.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class AttackConfig:
    """Configuration controlling which attack categories are active."""

    tool_poisoning: bool = True
    tool_shadowing: bool = True
    rug_pull: bool = True
    data_exfil: bool = True
    prompt_injection: bool = True
    credential_theft: bool = True
    excessive_perms: bool = True
    code_execution: bool = True
    command_injection: bool = True
    sandbox_escape: bool = True
    cross_server: bool = True
    honeypots: bool = True

    @classmethod
    def all_enabled(cls) -> AttackConfig:
        """Return config with all attacks enabled."""
        return cls()

    @classmethod
    def all_disabled(cls) -> AttackConfig:
        """Return config with all attacks disabled."""
        return cls(
            tool_poisoning=False,
            tool_shadowing=False,
            rug_pull=False,
            data_exfil=False,
            prompt_injection=False,
            credential_theft=False,
            excessive_perms=False,
            code_execution=False,
            command_injection=False,
            sandbox_escape=False,
            cross_server=False,
            honeypots=False,
        )

    @classmethod
    def from_env(cls) -> AttackConfig:
        """Load configuration from environment variables.

        Environment variables use the EVIL_MCP_ prefix:
            EVIL_MCP_TOOL_POISONING=true|false
            EVIL_MCP_TOOL_SHADOWING=true|false
            ...etc
        """

        def _parse_bool(key: str, default: bool = True) -> bool:
            val = os.environ.get(f"EVIL_MCP_{key.upper()}", "")
            if not val:
                return default
            return val.lower() in ("true", "1", "yes", "on")

        return cls(
            tool_poisoning=_parse_bool("TOOL_POISONING"),
            tool_shadowing=_parse_bool("TOOL_SHADOWING"),
            rug_pull=_parse_bool("RUG_PULL"),
            data_exfil=_parse_bool("DATA_EXFIL"),
            prompt_injection=_parse_bool("PROMPT_INJECTION"),
            credential_theft=_parse_bool("CREDENTIAL_THEFT"),
            excessive_perms=_parse_bool("EXCESSIVE_PERMS"),
            code_execution=_parse_bool("CODE_EXECUTION"),
            command_injection=_parse_bool("COMMAND_INJECTION"),
            sandbox_escape=_parse_bool("SANDBOX_ESCAPE"),
            cross_server=_parse_bool("CROSS_SERVER"),
            honeypots=_parse_bool("HONEYPOTS"),
        )
