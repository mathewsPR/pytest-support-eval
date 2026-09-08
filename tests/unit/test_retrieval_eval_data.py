from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEVELOPMENT_DATA = PROJECT_ROOT / "evals/data/development.jsonl"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_development_retrieval_eval_data_is_valid() -> None:
    records = load_jsonl(DEVELOPMENT_DATA)

    assert len(records) == 10

    query_ids = set()
    for record in records:
        assert set(record) == {
            "query_id",
            "query",
            "relevant_pages",
            "required_terms",
            "notes",
        }

        assert isinstance(record["query_id"], str)
        assert record["query_id"].startswith("dev-")
        assert record["query_id"] not in query_ids
        query_ids.add(record["query_id"])

        assert isinstance(record["query"], str)
        assert record["query"].strip()

        assert isinstance(record["relevant_pages"], list)
        assert record["relevant_pages"]
        assert all(type(page) is int and page > 0 for page in record["relevant_pages"])

        assert isinstance(record["required_terms"], list)
        assert record["required_terms"]
        assert all(
            isinstance(term, str) and term.strip() for term in record["required_terms"]
        )

        assert isinstance(record["notes"], str)
        assert record["notes"].strip()


def test_development_retrieval_eval_ids_are_sequential() -> None:
    records = load_jsonl(DEVELOPMENT_DATA)

    assert [record["query_id"] for record in records] == [
        f"dev-{index:03d}" for index in range(1, 11)
    ]
