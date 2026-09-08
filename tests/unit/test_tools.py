from __future__ import annotations

import json
from pathlib import Path

import pytest

from pytest_support.tools import ToolError, read_test_report, search_docs


def write_jsonl(path: Path, records: list[object]) -> None:
    path.write_text(
        "".join(f"{json.dumps(record)}\n" for record in records),
        encoding="utf-8",
    )


def make_chunk(chunk_id: str, page: int, text: str) -> dict[str, object]:
    return {
        "corpus_id": "pytest-documentation",
        "chunk_id": chunk_id,
        "source_page_number": page,
        "source_page_start": page,
        "source_page_end": page,
        "text": text,
    }


def test_search_docs_returns_citation_ready_results(tmp_path: Path) -> None:
    chunks_path = tmp_path / "chunks.jsonl"
    write_jsonl(
        chunks_path,
        [
            make_chunk(
                "pytest-documentation-p0001-c01",
                1,
                "tmp_path creates temporary directories for tests",
            ),
            make_chunk(
                "pytest-documentation-p0002-c01",
                2,
                "monkeypatch changes environment variables",
            ),
        ],
    )

    results = search_docs(
        "temporary directory",
        chunks_path=chunks_path,
        top_k=1,
    )

    assert results == [
        {
            "chunk_id": "pytest-documentation-p0001-c01",
            "source_page_number": 1,
            "score": results[0]["score"],
            "text": "tmp_path creates temporary directories for tests",
            "citation": "pytest docs p. 1",
        }
    ]
    assert results[0]["score"] > 0


def test_search_docs_returns_empty_list_for_no_matches(tmp_path: Path) -> None:
    chunks_path = tmp_path / "chunks.jsonl"
    write_jsonl(
        chunks_path,
        [
            make_chunk(
                "pytest-documentation-p0001-c01",
                1,
                "fixtures share setup between tests",
            )
        ],
    )

    assert search_docs("unrelated", chunks_path=chunks_path) == []


def test_search_docs_rejects_empty_query(tmp_path: Path) -> None:
    chunks_path = tmp_path / "chunks.jsonl"
    write_jsonl(chunks_path, [])

    with pytest.raises(ToolError, match="query"):
        search_docs("   ", chunks_path=chunks_path)


def test_search_docs_rejects_invalid_top_k(tmp_path: Path) -> None:
    chunks_path = tmp_path / "chunks.jsonl"
    write_jsonl(chunks_path, [])

    with pytest.raises(ToolError, match="top_k"):
        search_docs("fixture", chunks_path=chunks_path, top_k=0)


def test_read_test_report_loads_valid_fixture() -> None:
    report = read_test_report("run-002")

    assert report["report_id"] == "run-002"
    assert report["summary"] == {
        "total": 2,
        "passed": 1,
        "failed": 1,
        "errors": 0,
        "skipped": 0,
    }


def test_read_test_report_rejects_unknown_report() -> None:
    with pytest.raises(ToolError, match="unknown report_id"):
        read_test_report("missing")


def test_read_test_report_rejects_path_traversal() -> None:
    with pytest.raises(ToolError, match="not a path"):
        read_test_report("../run-001")


def test_read_test_report_rejects_invalid_fixture(tmp_path: Path) -> None:
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    path = reports_dir / "broken.json"
    path.write_text('{"schema_version": 1}', encoding="utf-8")

    with pytest.raises(ToolError, match="invalid report fixture"):
        read_test_report("broken", reports_dir=reports_dir)
