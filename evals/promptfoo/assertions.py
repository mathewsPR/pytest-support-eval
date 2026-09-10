from __future__ import annotations


def assert_non_empty(value: str) -> bool:
    return bool(value.strip())
