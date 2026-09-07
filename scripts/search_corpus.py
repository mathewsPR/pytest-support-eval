"""Search the local processed pytest documentation corpus."""

from __future__ import annotations

import argparse
from pathlib import Path

from pytest_support.retrieval import search_chunk_file

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHUNKS_PATH = (
    PROJECT_ROOT / "corpus/processed/pytest-documentation/chunks.jsonl"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search the local processed pytest documentation chunks."
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "--chunks",
        type=Path,
        default=DEFAULT_CHUNKS_PATH,
        help="Path to chunks.jsonl",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of results to show",
    )
    parser.add_argument(
        "--preview-chars",
        type=int,
        default=500,
        help="Maximum characters of each chunk to print",
    )
    return parser.parse_args()


def compact_preview(text: str, limit: int) -> str:
    preview = " ".join(text.split())
    if len(preview) <= limit:
        return preview
    return f"{preview[: limit - 3]}..."


def main() -> None:
    args = parse_args()

    if args.top_k < 1:
        raise SystemExit("--top-k must be at least 1")

    if args.preview_chars < 80:
        raise SystemExit("--preview-chars must be at least 80")

    if not args.chunks.is_file():
        raise SystemExit(f"Chunks file not found: {args.chunks}")

    results = search_chunk_file(args.chunks, args.query, top_k=args.top_k)

    if not results:
        print("No matching chunks found.")
        return

    for index, result in enumerate(results, start=1):
        print(f"{index}. {result.chunk_id}")
        print(f"   page: {result.source_page_number}")
        print(f"   score: {result.score:.3f}")
        print(f"   text: {compact_preview(result.text, args.preview_chars)}")
        print()


if __name__ == "__main__":
    main()
