from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from pytest_support.evals.retrieval import load_retrieval_eval_data
from pytest_support.retrieval import search_chunk_file

DEFAULT_EVAL_DATA = Path("evals/data/development.jsonl")
DEFAULT_CHUNKS = Path("corpus/processed/pytest-documentation/chunks.jsonl")
DEFAULT_OUTPUT = Path("artifacts/selected-runs/retrieval-diagnostics.json")


def _page_number(value: Any) -> int:
    if isinstance(value, bool):
        raise ValueError("page number must be an integer, not a boolean")

    if isinstance(value, int):
        return value

    if isinstance(value, str) and value.isdigit():
        return int(value)

    raise ValueError(f"invalid page number: {value!r}")


def _query_text(item: Any) -> str:
    if hasattr(item, "query"):
        return str(item.query)

    if hasattr(item, "question"):
        return str(item.question)

    if isinstance(item, dict):
        if "query" in item:
            return str(item["query"])
        if "question" in item:
            return str(item["question"])

    raise ValueError("retrieval eval item must contain query or question")


def _relevant_pages(item: Any) -> list[int]:
    if hasattr(item, "relevant_pages"):
        raw_pages = item.relevant_pages
    elif hasattr(item, "expected_pages"):
        raw_pages = item.expected_pages
    elif hasattr(item, "source_page_numbers"):
        raw_pages = item.source_page_numbers
    elif isinstance(item, dict) and "relevant_pages" in item:
        raw_pages = item["relevant_pages"]
    elif isinstance(item, dict) and "expected_pages" in item:
        raw_pages = item["expected_pages"]
    elif isinstance(item, dict) and "source_page_numbers" in item:
        raw_pages = item["source_page_numbers"]
    else:
        raise ValueError(
            "retrieval eval item must contain relevant_pages, "
            "expected_pages, or source_page_numbers"
        )

    return sorted({_page_number(page) for page in raw_pages})


def _result_page(result: Any) -> int:
    if hasattr(result, "source_page_number"):
        return _page_number(result.source_page_number)

    if isinstance(result, dict) and "source_page_number" in result:
        return _page_number(result["source_page_number"])

    raise ValueError("search result must contain source_page_number")


def _result_score(result: Any) -> float:
    if hasattr(result, "score"):
        return float(result.score)

    if isinstance(result, dict) and "score" in result:
        return float(result["score"])

    return 0.0


def _result_text(result: Any) -> str:
    if hasattr(result, "text"):
        return str(result.text)

    if isinstance(result, dict) and "text" in result:
        return str(result["text"])

    return ""


def diagnose(
    *,
    eval_data: Path,
    chunks: Path,
    top_k: int,
    preview_chars: int,
) -> dict[str, Any]:
    items = load_retrieval_eval_data(eval_data)

    rows: list[dict[str, Any]] = []
    retrieved_page_counts: Counter[int] = Counter()
    missed_relevant_page_counts: Counter[int] = Counter()

    for item in items:
        query = _query_text(item)
        relevant_pages = _relevant_pages(item)
        results = search_chunk_file(chunks, query, top_k=top_k)

        retrieved = []
        for result in results:
            page = _result_page(result)
            retrieved_page_counts[page] += 1
            retrieved.append(
                {
                    "page": page,
                    "score": _result_score(result),
                    "preview": _result_text(result)[:preview_chars],
                }
            )

        retrieved_pages = [entry["page"] for entry in retrieved]
        hit = bool(set(relevant_pages) & set(retrieved_pages))

        if not hit:
            missed_relevant_page_counts.update(relevant_pages)

        rows.append(
            {
                "query": query,
                "relevant_pages": relevant_pages,
                "retrieved_pages": retrieved_pages,
                "hit": hit,
                "retrieved": retrieved,
            }
        )

    return {
        "eval_data": str(eval_data),
        "chunks": str(chunks),
        "top_k": top_k,
        "item_count": len(rows),
        "hit_count": sum(1 for row in rows if row["hit"]),
        "hit_rate": (sum(1 for row in rows if row["hit"]) / len(rows) if rows else 0.0),
        "most_common_retrieved_pages": retrieved_page_counts.most_common(10),
        "missed_relevant_pages": missed_relevant_page_counts.most_common(10),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diagnose retrieval misses and repeated retrieved pages."
    )
    parser.add_argument("--eval-data", type=Path, default=DEFAULT_EVAL_DATA)
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--preview-chars", type=int, default=240)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if args.top_k < 1:
        parser.error("--top-k must be at least 1")

    if args.preview_chars < 1:
        parser.error("--preview-chars must be at least 1")

    if not args.eval_data.exists():
        parser.error(f"--eval-data does not exist: {args.eval_data}")

    if not args.chunks.exists():
        parser.error(f"--chunks does not exist: {args.chunks}")

    report = diagnose(
        eval_data=args.eval_data,
        chunks=args.chunks,
        top_k=args.top_k,
        preview_chars=args.preview_chars,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"items: {report['item_count']}")
    print(f"hits: {report['hit_count']}")
    print(f"hit_rate@{report['top_k']}: {report['hit_rate']:.3f}")
    print(f"saved: {args.output}")

    print()
    print("Most common retrieved pages:")
    for page, count in report["most_common_retrieved_pages"]:
        print(f"- page {page}: {count}")

    print()
    print("Most common missed relevant pages:")
    for page, count in report["missed_relevant_pages"]:
        print(f"- page {page}: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
