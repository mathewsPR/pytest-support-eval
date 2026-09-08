from __future__ import annotations

import json
from pathlib import Path

from pytest_support.agent import PytestSupportAgent


class FakeClient:
    def __init__(self) -> None:
        self.messages: list[dict[str, str]] | None = None
        self.max_tokens: int | None = None

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.0,
        max_tokens: int = 512,
    ) -> str:
        self.messages = messages
        self.max_tokens = max_tokens
        return "Use the missing fixture or define it in conftest.py."


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


def write_jsonl(path: Path, records: list[object]) -> None:
    path.write_text(
        "".join(f"{json.dumps(record)}\n" for record in records),
        encoding="utf-8",
    )


def test_pytest_support_agent_runs_report_answer(tmp_path: Path) -> None:
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    chunks_path = tmp_path / "chunks.jsonl"

    write_json(
        reports_dir / "run-test.json",
        {
            "schema_version": 1,
            "report_id": "run-test",
            "synthetic": True,
            "summary": {
                "total": 1,
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "skipped": 0,
            },
            "tests": [
                {
                    "nodeid": "tests/test_demo.py::test_client",
                    "outcome": "error",
                    "phase": "setup",
                    "message": "FixtureLookupError: fixture 'client' not found",
                }
            ],
        },
    )

    doc_text = (
        "pytest fixture setup errors can happen when a client fixture "
        "is not found in conftest.py."
    )

    write_jsonl(
        chunks_path,
        [
            {
                "corpus_id": "pytest-documentation",
                "chunk_id": "pytest-documentation-p0100-c01",
                "source_page_number": 100,
                "source_page_start": 100,
                "source_page_end": 100,
                "text": doc_text,
            }
        ],
    )

    client = FakeClient()
    agent = PytestSupportAgent(
        client=client,
        reports_dir=reports_dir,
        chunks_path=chunks_path,
        top_k=1,
        max_tokens=256,
    )

    run = agent.run("run-test")

    assert run.report_id == "run-test"
    assert run.answer == "Use the missing fixture or define it in conftest.py."
    assert client.max_tokens == 256
    assert client.messages is not None
    assert "tests/test_demo.py::test_client" in client.messages[1]["content"]
    assert "pytest docs p. 100" in client.messages[1]["content"]
