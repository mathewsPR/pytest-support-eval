"""Local tools used by the pytest support agent."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pytest_support.corpus import CorpusError, load_chunk_records
from pytest_support.retrieval import search_chunks
from pytest_support.schemas import ReportValidationError, validate_test_report

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CHUNKS_PATH = (
    PROJECT_ROOT / "corpus/processed/pytest-documentation/chunks.jsonl"
)
DEFAULT_REPORTS_DIR = PROJECT_ROOT / "fixtures/reports"


class ToolError(ValueError):
    """Raised when a local tool cannot complete a requested operation."""


def search_docs(
    query: str,
    *,
    chunks_path: Path = DEFAULT_CHUNKS_PATH,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    """Search pytest documentation chunks and return citation-ready results."""
    if not isinstance(query, str) or not query.strip():
        raise ToolError("query must be a non-empty string")

    if top_k < 1:
        raise ToolError("top_k must be at least 1")

    try:
        chunks = load_chunk_records(chunks_path)
    except CorpusError as error:
        raise ToolError(str(error)) from error

    results = search_chunks(chunks, query, top_k=top_k)

    return [
        {
            "chunk_id": result.chunk_id,
            "source_page_number": result.source_page_number,
            "score": round(result.score, 3),
            "text": result.text,
            "citation": f"pytest docs p. {result.source_page_number}",
        }
        for result in results
    ]


def read_test_report(
    report_id: str,
    *,
    reports_dir: Path = DEFAULT_REPORTS_DIR,
) -> dict[str, Any]:
    """Load and validate one fixed test-report fixture."""
    if not isinstance(report_id, str) or not report_id.strip():
        raise ToolError("report_id must be a non-empty string")

    if "/" in report_id or "\\" in report_id:
        raise ToolError("report_id must be a fixture id, not a path")

    report_path = reports_dir / f"{report_id}.json"

    try:
        raw_report = json.loads(report_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ToolError(f"unknown report_id: {report_id}") from error
    except OSError as error:
        raise ToolError(f"could not read report fixture: {report_id}") from error
    except json.JSONDecodeError as error:
        raise ToolError(f"invalid report fixture JSON: {report_id}") from error

    try:
        return validate_test_report(raw_report)
    except ReportValidationError as error:
        raise ToolError(f"invalid report fixture {report_id}: {error}") from error
