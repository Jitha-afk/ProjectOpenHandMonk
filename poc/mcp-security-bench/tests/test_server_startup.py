from __future__ import annotations

from types import SimpleNamespace

import pytest

from evil_server import callback_server as callback_server_module
from evil_server import server as server_module


class DummyMCP:
    def __init__(self) -> None:
        self.transport: str | None = None

    def run(self, transport: str) -> None:
        self.transport = transport


class TestServerStartup:
    @pytest.fixture(autouse=True)
    def _isolate_artifacts(self, monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
        monkeypatch.setenv("EVIL_MCP_ARTIFACTS_DIR", str(tmp_path / "artifacts"))

    def test_parse_args_defaults_enable_callback_server(self) -> None:
        args = server_module.parse_args([])

        assert args.transport == "stdio"
        assert args.callback_port == 8080
        assert args.no_callback is False

    def test_main_starts_callback_server_by_default(self, monkeypatch: pytest.MonkeyPatch) -> None:
        started: dict[str, object] = {}
        dummy_mcp = DummyMCP()

        monkeypatch.delenv("EVIL_WEBHOOK_URL", raising=False)
        monkeypatch.setattr(
            server_module,
            "AttackConfig",
            SimpleNamespace(from_env=lambda: "config"),
        )
        monkeypatch.setattr(
            server_module,
            "create_server",
            lambda config, host, port: dummy_mcp,
        )
        monkeypatch.setattr(
            callback_server_module,
            "start_callback_server",
            lambda host, port, background=True: started.update(
                {"host": host, "port": port, "background": background}
            ),
        )

        server_module.main([])

        assert started == {"host": "0.0.0.0", "port": 8080, "background": True}
        assert dummy_mcp.transport == "stdio"
        assert server_module.os.environ["EVIL_WEBHOOK_URL"] == "http://127.0.0.1:8080/callback"

    def test_main_sets_default_webhook_url_for_custom_callback_port(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        dummy_mcp = DummyMCP()

        monkeypatch.delenv("EVIL_WEBHOOK_URL", raising=False)
        monkeypatch.setattr(
            server_module,
            "AttackConfig",
            SimpleNamespace(from_env=lambda: "config"),
        )
        monkeypatch.setattr(
            server_module,
            "create_server",
            lambda config, host, port: dummy_mcp,
        )
        monkeypatch.setattr(
            callback_server_module,
            "start_callback_server",
            lambda host, port, background=True: None,
        )

        server_module.main(["--host", "127.0.0.1", "--callback-port", "18080"])

        assert server_module.os.environ["EVIL_WEBHOOK_URL"] == "http://127.0.0.1:18080/callback"
        assert dummy_mcp.transport == "stdio"

    def test_main_preserves_existing_webhook_url(self, monkeypatch: pytest.MonkeyPatch) -> None:
        dummy_mcp = DummyMCP()

        monkeypatch.setenv("EVIL_WEBHOOK_URL", "http://collector.example/callback")
        monkeypatch.setattr(
            server_module,
            "AttackConfig",
            SimpleNamespace(from_env=lambda: "config"),
        )
        monkeypatch.setattr(
            server_module,
            "create_server",
            lambda config, host, port: dummy_mcp,
        )
        monkeypatch.setattr(
            callback_server_module,
            "start_callback_server",
            lambda host, port, background=True: None,
        )

        server_module.main([])

        assert server_module.os.environ["EVIL_WEBHOOK_URL"] == "http://collector.example/callback"
        assert dummy_mcp.transport == "stdio"

    def test_main_continues_when_callback_port_is_unavailable(
        self,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        dummy_mcp = DummyMCP()

        monkeypatch.delenv("EVIL_WEBHOOK_URL", raising=False)
        monkeypatch.setattr(
            server_module,
            "AttackConfig",
            SimpleNamespace(from_env=lambda: "config"),
        )
        monkeypatch.setattr(
            server_module,
            "create_server",
            lambda config, host, port: dummy_mcp,
        )

        def _raise_port_in_use(host: str, port: int, background: bool = True) -> None:
            raise OSError(98, "Address already in use")

        monkeypatch.setattr(
            callback_server_module,
            "start_callback_server",
            _raise_port_in_use,
        )

        server_module.main([])

        captured = capsys.readouterr()
        assert "Callback server unavailable" in captured.err
        assert dummy_mcp.transport == "stdio"

    def test_main_skips_callback_server_when_disabled(self, monkeypatch: pytest.MonkeyPatch) -> None:
        started = False
        dummy_mcp = DummyMCP()

        monkeypatch.delenv("EVIL_WEBHOOK_URL", raising=False)
        monkeypatch.setattr(
            server_module,
            "AttackConfig",
            SimpleNamespace(from_env=lambda: "config"),
        )
        monkeypatch.setattr(
            server_module,
            "create_server",
            lambda config, host, port: dummy_mcp,
        )

        def _start_callback_server(host: str, port: int, background: bool = True) -> None:
            nonlocal started
            started = True

        monkeypatch.setattr(
            callback_server_module,
            "start_callback_server",
            _start_callback_server,
        )

        server_module.main(["--no-callback"])

        assert started is False
        assert "EVIL_WEBHOOK_URL" not in server_module.os.environ
        assert dummy_mcp.transport == "stdio"
