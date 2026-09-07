from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHUNK_MANIFEST = PROJECT_ROOT / "artifacts/manifests/corpus-chunks.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_chunk_manifest_records_expected_strategy() -> None:
    manifest = load_json(CHUNK_MANIFEST)

    assert manifest["schema_version"] == 1
    assert manifest["corpus_id"] == "pytest-documentation"
    assert manifest["chunking_strategy"] == (
        "single-page paragraph chunks with local overlap"
    )
    assert manifest["target_chars"] == 1800
    assert manifest["overlap_chars"] == 250
    assert manifest["min_chars"] == 350
    assert manifest["chunking_status"] == "completed"


def test_chunk_manifest_records_expected_counts() -> None:
    manifest = load_json(CHUNK_MANIFEST)

    assert manifest["source_page_count"] == 571
    assert manifest["pages_with_chunks"] == 570
    assert manifest["empty_pages"] == 1
    assert manifest["chunk_count"] == 920


def test_chunk_manifest_tracks_inputs_and_outputs() -> None:
    manifest = load_json(CHUNK_MANIFEST)

    assert manifest["extraction_manifest_path"] == (
        "artifacts/manifests/corpus-extraction.json"
    )
    assert manifest["pages_path"] == (
        "corpus/extracted/pytest-documentation/pages.jsonl"
    )
    assert manifest["chunks_path"] == (
        "corpus/processed/pytest-documentation/chunks.jsonl"
    )
    assert len(manifest["source_sha256"]) == 64
    assert len(manifest["extraction_manifest_sha256"]) == 64
    assert len(manifest["pages_sha256"]) == 64
    assert len(manifest["chunks_sha256"]) == 64
    assert len(manifest["script_sha256"]) == 64
