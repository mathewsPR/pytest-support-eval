from __future__ import annotations

import json
from pathlib import Path

from pytest_support.context import (
    build_context,
    build_report_query,
    format_context,
    limit_docs,
    summarize_report,
    truncate_text,
)


def write_jsonl(path: Path, records: list[object]) -> None:
    path.write_text(
        "".join(f"{json.dumps(record)}\n" for record in records),
        encoding="utf-8",
    )


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


def make_report(report_id: str, tests: list[dict[str, object]]) -> dict[str, object]:
    passed = sum(test["outcome"] == "passed" for test in tests)
    failed = sum(test["outcome"] == "failed" for test in tests)
    errors = sum(test["outcome"] == "error" for test in tests)
    skipped = sum(test["outcome"] == "skipped" for test in tests)

    return {
        "schema_version": 1,
        "report_id": report_id,
        "synthetic": True,
        "summary": {
            "total": len(tests),
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "skipped": skipped,
        },
        "tests": tests,
    }


def make_chunk(chunk_id: str, page: int, text: str) -> dict[str, object]:
    return {
        "corpus_id": "pytest-documentation",
        "chunk_id": chunk_id,
        "source_page_number": page,
        "source_page_start": page,
        "source_page_end": page,
        "text": text,
    }


def test_summarize_report_includes_counts_and_test_details() -> None:
    report = make_report(
        "run-test",
        [
            {
                "nodeid": "tests/test_demo.py::test_ok",
                "outcome": "passed",
                "phase": "call",
                "message": None,
            },
            {
                "nodeid": "tests/test_demo.py::test_bad",
                "outcome": "failed",
                "phase": "call",
                "message": "AssertionError: assert 1 == 2",
            },
        ],
    )

    summary = summarize_report(report)

    assert "Report: run-test" in summary
    assert "2 total, 1 passed, 1 failed, 0 errors, 0 skipped" in summary
    assert "tests/test_demo.py::test_bad" in summary
    assert "AssertionError: assert 1 == 2" in summary


def test_build_report_query_uses_non_passing_tests() -> None:
    report = make_report(
        "run-test",
        [
            {
                "nodeid": "tests/test_demo.py::test_ok",
                "outcome": "passed",
                "phase": "call",
                "message": None,
            },
            {
                "nodeid": "tests/test_demo.py::test_client",
                "outcome": "error",
                "phase": "setup",
                "message": "FixtureLookupError: fixture 'client' not found",
            },
        ],
    )

    assert build_report_query(report) == (
        "error setup FixtureLookupError: fixture 'client' not found"
    )


def test_build_report_query_for_passing_report() -> None:
    report = make_report(
        "run-test",
        [
            {
                "nodeid": "tests/test_demo.py::test_ok",
                "outcome": "passed",
                "phase": "call",
                "message": None,
            }
        ],
    )

    assert build_report_query(report) == "pytest test report all tests passed"


def test_build_context_loads_report_and_retrieved_docs(tmp_path: Path) -> None:
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    chunks_path = tmp_path / "chunks.jsonl"

    write_json(
        reports_dir / "run-test.json",
        make_report(
            "run-test",
            [
                {
                    "nodeid": "tests/test_demo.py::test_client",
                    "outcome": "error",
                    "phase": "setup",
                    "message": "FixtureLookupError: fixture 'client' not found",
                }
            ],
        ),
    )
    write_jsonl(
        chunks_path,
        [
            make_chunk(
                "pytest-documentation-p0100-c01",
                100,
                "pytest fixtures are requested by test functions and setup can fail",
            ),
            make_chunk(
                "pytest-documentation-p0101-c01",
                101,
                "unrelated documentation about markers",
            ),
        ],
    )

    context = build_context(
        "run-test",
        reports_dir=reports_dir,
        chunks_path=chunks_path,
        top_k=1,
    )

    assert context["report"]["report_id"] == "run-test"
    assert context["docs_query"] == (
        "error setup FixtureLookupError: fixture 'client' not found"
    )
    assert context["docs"][0]["chunk_id"] == "pytest-documentation-p0100-c01"
    assert context["docs"][0]["citation"] == "pytest docs p. 100"


def test_format_context_includes_report_and_docs() -> None:
    context = {
        "report_summary": "Report: run-test\nSummary: 1 total",
        "docs_query": "fixture setup error",
        "docs": [
            {
                "citation": "pytest docs p. 100",
                "chunk_id": "pytest-documentation-p0100-c01",
                "score": 12.345,
                "text": "Fixtures can be used during setup.",
            }
        ],
    }

    formatted = format_context(context)

    assert "TEST REPORT" in formatted
    assert "Report: run-test" in formatted
    assert "DOCUMENTATION SEARCH QUERY" in formatted
    assert "fixture setup error" in formatted
    assert "pytest docs p. 100" in formatted
    assert "Fixtures can be used during setup." in formatted


def test_format_context_handles_no_docs() -> None:
    context = {
        "report_summary": "Report: run-test",
        "docs_query": "unknown topic",
        "docs": [],
    }

    assert "No matching documentation chunks found." in format_context(context)


def test_truncate_text_compacts_whitespace_and_respects_limit() -> None:
    text = "alpha\n\nbeta     gamma " * 20

    truncated = truncate_text(text, char_limit=60)

    assert len(truncated) <= 60
    assert "\n" not in truncated
    assert "  " not in truncated
    assert truncated.endswith("...")


def test_truncate_text_rejects_tiny_limit() -> None:
    try:
        truncate_text("short text", char_limit=10)
    except ValueError as error:
        assert "char_limit" in str(error)
    else:
        raise AssertionError("expected ValueError")


def test_limit_docs_preserves_metadata_and_trims_text() -> None:
    docs = [
        {
            "citation": "pytest docs p. 100",
            "chunk_id": "pytest-documentation-p0100-c01",
            "score": 12.345,
            "source_page_number": 100,
            "text": "fixture setup details " * 20,
        }
    ]

    limited = limit_docs(docs, doc_text_char_limit=80)

    assert limited[0]["citation"] == "pytest docs p. 100"
    assert limited[0]["chunk_id"] == "pytest-documentation-p0100-c01"
    assert limited[0]["score"] == 12.345
    assert limited[0]["source_page_number"] == 100
    assert len(limited[0]["text"]) <= 80
    assert limited[0]["text"].endswith("...")


def test_build_context_limits_retrieved_doc_text(tmp_path: Path) -> None:
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    chunks_path = tmp_path / "chunks.jsonl"

    write_json(
        reports_dir / "run-test.json",
        make_report(
            "run-test",
            [
                {
                    "nodeid": "tests/test_demo.py::test_client",
                    "outcome": "error",
                    "phase": "setup",
                    "message": "FixtureLookupError: fixture 'client' not found",
                }
            ],
        ),
    )
    write_jsonl(
        chunks_path,
        [
            make_chunk(
                "pytest-documentation-p0100-c01",
                100,
                "pytest fixtures setup lookup error " * 50,
            )
        ],
    )

    context = build_context(
        "run-test",
        reports_dir=reports_dir,
        chunks_path=chunks_path,
        doc_text_char_limit=90,
    )

    assert len(context["docs"][0]["text"]) <= 90
    assert context["docs"][0]["text"].endswith("...")
    assert context["docs"][0]["citation"] == "pytest docs p. 100"
