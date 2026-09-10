import json

import pytest

from pytest_support.tracing import append_jsonl, make_event, utc_timestamp


def test_utc_timestamp_uses_utc_suffix() -> None:
    timestamp = utc_timestamp()

    assert timestamp.endswith("+00:00")


def test_make_event_rejects_empty_event_type() -> None:
    with pytest.raises(ValueError, match="event_type must not be empty"):
        make_event("", {"key": "value"})


def test_append_jsonl_writes_event(tmp_path) -> None:
    path = tmp_path / "trace.jsonl"
    event = make_event("retrieval.run", {"hit_rate": 0.2})

    append_jsonl(path, event)

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1

    payload = json.loads(lines[0])
    assert payload["event_type"] == "retrieval.run"
    assert payload["payload"] == {"hit_rate": 0.2}
    assert payload["created_at"].endswith("+00:00")
