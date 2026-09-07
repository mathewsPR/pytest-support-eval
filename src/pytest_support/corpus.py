"""Corpus manifest and JSONL loading helpers."""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

EXPECTED_CORPUS_ID = "pytest-documentation"


class CorpusError(ValueError):
    """Raised when corpus metadata or records are invalid."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise CorpusError(f"Could not read JSON file: {path}") from error
    except json.JSONDecodeError as error:
        raise CorpusError(f"Invalid JSON file: {path}") from error

    if not isinstance(data, dict):
        raise CorpusError(f"Expected JSON object in file: {path}")

    return data


def require_corpus_id(record: dict[str, Any], *, path: Path) -> None:
    corpus_id = record.get("corpus_id")
    if corpus_id != EXPECTED_CORPUS_ID:
        raise CorpusError(
            f"Unexpected corpus_id in {path}: "
            f"expected {EXPECTED_CORPUS_ID!r}, got {corpus_id!r}"
        )


def load_manifest(path: Path) -> dict[str, Any]:
    manifest = load_json(path)
    require_corpus_id(manifest, path=path)
    return manifest


def iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8") as source:
            for line_number, line in enumerate(source, start=1):
                if not line.strip():
                    continue

                try:
                    record = json.loads(line)
                except json.JSONDecodeError as error:
                    raise CorpusError(
                        f"Invalid JSONL record in {path} on line {line_number}"
                    ) from error

                if not isinstance(record, dict):
                    raise CorpusError(
                        f"Expected JSON object in {path} on line {line_number}"
                    )

                yield record
    except OSError as error:
        raise CorpusError(f"Could not read JSONL file: {path}") from error


def load_page_records(path: Path) -> list[dict[str, Any]]:
    pages = list(iter_jsonl(path))

    for expected_page_number, record in enumerate(pages, start=1):
        require_corpus_id(record, path=path)

        page_number = record.get("pdf_page_number")
        if page_number != expected_page_number:
            raise CorpusError(
                f"Unexpected pdf_page_number in {path}: "
                f"expected {expected_page_number}, got {page_number!r}"
            )

        text = record.get("text")
        if not isinstance(text, str):
            raise CorpusError(
                f"Expected string text in {path} on page {expected_page_number}"
            )

    return pages


def load_chunk_records(path: Path) -> list[dict[str, Any]]:
    chunks = list(iter_jsonl(path))
    seen_chunk_ids: set[str] = set()

    for index, record in enumerate(chunks, start=1):
        require_corpus_id(record, path=path)

        chunk_id = record.get("chunk_id")
        if not isinstance(chunk_id, str) or not chunk_id:
            raise CorpusError(f"Expected non-empty chunk_id in {path} on line {index}")

        if chunk_id in seen_chunk_ids:
            raise CorpusError(f"Duplicate chunk_id in {path}: {chunk_id}")

        seen_chunk_ids.add(chunk_id)

        text = record.get("text")
        if not isinstance(text, str) or not text.strip():
            raise CorpusError(f"Expected non-empty text in {path} on line {index}")

        source_page = record.get("source_page_number")
        source_page_start = record.get("source_page_start")
        source_page_end = record.get("source_page_end")

        if not isinstance(source_page, int) or source_page < 1:
            raise CorpusError(
                f"Expected positive source_page_number in {path} on line {index}"
            )

        if source_page_start != source_page or source_page_end != source_page:
            raise CorpusError(
                f"Expected single-page citation fields in {path} on line {index}"
            )

    return chunks
