"""Command line interface for pytest support answers."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from pytest_support.inference import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    DEFAULT_TIMEOUT_SECONDS,
    InferenceError,
    LlamaCppClient,
)
from pytest_support.rag import answer_report
from pytest_support.tools import ToolError


def build_parser() -> argparse.ArgumentParser:
    """Build the pytest-support command line parser."""
    parser = argparse.ArgumentParser(
        prog="pytest-support",
        description="Generate pytest support answers from fixed report fixtures.",
    )
    parser.add_argument(
        "report_id",
        help="Report fixture ID, such as run-001, run-002, or run-003.",
    )
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=None,
        help="Directory containing report fixture JSON files.",
    )
    parser.add_argument(
        "--chunks",
        type=Path,
        default=None,
        help="Path to the processed corpus chunks JSONL file.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of documentation chunks to retrieve.",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="llama.cpp server base URL.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Model name sent to the llama.cpp OpenAI-compatible endpoint.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="llama.cpp request timeout in seconds.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=512,
        help="Maximum answer tokens requested from the model.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)

    client = LlamaCppClient(
        base_url=args.base_url,
        model=args.model,
        timeout_seconds=args.timeout,
    )

    try:
        answer = answer_report(
            args.report_id,
            client=client,
            reports_dir=args.reports_dir,
            chunks_path=args.chunks,
            top_k=args.top_k,
            max_tokens=args.max_tokens,
        )
    except (InferenceError, ToolError, ValueError) as error:
        parser.exit(status=1, message=f"error: {error}\n")

    print(answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
