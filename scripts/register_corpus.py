"""Register the locally downloaded pytest PDF without modifying it."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = PROJECT_ROOT / "corpus/raw/pytest-documentation.pdf"
MANIFEST_PATH = PROJECT_ROOT / "artifacts/manifests/corpus-source.json"

EXPECTED_SHA256 = "015b1641be533eff8174a1a1b17663ba9178d8f5565b102a7a11becb4dd23b77"
SOURCE_URL = "https://media.readthedocs.org/pdf/pytest/latest/pytest.pdf"


def sha256_file(path: Path) -> str:
    """Compute SHA-256 without loading the entire file into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    if not PDF_PATH.is_file():
        raise SystemExit(f"PDF not found: {PDF_PATH}")

    actual_sha256 = sha256_file(PDF_PATH)
    if actual_sha256 != EXPECTED_SHA256:
        raise SystemExit(
            "PDF hash mismatch. Source registration stopped.\n"
            f"Expected: {EXPECTED_SHA256}\n"
            f"Actual:   {actual_sha256}"
        )

    manifest = {
        "schema_version": 1,
        "corpus_id": "pytest-documentation",
        "source_url": SOURCE_URL,
        "source_url_version_selector": "latest",
        "local_path": PDF_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "sha256": actual_sha256,
        "size_bytes": PDF_PATH.stat().st_size,
        "documentation_release": "9.2",
        "documentation_release_basis": "User inspected PDF cover",
        "viewer_page_count": 571,
        "viewer_page_count_basis": "User inspected PDF viewer",
        "parser_page_count": None,
        "registered_at_utc": datetime.now(UTC).isoformat(),
        "downloaded_at_utc": None,
        "license_verification_status": "pending",
        "extraction_status": "not_started",
    }

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        with MANIFEST_PATH.open("x", encoding="utf-8", newline="\n") as output:
            json.dump(manifest, output, indent=2, ensure_ascii=False)
            output.write("\n")
    except FileExistsError:
        raise SystemExit(
            f"Manifest already exists: {MANIFEST_PATH}\n"
            "Review the existing record before replacing it."
        ) from None

    print(f"Registered: {manifest['local_path']}")
    print(f"SHA-256: {actual_sha256}")
    print("Documentation release: 9.2 (user-reported)")
    print("Viewer page count: 571 (parser verification pending)")
    print(f"Manifest: {MANIFEST_PATH.relative_to(PROJECT_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
