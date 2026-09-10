from __future__ import annotations


def contains_required_citation(answer: str) -> bool:
    return "page" in answer.lower()
