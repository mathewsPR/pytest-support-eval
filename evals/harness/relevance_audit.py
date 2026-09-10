from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from pytest_support.evals.retrieval import load_retrieval_eval_data
from pytest_support.retrieval import search_chunk_file

DEFAULT_EVAL_DATA = Path("evals/data/development.jsonl")
DEFAULT_CHUNKS = Path("corpus/processed/pytest-documentation/chunks.jsonl")
DEFAULT_OUTPUT = Path("artifacts/selected-runs/relevance-audit-development.md")


def load_chunks_by_page(chunks_path: Path) -> dict[int, list[dict]]:
    chunks_by_page: dict[int, list[dict]] = defaultdict(list)

    for line in chunks_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue

        record = json.loads(line)
        page = record["source_page_number"]
        chunks_by_page[page].append(record)

    return dict(chunks_by_page)


def clip(text: str, max_chars: int) -> str:
    text = " ".join(text.split())
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."


def code_block(text: str) -> str:
    return f"```text\n{text.replace('```', '`​``')}\n```"


def build_report(
    *,
    eval_data: Path,
    chunks: Path,
    top_k: int,
    max_chars: int,
) -> str:
    items = load_retrieval_eval_data(eval_data)
    chunks_by_page = load_chunks_by_page(chunks)

    lines = [
        "# Relevance Audit: Development Set",
        "",
        f"- Eval data: `{eval_data}`",
        f"- Chunks: `{chunks}`",
        f"- Top k: `{top_k}`",
        f"- Items: {len(items)}",
        "",
        "This report compares labeled relevant pages with retrieved pages.",
        "",
    ]

    hits = 0

    for index, item in enumerate(items, start=1):
        results = search_chunk_file(chunks, item.query, top_k=top_k)
        relevant_pages = sorted(item.relevant_pages)
        retrieved_pages = [result.source_page_number for result in results]
        hit = bool(set(relevant_pages) & set(retrieved_pages))

        if hit:
            hits += 1

        lines.extend(
            [
                f"## {index}. {item.query_id}: {item.query}",
                "",
                f"- Relevant pages: `{relevant_pages}`",
                f"- Retrieved pages: `{retrieved_pages}`",
                f"- Hit: `{hit}`",
                "",
                "### Retrieved chunks",
                "",
            ]
        )

        for rank, result in enumerate(results, start=1):
            lines.extend(
                [
                    (
                        f"#### Rank {rank}: page {result.source_page_number}, "
                        f"score {result.score:.3f}, chunk `{result.chunk_id}`"
                    ),
                    "",
                    code_block(clip(result.text, max_chars)),
                    "",
                ]
            )

        lines.extend(["### Labeled relevant page text", ""])

        for page in relevant_pages:
            page_chunks = chunks_by_page.get(page, [])
            if not page_chunks:
                lines.append(f"- Page {page}: no chunks found")
                lines.append("")
                continue

            lines.append(f"- Page {page}: {len(page_chunks)} chunk(s)")
            for chunk in page_chunks[:3]:
                lines.append(f"  - Chunk `{chunk.get('chunk_id', '')}`")
                lines.append(code_block(clip(str(chunk.get("text", "")), max_chars)))
            lines.append("")

    hit_rate = hits / len(items) if items else 0.0
    lines.insert(6, f"- Hits: {hits}")
    lines.insert(7, f"- Hit rate@{top_k}: {hit_rate:.3f}")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a relevance audit report.")
    parser.add_argument("--eval-data", type=Path, default=DEFAULT_EVAL_DATA)
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--max-chars", type=int, default=900)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if not args.eval_data.exists():
        parser.error(f"--eval-data does not exist: {args.eval_data}")

    if not args.chunks.exists():
        parser.error(f"--chunks does not exist: {args.chunks}")

    report = build_report(
        eval_data=args.eval_data,
        chunks=args.chunks,
        top_k=args.top_k,
        max_chars=args.max_chars,
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")

    print(f"saved: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
