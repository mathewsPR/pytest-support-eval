from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class TraceEvent:
    event_type: str
    payload: dict[str, Any]
    created_at: str


def utc_timestamp() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def make_event(event_type: str, payload: dict[str, Any]) -> TraceEvent:
    if not event_type:
        raise ValueError("event_type must not be empty")

    return TraceEvent(
        event_type=event_type,
        payload=payload,
        created_at=utc_timestamp(),
    )


def append_jsonl(path: Path, event: TraceEvent) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")
