"""Build bounded prompt context for pytest support runs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pytest_support.tools import read_test_report, search_docs

DEFAULT_DOC_TEXT_CHAR_LIMIT = 1200


def summarize_report(report: dict[str, Any]) -> str:
    """Create a compact text summary of a validated test report."""
    summary = report["summary"]

    lines = [
        f"Report: {report['report_id']}",
        (
            "Summary: "
            f"{summary['total']} total, "
            f"{summary['passed']} passed, "
            f"{summary['failed']} failed, "
            f"{summary['errors']} errors, "
            f"{summary['skipped']} skipped"
        ),
        "Tests:",
    ]

    for test in report["tests"]:
        message = test["message"] if test["message"] is not None else "none"
        lines.append(
            "- "
            f"{test['nodeid']} | "
            f"outcome={test['outcome']} | "
            f"phase={test['phase']} | "
            f"message={message}"
        )

    return "\n".join(lines)


def build_report_query(report: dict[str, Any]) -> str:
    """Build a documentation search query from failing report details."""
    query_parts: list[str] = []

    for test in report["tests"]:
        if test["outcome"] == "passed":
            continue

        query_parts.append(test["outcome"])
        query_parts.append(test["phase"])

        message = test["message"]
        if isinstance(message, str):
            query_parts.append(message)

    if query_parts:
        return " ".join(query_parts)

    return "pytest test report all tests passed"


def truncate_text(text: str, *, char_limit: int) -> str:
    """Trim text to a character budget."""
    if char_limit < 20:
        raise ValueError("char_limit must be at least 20")

    compact = " ".join(text.split())

    if len(compact) <= char_limit:
        return compact

    marker = "..."
    return compact[: char_limit - len(marker)].rstrip() + marker


def limit_docs(
    docs: list[dict[str, Any]],
    *,
    doc_text_char_limit: int = DEFAULT_DOC_TEXT_CHAR_LIMIT,
) -> list[dict[str, Any]]:
    """Return docs with bounded text while preserving metadata."""
    return [
        {
            **doc,
            "text": truncate_text(
                str(doc["text"]),
                char_limit=doc_text_char_limit,
            ),
        }
        for doc in docs
    ]


def build_context(
    report_id: str,
    *,
    reports_dir: Path | None = None,
    chunks_path: Path | None = None,
    top_k: int = 3,
    doc_text_char_limit: int = DEFAULT_DOC_TEXT_CHAR_LIMIT,
) -> dict[str, Any]:
    """Load a report, retrieve docs, and return prompt-ready context."""
    if reports_dir is None:
        report = read_test_report(report_id)
    else:
        report = read_test_report(report_id, reports_dir=reports_dir)

    query = build_report_query(report)

    if chunks_path is None:
        docs = search_docs(query, top_k=top_k)
    else:
        docs = search_docs(query, chunks_path=chunks_path, top_k=top_k)

    return {
        "report": report,
        "report_summary": summarize_report(report),
        "docs_query": query,
        "docs": limit_docs(docs, doc_text_char_limit=doc_text_char_limit),
    }


def format_context(context: dict[str, Any]) -> str:
    """Format context as plain text for a later prompt."""
    lines = [
        "TEST REPORT",
        context["report_summary"],
        "",
        "DOCUMENTATION SEARCH QUERY",
        context["docs_query"],
        "",
        "RETRIEVED DOCUMENTATION",
    ]

    docs = context["docs"]
    if not docs:
        lines.append("No matching documentation chunks found.")
        return "\n".join(lines)

    for index, doc in enumerate(docs, start=1):
        lines.extend(
            [
                f"{index}. {doc['citation']}",
                f"chunk_id: {doc['chunk_id']}",
                f"score: {doc['score']}",
                doc["text"],
                "",
            ]
        )

    return "\n".join(lines).rstrip()
