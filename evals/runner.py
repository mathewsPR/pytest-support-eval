from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from pytest_support.evals.retrieval import load_retrieval_eval_data
from pytest_support.retrieval import search_chunk_file

DEFAULT_EVAL_DATA = Path("evals/data/development.jsonl")
DEFAULT_CHUNKS = Path("corpus/processed/pytest-documentation/chunks.jsonl")
DEFAULT_OUTPUT = Path("artifacts/selected-runs/retrieval-development-baseline.json")


@dataclass(frozen=True)
class QueryRun:
    query: str
    relevant_pages: list[int]
    retrieved_pages: list[int]
    hit: bool


@dataclass(frozen=True)
class RetrievalRun:
    eval_data: str
    chunks: str
    top_k: int
    commit: str | None
    item_count: int
    hit_count: int
    hit_rate: float
    misses: list[QueryRun]
    results: list[QueryRun]


def _git_commit() -> str | None:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    return completed.stdout.strip() or None


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


def _retrieved_pages(search_results: list[Any]) -> list[int]:
    pages: list[int] = []

    for result in search_results:
        if hasattr(result, "source_page_number"):
            pages.append(_page_number(result.source_page_number))
        elif isinstance(result, dict) and "source_page_number" in result:
            pages.append(_page_number(result["source_page_number"]))
        else:
            raise ValueError("search result must contain source_page_number")

    return pages


def _hit(relevant_pages: list[int], retrieved_pages: list[int]) -> bool:
    return bool(set(relevant_pages) & set(retrieved_pages))


def run_retrieval_eval(
    *,
    eval_data: Path,
    chunks: Path,
    top_k: int,
) -> RetrievalRun:
    items = load_retrieval_eval_data(eval_data)

    query_runs: list[QueryRun] = []

    for item in items:
        query = _query_text(item)
        relevant_pages = _relevant_pages(item)

        search_results = search_chunk_file(
            chunks,
            query,
            top_k=top_k,
        )
        retrieved_pages = _retrieved_pages(search_results)

        query_runs.append(
            QueryRun(
                query=query,
                relevant_pages=relevant_pages,
                retrieved_pages=retrieved_pages,
                hit=_hit(relevant_pages, retrieved_pages),
            )
        )

    hit_count = sum(1 for query_run in query_runs if query_run.hit)
    hit_rate = hit_count / len(query_runs) if query_runs else 0.0
    misses = [query_run for query_run in query_runs if not query_run.hit]

    return RetrievalRun(
        eval_data=str(eval_data),
        chunks=str(chunks),
        top_k=top_k,
        commit=_git_commit(),
        item_count=len(query_runs),
        hit_count=hit_count,
        hit_rate=hit_rate,
        misses=misses,
        results=query_runs,
    )


def write_json(path: Path, run: RetrievalRun) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(asdict(run), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run retrieval evaluation against a labeled dataset."
    )
    parser.add_argument(
        "--eval-data",
        type=Path,
        default=DEFAULT_EVAL_DATA,
        help="Path to retrieval eval JSONL data.",
    )
    parser.add_argument(
        "--chunks",
        type=Path,
        default=DEFAULT_CHUNKS,
        help="Path to corpus chunks JSONL file.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of chunks to retrieve per query.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Where to save the JSON baseline result.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the full JSON result to stdout.",
    )

    args = parser.parse_args()

    if args.top_k < 1:
        parser.error("--top-k must be at least 1")

    if not args.eval_data.exists():
        parser.error(f"--eval-data does not exist: {args.eval_data}")

    if not args.chunks.exists():
        parser.error(f"--chunks does not exist: {args.chunks}")

    run = run_retrieval_eval(
        eval_data=args.eval_data,
        chunks=args.chunks,
        top_k=args.top_k,
    )

    write_json(args.output, run)

    if args.json:
        print(json.dumps(asdict(run), indent=2, ensure_ascii=False))
    else:
        print(f"eval_data: {run.eval_data}")
        print(f"chunks: {run.chunks}")
        print(f"top_k: {run.top_k}")
        print(f"commit: {run.commit}")
        print(f"items: {run.item_count}")
        print(f"hits: {run.hit_count}")
        print(f"hit_rate@{run.top_k}: {run.hit_rate:.3f}")
        print(f"misses: {len(run.misses)}")
        print(f"saved: {args.output}")

        if run.misses:
            print()
            print("Misses:")
            for index, miss in enumerate(run.misses, start=1):
                print(f"{index}. {miss.query}")
                print(f"   relevant_pages: {miss.relevant_pages}")
                print(f"   retrieved_pages: {miss.retrieved_pages}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
