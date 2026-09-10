from __future__ import annotations

import pytest

from pytest_support.retrieval import search_chunks, search_pages, tokenize


def make_chunk(
    chunk_id: str,
    page: int,
    text: str,
) -> dict:
    return {
        "corpus_id": "pytest-documentation",
        "chunk_id": chunk_id,
        "source_page_number": page,
        "source_page_start": page,
        "source_page_end": page,
        "text": text,
    }


def test_tokenize_preserves_python_identifiers() -> None:
    assert tokenize("pytest.fixture and tmp_path") == [
        "pytest",
        "fixture",
        "and",
        "tmp_path",
    ]


def test_search_ranks_more_relevant_chunk_first() -> None:
    chunks = [
        make_chunk(
            "pytest-documentation-p0001-c01",
            1,
            "fixture data can be shared by tests",
        ),
        make_chunk(
            "pytest-documentation-p0002-c01",
            2,
            "tmp_path fixture creates temporary directories with pytest fixtures",
        ),
    ]

    results = search_chunks(chunks, "tmp_path fixture", top_k=2)

    assert [result.chunk_id for result in results] == [
        "pytest-documentation-p0002-c01",
        "pytest-documentation-p0001-c01",
    ]


def test_search_returns_page_citation_metadata() -> None:
    chunks = [
        make_chunk(
            "pytest-documentation-p0042-c01",
            42,
            "monkeypatch can modify environment variables during tests",
        )
    ]

    results = search_chunks(chunks, "environment variables")

    assert results[0].source_page_number == 42


def test_search_returns_empty_list_for_empty_query() -> None:
    assert search_chunks([], "   ") == []


def test_search_rejects_invalid_top_k() -> None:
    with pytest.raises(ValueError, match="top_k"):
        search_chunks([], "fixture", top_k=0)


def test_search_pages_aggregates_chunk_scores_by_page() -> None:
    chunks = [
        make_chunk("pytest-documentation-p0001-c01", 1, "fixture setup"),
        make_chunk("pytest-documentation-p0001-c02", 1, "fixture sharing"),
        make_chunk("pytest-documentation-p0002-c01", 2, "fixture"),
    ]

    results = search_pages(chunks, "fixture setup sharing", top_k=2)

    assert [result.source_page_number for result in results] == [1, 2]
    assert results[0].chunk_id == "pytest-documentation-p0001-c02"
    assert results[0].score > results[1].score


def test_search_pages_returns_one_result_per_page() -> None:
    chunks = [
        make_chunk("pytest-documentation-p0001-c01", 1, "fixture setup"),
        make_chunk("pytest-documentation-p0001-c02", 1, "fixture setup"),
        make_chunk("pytest-documentation-p0002-c01", 2, "fixture setup"),
    ]

    results = search_pages(chunks, "fixture", top_k=5)

    assert [result.source_page_number for result in results] == [1, 2]
