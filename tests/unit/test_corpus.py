from __future__ import annotations

import json
from pathlib import Path

import pytest

from pytest_support.corpus import (
    CorpusError,
    iter_jsonl,
    load_chunk_records,
    load_manifest,
    load_page_records,
)


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


def write_jsonl(path: Path, records: list[object]) -> None:
    path.write_text(
        "".join(f"{json.dumps(record)}\n" for record in records),
        encoding="utf-8",
    )


def test_load_manifest_accepts_expected_corpus_id(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    write_json(path, {"corpus_id": "pytest-documentation"})

    assert load_manifest(path)["corpus_id"] == "pytest-documentation"


def test_load_manifest_rejects_unexpected_corpus_id(tmp_path: Path) -> None:
    path = tmp_path / "manifest.json"
    write_json(path, {"corpus_id": "other"})

    with pytest.raises(CorpusError, match="Unexpected corpus_id"):
        load_manifest(path)


def test_iter_jsonl_skips_blank_lines(tmp_path: Path) -> None:
    path = tmp_path / "records.jsonl"
    path.write_text('{"a": 1}\n\n{"b": 2}\n', encoding="utf-8")

    assert list(iter_jsonl(path)) == [{"a": 1}, {"b": 2}]


def test_iter_jsonl_rejects_non_object_records(tmp_path: Path) -> None:
    path = tmp_path / "records.jsonl"
    path.write_text("[1, 2, 3]\n", encoding="utf-8")

    with pytest.raises(CorpusError, match="Expected JSON object"):
        list(iter_jsonl(path))


def test_load_page_records_accepts_sequential_pages(tmp_path: Path) -> None:
    path = tmp_path / "pages.jsonl"
    write_jsonl(
        path,
        [
            {
                "corpus_id": "pytest-documentation",
                "pdf_page_number": 1,
                "text": "Page one",
            },
            {
                "corpus_id": "pytest-documentation",
                "pdf_page_number": 2,
                "text": "",
            },
        ],
    )

    assert len(load_page_records(path)) == 2


def test_load_page_records_rejects_page_number_gap(tmp_path: Path) -> None:
    path = tmp_path / "pages.jsonl"
    write_jsonl(
        path,
        [
            {
                "corpus_id": "pytest-documentation",
                "pdf_page_number": 2,
                "text": "Wrong page",
            }
        ],
    )

    with pytest.raises(CorpusError, match="Unexpected pdf_page_number"):
        load_page_records(path)


def test_load_chunk_records_accepts_single_page_chunks(tmp_path: Path) -> None:
    path = tmp_path / "chunks.jsonl"
    write_jsonl(
        path,
        [
            {
                "corpus_id": "pytest-documentation",
                "chunk_id": "pytest-documentation-p0001-c01",
                "source_page_number": 1,
                "source_page_start": 1,
                "source_page_end": 1,
                "text": "chunk text",
            }
        ],
    )

    assert load_chunk_records(path)[0]["chunk_id"] == "pytest-documentation-p0001-c01"


def test_load_chunk_records_rejects_duplicate_chunk_ids(tmp_path: Path) -> None:
    path = tmp_path / "chunks.jsonl"
    record = {
        "corpus_id": "pytest-documentation",
        "chunk_id": "pytest-documentation-p0001-c01",
        "source_page_number": 1,
        "source_page_start": 1,
        "source_page_end": 1,
        "text": "chunk text",
    }
    write_jsonl(path, [record, record])

    with pytest.raises(CorpusError, match="Duplicate chunk_id"):
        load_chunk_records(path)


def test_load_chunk_records_rejects_cross_page_citations(tmp_path: Path) -> None:
    path = tmp_path / "chunks.jsonl"
    write_jsonl(
        path,
        [
            {
                "corpus_id": "pytest-documentation",
                "chunk_id": "pytest-documentation-p0001-c01",
                "source_page_number": 1,
                "source_page_start": 1,
                "source_page_end": 2,
                "text": "chunk text",
            }
        ],
    )

    with pytest.raises(CorpusError, match="single-page citation"):
        load_chunk_records(path)
