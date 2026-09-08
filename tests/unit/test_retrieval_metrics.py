from __future__ import annotations

import json
from pathlib import Path

import pytest

from pytest_support.evals.retrieval import (
    RetrievalEvalItem,
    RetrievalEvalResult,
    evaluate_retrieval,
    hit_rate,
    load_retrieval_eval_data,
    summarize_results,
)


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


def test_load_retrieval_eval_data_reads_items(tmp_path: Path) -> None:
    path = tmp_path / "development.jsonl"
    write_jsonl(
        path,
        [
            {
                "query_id": "dev-001",
                "query": "tmp_path temporary file",
                "relevant_pages": [63],
                "required_terms": ["tmp_path"],
                "notes": "temporary path",
            }
        ],
    )

    items = load_retrieval_eval_data(path)

    assert items == [
        RetrievalEvalItem(
            query_id="dev-001",
            query="tmp_path temporary file",
            relevant_pages={63},
        )
    ]


@pytest.mark.parametrize(
    "record",
    [
        [],
        {"query_id": "", "query": "x", "relevant_pages": [1]},
        {"query_id": "dev-001", "query": "", "relevant_pages": [1]},
        {"query_id": "dev-001", "query": "x", "relevant_pages": []},
        {"query_id": "dev-001", "query": "x", "relevant_pages": [True]},
    ],
)
def test_load_retrieval_eval_data_rejects_invalid_records(
    tmp_path: Path,
    record: object,
) -> None:
    path = tmp_path / "development.jsonl"
    write_jsonl(path, [record])

    with pytest.raises(ValueError):
        load_retrieval_eval_data(path)


def test_evaluate_retrieval_marks_hits_and_misses(tmp_path: Path) -> None:
    chunks_path = tmp_path / "chunks.jsonl"
    write_jsonl(
        chunks_path,
        [
            make_chunk(
                "pytest-documentation-p0063-c01",
                63,
                "tmp_path creates temporary files",
            ),
            make_chunk(
                "pytest-documentation-p0100-c01",
                100,
                "fixtures share setup",
            ),
        ],
    )
    items = [
        RetrievalEvalItem(
            query_id="dev-001",
            query="tmp_path temporary files",
            relevant_pages={63},
        ),
        RetrievalEvalItem(
            query_id="dev-002",
            query="monkeypatch environment variables",
            relevant_pages={69},
        ),
    ]

    results = evaluate_retrieval(items, chunks_path=chunks_path, top_k=1)

    assert results[0].hit is True
    assert results[0].retrieved_pages == [63]
    assert results[1].hit is False
    assert results[1].retrieved_pages == []


def test_hit_rate_and_summary() -> None:
    results = [
        RetrievalEvalResult(
            query_id="dev-001",
            hit=True,
            retrieved_pages=[63],
            relevant_pages=[63],
        ),
        RetrievalEvalResult(
            query_id="dev-002",
            hit=False,
            retrieved_pages=[],
            relevant_pages=[69],
        ),
    ]

    summary = summarize_results(results)

    assert hit_rate(results) == 0.5
    assert summary["queries"] == 2
    assert summary["hits"] == 1
    assert summary["hit_rate"] == 0.5
