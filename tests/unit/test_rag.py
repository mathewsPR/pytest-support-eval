from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pytest_support.rag import answer_report


class FakeClient:
    def __init__(self) -> None:
        self.messages: list[dict[str, str]] | None = None
        self.temperature: float | None = None
        self.max_tokens: int | None = None

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.0,
        max_tokens: int = 512,
    ) -> str:
        self.messages = messages
        self.temperature = temperature
        self.max_tokens = max_tokens
        return "The test failed because the assertion expected a different value."


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


def write_jsonl(path: Path, records: list[object]) -> None:
    path.write_text(
        "".join(f"{json.dumps(record)}\n" for record in records),
        encoding="utf-8",
    )


def make_report() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "report_id": "run-test",
        "synthetic": True,
        "summary": {
            "total": 1,
            "passed": 0,
            "failed": 1,
            "errors": 0,
            "skipped": 0,
        },
        "tests": [
            {
                "nodeid": "tests/test_demo.py::test_bad",
                "outcome": "failed",
                "phase": "call",
                "message": "AssertionError: assert 1 == 2",
            }
        ],
    }


def make_chunk() -> dict[str, object]:
    text = "pytest explains failing assert statements with assertion introspection."

    return {
        "corpus_id": "pytest-documentation",
        "chunk_id": "pytest-documentation-p0042-c01",
        "source_page_number": 42,
        "source_page_start": 42,
        "source_page_end": 42,
        "text": text,
    }


def test_answer_report_builds_messages_and_calls_client(tmp_path: Path) -> None:
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    chunks_path = tmp_path / "chunks.jsonl"
    write_json(reports_dir / "run-test.json", make_report())
    write_jsonl(chunks_path, [make_chunk()])

    client = FakeClient()

    answer = answer_report(
        "run-test",
        client=client,
        reports_dir=reports_dir,
        chunks_path=chunks_path,
        max_tokens=256,
    )

    assert answer == (
        "The test failed because the assertion expected a different value."
    )
    assert client.temperature == 0.0
    assert client.max_tokens == 256
    assert client.messages is not None
    assert client.messages[0]["role"] == "system"
    assert client.messages[1]["role"] == "user"
    assert "tests/test_demo.py::test_bad" in client.messages[1]["content"]
    assert "pytest docs p. 42" in client.messages[1]["content"]
