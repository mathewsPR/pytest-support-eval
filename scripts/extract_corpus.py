"""Extract the registered pytest PDF into page-preserving layout text."""

from __future__ import annotations

import hashlib
import json
import platform
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory

from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = PROJECT_ROOT / "corpus/raw/pytest-documentation.pdf"
SOURCE_MANIFEST_PATH = PROJECT_ROOT / "artifacts/manifests/corpus-source.json"
OUTPUT_DIR = PROJECT_ROOT / "corpus/extracted/pytest-documentation"
EXTRACTION_MANIFEST_PATH = PROJECT_ROOT / "artifacts/manifests/corpus-extraction.json"

EXTRACTION_OPTIONS = {
    "extraction_mode": "layout",
    "layout_mode_space_vertically": True,
    "layout_mode_strip_rotated": False,
}


def sha256_file(path: Path) -> str:
    """Compute a file's SHA-256 using bounded reads."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative_path(path: Path) -> str:
    """Return a portable project-relative path."""
    return path.relative_to(PROJECT_ROOT).as_posix()


def write_json(path: Path, data: dict) -> None:
    """Write a new JSON file without replacing an existing file."""
    with path.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(data, output, indent=2, ensure_ascii=False)
        output.write("\n")


def main() -> None:
    for required_path in (PDF_PATH, SOURCE_MANIFEST_PATH):
        if not required_path.is_file():
            raise SystemExit(f"Required file not found: {required_path}")

    for destination in (OUTPUT_DIR, EXTRACTION_MANIFEST_PATH):
        if destination.exists():
            raise SystemExit(
                f"Output already exists: {destination}\n"
                "Review the existing extraction before running again."
            )

    source_manifest = json.loads(SOURCE_MANIFEST_PATH.read_text(encoding="utf-8"))

    if source_manifest.get("schema_version") != 1:
        raise SystemExit("Unsupported source manifest schema version.")

    if source_manifest.get("local_path") != relative_path(PDF_PATH):
        raise SystemExit("Source manifest points to a different PDF.")

    actual_sha256 = sha256_file(PDF_PATH)
    if actual_sha256 != source_manifest.get("sha256"):
        raise SystemExit("PDF hash does not match the source manifest.")

    expected_pages = source_manifest.get("viewer_page_count")
    if type(expected_pages) is not int or expected_pages <= 0:
        raise SystemExit("Source manifest has an invalid viewer page count.")

    OUTPUT_DIR.parent.mkdir(parents=True, exist_ok=True)
    EXTRACTION_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Stage the large outputs. Failed extraction leaves no final output folder.
    with TemporaryDirectory(
        prefix="pytest-extraction-",
        dir=OUTPUT_DIR.parent,
    ) as temporary_directory:
        staged_dir = Path(temporary_directory) / "output"
        staged_dir.mkdir()
        pages_path = staged_dir / "pages.jsonl"
        review_path = staged_dir / "review.txt"

        empty_pages = []
        total_characters = 0

        with PDF_PATH.open("rb") as pdf_file:
            reader = PdfReader(pdf_file)

            if reader.is_encrypted:
                raise SystemExit("Encrypted PDFs are not supported by this script.")

            page_count = len(reader.pages)
            if page_count != expected_pages:
                raise SystemExit(
                    "Page count mismatch. Extraction stopped.\n"
                    f"Viewer: {expected_pages}; parser: {page_count}"
                )

            with (
                pages_path.open("x", encoding="utf-8", newline="\n") as pages_file,
                review_path.open("x", encoding="utf-8", newline="\n") as review_file,
            ):
                for page_number, page in enumerate(reader.pages, start=1):
                    try:
                        text = page.extract_text(**EXTRACTION_OPTIONS)
                    except Exception as exc:
                        raise SystemExit(
                            f"Extraction failed on PDF page {page_number}: {exc}"
                        ) from exc

                    if not isinstance(text, str):
                        raise SystemExit(
                            f"Unexpected extraction result on page {page_number}."
                        )

                    is_empty = not text.strip()
                    if is_empty:
                        empty_pages.append(page_number)

                    total_characters += len(text)

                    record = {
                        "schema_version": 1,
                        "corpus_id": source_manifest["corpus_id"],
                        "source_sha256": actual_sha256,
                        "pdf_page_number": page_number,
                        "text": text,
                        "character_count": len(text),
                        "is_empty": is_empty,
                    }
                    pages_file.write(json.dumps(record, ensure_ascii=False))
                    pages_file.write("\n")

                    review_file.write(f"===== PDF PAGE {page_number:04d} =====\n")
                    review_file.write(text)
                    review_file.write("\n\n")

                    if page_number % 50 == 0 or page_number == page_count:
                        print(f"Extracted {page_number}/{page_count} pages")

        if total_characters == 0 or len(empty_pages) == page_count:
            raise SystemExit("All pages are empty. Extraction was not published.")

        extraction_manifest = {
            "schema_version": 1,
            "corpus_id": source_manifest["corpus_id"],
            "source_manifest_path": relative_path(SOURCE_MANIFEST_PATH),
            "source_manifest_sha256": sha256_file(SOURCE_MANIFEST_PATH),
            "source_sha256": actual_sha256,
            "extractor": "pypdf",
            "extractor_version": version("pypdf"),
            "python_version": platform.python_version(),
            "script_sha256": sha256_file(Path(__file__).resolve()),
            "extraction_options": EXTRACTION_OPTIONS,
            "page_number_basis": "1-based physical PDF page, including front matter",
            "viewer_page_count": expected_pages,
            "parser_page_count": page_count,
            "page_record_count": page_count,
            "empty_page_numbers": empty_pages,
            "total_characters": total_characters,
            "pages_path": relative_path(OUTPUT_DIR / "pages.jsonl"),
            "pages_sha256": sha256_file(pages_path),
            "review_path": relative_path(OUTPUT_DIR / "review.txt"),
            "review_sha256": sha256_file(review_path),
            "extracted_at_utc": datetime.now(UTC).isoformat(),
            "extraction_status": "completed",
            "quality_review_status": "pending",
        }

        staged_dir.rename(OUTPUT_DIR)

        try:
            write_json(EXTRACTION_MANIFEST_PATH, extraction_manifest)
        except OSError as exc:
            raise SystemExit(
                "Text outputs were created, but manifest writing failed.\n"
                f"Outputs: {OUTPUT_DIR}\n"
                f"Error: {exc}\n"
                "Review these files before attempting another run."
            ) from exc

    print(f"Page records: {page_count}")
    print(f"Empty pages: {empty_pages}")
    print(f"Review text: {relative_path(OUTPUT_DIR / 'review.txt')}")
    print(f"Manifest: {relative_path(EXTRACTION_MANIFEST_PATH)}")
    print("Extraction completed. Quality review is still pending.")


if __name__ == "__main__":
    main()
