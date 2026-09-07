import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_MANIFEST = PROJECT_ROOT / "artifacts/manifests/corpus-source.json"
EXTRACTION_MANIFEST = PROJECT_ROOT / "artifacts/manifests/corpus-extraction.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_manifest_records_expected_pytest_pdf() -> None:
    manifest = load_json(SOURCE_MANIFEST)

    assert manifest["schema_version"] == 1
    assert manifest["corpus_id"] == "pytest-documentation"
    assert manifest["source_url"] == (
        "https://media.readthedocs.org/pdf/pytest/latest/pytest.pdf"
    )
    assert manifest["source_url_version_selector"] == "latest"
    assert manifest["local_path"] == "corpus/raw/pytest-documentation.pdf"
    assert manifest["sha256"] == (
        "015b1641be533eff8174a1a1b17663ba9178d8f5565b102a7a11becb4dd23b77"
    )
    assert manifest["documentation_release"] == "9.2"
    assert manifest["viewer_page_count"] == 571
    assert manifest["license_verification_status"] == "pending"


def test_extraction_manifest_matches_source_manifest() -> None:
    source = load_json(SOURCE_MANIFEST)
    extraction = load_json(EXTRACTION_MANIFEST)

    assert extraction["schema_version"] == 1
    assert extraction["corpus_id"] == source["corpus_id"]
    assert extraction["source_sha256"] == source["sha256"]
    assert extraction["viewer_page_count"] == source["viewer_page_count"]
    assert extraction["parser_page_count"] == 571
    assert extraction["page_record_count"] == 571
    assert extraction["empty_page_numbers"] == [2]
    assert extraction["extraction_status"] == "completed"
    assert extraction["quality_review_status"] == "pending"


def test_extraction_manifest_tracks_ignored_outputs() -> None:
    extraction = load_json(EXTRACTION_MANIFEST)

    assert extraction["pages_path"] == (
        "corpus/extracted/pytest-documentation/pages.jsonl"
    )
    assert extraction["review_path"] == (
        "corpus/extracted/pytest-documentation/review.txt"
    )
    assert len(extraction["pages_sha256"]) == 64
    assert len(extraction["review_sha256"]) == 64
