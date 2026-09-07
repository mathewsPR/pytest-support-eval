"""Create citation-preserving text chunks from extracted pytest documentation pages."""

from __future__ import annotations

import hashlib
import json
import platform
import re
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SOURCE_MANIFEST_PATH = PROJECT_ROOT / "artifacts/manifests/corpus-source.json"
EXTRACTION_MANIFEST_PATH = PROJECT_ROOT / "artifacts/manifests/corpus-extraction.json"
PAGES_PATH = PROJECT_ROOT / "corpus/extracted/pytest-documentation/pages.jsonl"

OUTPUT_DIR = PROJECT_ROOT / "corpus/processed/pytest-documentation"
CHUNKS_PATH = OUTPUT_DIR / "chunks.jsonl"
CHUNK_MANIFEST_PATH = PROJECT_ROOT / "artifacts/manifests/corpus-chunks.json"

TARGET_CHARS = 1800
OVERLAP_CHARS = 250
MIN_CHARS = 350


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def split_paragraphs(text: str) -> list[str]:
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text)]
    return [part for part in paragraphs if part]


def split_long_text(text: str, target_chars: int) -> list[str]:
    parts: list[str] = []
    start = 0

    while start < len(text):
        end = min(start + target_chars, len(text))

        if end < len(text):
            newline = text.rfind("\n", start, end)
            sentence = max(
                text.rfind(". ", start, end),
                text.rfind("? ", start, end),
                text.rfind("! ", start, end),
            )
            split_at = max(newline, sentence)
            if split_at > start + target_chars // 2:
                end = split_at + 1

        part = text[start:end].strip()
        if part:
            parts.append(part)

        start = end

    return parts


def chunk_page(page_record: dict, corpus_id: str) -> list[dict]:
    page_number = page_record["pdf_page_number"]
    text = normalize_text(page_record["text"])

    if len(text) < 20:
        return []

    paragraphs = split_paragraphs(text)
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        if len(paragraph) > TARGET_CHARS:
            if current.strip():
                chunks.append(current.strip())
                current = ""
            chunks.extend(split_long_text(paragraph, TARGET_CHARS))
            continue

        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph
        if len(candidate) <= TARGET_CHARS:
            current = candidate
        else:
            if current.strip():
                chunks.append(current.strip())
            current = paragraph

    if current.strip():
        chunks.append(current.strip())

    merged: list[str] = []
    for chunk in chunks:
        if merged and len(chunk) < MIN_CHARS:
            merged[-1] = f"{merged[-1]}\n\n{chunk}".strip()
        else:
            merged.append(chunk)

    records = []
    for chunk_index, chunk_text in enumerate(merged, start=1):
        if chunk_index > 1 and OVERLAP_CHARS > 0:
            previous_tail = merged[chunk_index - 2][-OVERLAP_CHARS:].strip()
            chunk_text = f"{previous_tail}\n\n{chunk_text}".strip()

        records.append(
            {
                "schema_version": 1,
                "corpus_id": corpus_id,
                "chunk_id": (f"{corpus_id}-p{page_number:04d}-c{chunk_index:02d}"),
                "source_page_number": page_number,
                "source_page_start": page_number,
                "source_page_end": page_number,
                "text": chunk_text,
                "character_count": len(chunk_text),
            }
        )

    return records


def load_pages(path: Path) -> list[dict]:
    pages = []
    with path.open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            if record["pdf_page_number"] != line_number:
                raise SystemExit(
                    "Unexpected page numbering in extracted pages.\n"
                    f"Line: {line_number}\n"
                    f"Record page: {record['pdf_page_number']}"
                )
            pages.append(record)
    return pages


def main() -> None:
    if not PAGES_PATH.is_file():
        raise SystemExit(f"Extracted pages not found: {PAGES_PATH}")

    if OUTPUT_DIR.exists():
        raise SystemExit(f"Output directory already exists: {OUTPUT_DIR}")

    if CHUNK_MANIFEST_PATH.exists():
        raise SystemExit(f"Chunk manifest already exists: {CHUNK_MANIFEST_PATH}")

    source_manifest = load_json(SOURCE_MANIFEST_PATH)
    extraction_manifest = load_json(EXTRACTION_MANIFEST_PATH)

    corpus_id = source_manifest["corpus_id"]
    if extraction_manifest["corpus_id"] != corpus_id:
        raise SystemExit("Corpus ID mismatch between source and extraction manifests.")

    pages = load_pages(PAGES_PATH)
    expected_pages = extraction_manifest["page_record_count"]

    if len(pages) != expected_pages:
        raise SystemExit(f"Expected {expected_pages} page records, found {len(pages)}.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=False)

    chunk_count = 0
    empty_pages = 0
    pages_with_chunks = set()

    with CHUNKS_PATH.open("x", encoding="utf-8", newline="\n") as output:
        for page in pages:
            page_chunks = chunk_page(page, corpus_id)
            if not page_chunks:
                empty_pages += 1
                continue

            for chunk in page_chunks:
                output.write(json.dumps(chunk, ensure_ascii=False))
                output.write("\n")
                chunk_count += 1
                pages_with_chunks.add(chunk["source_page_number"])

    manifest = {
        "schema_version": 1,
        "corpus_id": corpus_id,
        "source_sha256": source_manifest["sha256"],
        "extraction_manifest_path": EXTRACTION_MANIFEST_PATH.relative_to(
            PROJECT_ROOT
        ).as_posix(),
        "extraction_manifest_sha256": sha256_file(EXTRACTION_MANIFEST_PATH),
        "pages_path": PAGES_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "pages_sha256": sha256_file(PAGES_PATH),
        "chunks_path": CHUNKS_PATH.relative_to(PROJECT_ROOT).as_posix(),
        "chunks_sha256": sha256_file(CHUNKS_PATH),
        "chunking_strategy": "single-page paragraph chunks with local overlap",
        "target_chars": TARGET_CHARS,
        "overlap_chars": OVERLAP_CHARS,
        "min_chars": MIN_CHARS,
        "source_page_count": len(pages),
        "pages_with_chunks": len(pages_with_chunks),
        "empty_pages": empty_pages,
        "chunk_count": chunk_count,
        "python_version": platform.python_version(),
        "script_sha256": sha256_file(Path(__file__).resolve()),
        "created_at_utc": datetime.now(UTC).isoformat(),
        "chunking_status": "completed",
    }

    with CHUNK_MANIFEST_PATH.open("x", encoding="utf-8", newline="\n") as output:
        json.dump(manifest, output, indent=2, ensure_ascii=False)
        output.write("\n")

    print(f"Chunks: {chunk_count}")
    print(f"Pages with chunks: {len(pages_with_chunks)}")
    print(f"Empty pages: {empty_pages}")
    print(f"Chunks file: {CHUNKS_PATH.relative_to(PROJECT_ROOT).as_posix()}")
    print(f"Manifest: {CHUNK_MANIFEST_PATH.relative_to(PROJECT_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
