from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Event:
    event_type: str
    scenario_id: str
    mode: str
    action: str
    capability: str
    allowed: bool
    reason: str
    canary_touched: bool
    sequence: int

    def to_jsonrpc(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "method": "canaryweave.event",
            "params": asdict(self),
            "id": f"{self.scenario_id}:{self.sequence}",
        }


class JsonRpcEventLogger:
    """JSON-RPC-shaped event logger with optional JSONL persistence."""

    def __init__(self, path: Path | str | None = None):
        self.path = Path(path) if path is not None else None
        self.events: list[Event] = []
        self._fh = None
        if self.path is not None:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._fh = self.path.open("w", encoding="utf-8")

    def log(self, event: Event) -> None:
        self.events.append(event)
        if self._fh is not None:
            self._fh.write(json.dumps(event.to_jsonrpc(), sort_keys=True) + "\n")
            self._fh.flush()

    def close(self) -> None:
        if self._fh is not None:
            self._fh.close()
            self._fh = None

    def __enter__(self) -> "JsonRpcEventLogger":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        self.close()
