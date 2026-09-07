"""Deterministic lexical retrieval over corpus chunks."""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pytest_support.corpus import load_chunk_records

TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+")


@dataclass(frozen=True)
class SearchResult:
    chunk_id: str
    source_page_number: int
    score: float
    text: str


def tokenize(text: str) -> list[str]:
    return [match.group(0).lower() for match in TOKEN_PATTERN.finditer(text)]


def document_frequency(chunks: list[dict[str, Any]]) -> Counter[str]:
    frequencies: Counter[str] = Counter()

    for chunk in chunks:
        frequencies.update(set(tokenize(chunk["text"])))

    return frequencies


def score_chunk(
    query_terms: list[str],
    chunk_terms: Counter[str],
    document_frequencies: Counter[str],
    document_count: int,
) -> float:
    score = 0.0

    for term in query_terms:
        term_frequency = chunk_terms[term]
        if term_frequency == 0:
            continue

        idf = math.log((document_count + 1) / (document_frequencies[term] + 1)) + 1.0
        score += term_frequency * idf

    return score


def search_chunks(
    chunks: list[dict[str, Any]],
    query: str,
    *,
    top_k: int = 5,
) -> list[SearchResult]:
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    query_terms = tokenize(query)
    if not query_terms:
        return []

    document_count = len(chunks)
    document_frequencies = document_frequency(chunks)

    results: list[SearchResult] = []

    for chunk in chunks:
        chunk_terms = Counter(tokenize(chunk["text"]))
        score = score_chunk(
            query_terms=query_terms,
            chunk_terms=chunk_terms,
            document_frequencies=document_frequencies,
            document_count=document_count,
        )

        if score <= 0:
            continue

        results.append(
            SearchResult(
                chunk_id=chunk["chunk_id"],
                source_page_number=chunk["source_page_number"],
                score=score,
                text=chunk["text"],
            )
        )

    return sorted(results, key=lambda result: (-result.score, result.chunk_id))[:top_k]


def search_chunk_file(
    chunks_path: Path,
    query: str,
    *,
    top_k: int = 5,
) -> list[SearchResult]:
    return search_chunks(load_chunk_records(chunks_path), query, top_k=top_k)
