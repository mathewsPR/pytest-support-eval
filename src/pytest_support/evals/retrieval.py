"""Retrieval evaluation metrics."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pytest_support.retrieval import search_chunk_file


@dataclass(frozen=True)
class RetrievalEvalItem:
    query_id: str
    query: str
    relevant_pages: set[int]


@dataclass(frozen=True)
class RetrievalEvalResult:
    query_id: str
    hit: bool
    retrieved_pages: list[int]
    relevant_pages: list[int]


def load_retrieval_eval_data(path: Path) -> list[RetrievalEvalItem]:
    """Load retrieval evaluation data from JSONL."""
    items: list[RetrievalEvalItem] = []

    lines = path.read_text(encoding="utf-8").splitlines()
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        raw = json.loads(line)

        if not isinstance(raw, dict):
            raise ValueError(f"line {line_number} must be a JSON object")

        query_id = raw.get("query_id")
        query = raw.get("query")
        relevant_pages = raw.get("relevant_pages")

        if not isinstance(query_id, str) or not query_id.strip():
            raise ValueError(f"line {line_number} has invalid query_id")

        if not isinstance(query, str) or not query.strip():
            raise ValueError(f"line {line_number} has invalid query")

        if not isinstance(relevant_pages, list) or not relevant_pages:
            raise ValueError(f"line {line_number} has invalid relevant_pages")

        page_set: set[int] = set()
        for page in relevant_pages:
            if type(page) is not int or page < 1:
                raise ValueError(f"line {line_number} has invalid relevant page")
            page_set.add(page)

        items.append(
            RetrievalEvalItem(
                query_id=query_id,
                query=query,
                relevant_pages=page_set,
            )
        )

    return items


def evaluate_retrieval(
    items: list[RetrievalEvalItem],
    *,
    chunks_path: Path,
    top_k: int = 3,
) -> list[RetrievalEvalResult]:
    """Evaluate retrieval hits against expected relevant pages."""
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    results: list[RetrievalEvalResult] = []

    for item in items:
        retrieved = search_chunk_file(chunks_path, item.query, top_k=top_k)
        retrieved_pages = [result.source_page_number for result in retrieved]
        hit = bool(item.relevant_pages.intersection(retrieved_pages))

        results.append(
            RetrievalEvalResult(
                query_id=item.query_id,
                hit=hit,
                retrieved_pages=retrieved_pages,
                relevant_pages=sorted(item.relevant_pages),
            )
        )

    return results


def hit_rate(results: list[RetrievalEvalResult]) -> float:
    """Return the fraction of queries with at least one relevant page hit."""
    if not results:
        raise ValueError("results must not be empty")

    return sum(result.hit for result in results) / len(results)


def summarize_results(results: list[RetrievalEvalResult]) -> dict[str, Any]:
    """Summarize retrieval evaluation results."""
    return {
        "queries": len(results),
        "hits": sum(result.hit for result in results),
        "hit_rate": hit_rate(results),
        "results": [
            {
                "query_id": result.query_id,
                "hit": result.hit,
                "retrieved_pages": result.retrieved_pages,
                "relevant_pages": result.relevant_pages,
            }
            for result in results
        ],
    }
