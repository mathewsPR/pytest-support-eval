from __future__ import annotations


def exact_match(expected: str, actual: str) -> bool:
    return expected.strip() == actual.strip()
