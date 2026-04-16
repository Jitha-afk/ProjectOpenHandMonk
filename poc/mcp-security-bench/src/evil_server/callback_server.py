"""HTTP Callback Server for data exfiltration verification.

A simple HTTP server that logs incoming POST requests to a file,
enabling verification that data exfiltration attacks executed successfully.

Usage:
    python -m evil_server.callback_server            # standalone
    # Or started automatically via server.py --callback-port 8080
"""

from __future__ import annotations

import json
import os
import threading
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any


LOG_FILE = os.environ.get("CALLBACK_LOG_FILE", "callback_log.json")


def _read_log() -> list[dict[str, Any]]:
    """Read existing log entries."""
    try:
        with open(LOG_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _append_log(entry: dict[str, Any]) -> None:
    """Append an entry to the log file."""
    entries = _read_log()
    entries.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(entries, f, indent=2)


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the callback endpoint."""

    def log_message(self, format: str, *args: Any) -> None:
        """Suppress default stderr logging."""
        pass

    def do_POST(self) -> None:
        if self.path == "/callback":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8", errors="replace")

            try:
                body_json = json.loads(body)
            except json.JSONDecodeError:
                body_json = {"raw": body}

            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source_ip": self.client_address[0],
                "headers": dict(self.headers),
                "body": body_json,
            }

            _append_log(entry)
            print(f"[callback] Received POST from {self.client_address[0]}: {json.dumps(body_json)[:200]}")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self) -> None:
        if self.path == "/callback/log":
            entries = _read_log()
            # Return last 50 entries
            recent = entries[-50:]

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(recent, indent=2).encode())
        else:
            self.send_response(404)
            self.end_headers()


def start_callback_server(port: int = 8080, background: bool = True) -> HTTPServer | None:
    """Start the callback HTTP server.

    Args:
        port: Port to listen on.
        background: If True, run in a daemon thread and return the server.
                    If False, run in the foreground (blocking).

    Returns:
        The HTTPServer instance if background=True, None otherwise.
    """
    server = HTTPServer(("0.0.0.0", port), CallbackHandler)
    print(f"[callback] Listening on http://0.0.0.0:{port}/callback")

    if background:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server
    else:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        server.server_close()
        return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Callback HTTP server for exfil verification")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on (default: 8080)")
    args = parser.parse_args()
    start_callback_server(port=args.port, background=False)
