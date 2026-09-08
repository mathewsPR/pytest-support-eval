"""RAG answer generation for pytest support reports."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from pytest_support.context import build_context
from pytest_support.inference import LlamaCppClient
from pytest_support.prompts import build_messages


class ChatClient(Protocol):
    """Minimal chat client interface used by answer generation."""

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.0,
        max_tokens: int = 512,
    ) -> str:
        """Return assistant text for chat messages."""


def answer_report(
    report_id: str,
    *,
    client: ChatClient | None = None,
    reports_dir: Path | None = None,
    chunks_path: Path | None = None,
    top_k: int = 3,
    max_tokens: int = 512,
) -> str:
    """Generate a support answer for one test-report fixture."""
    context = build_context(
        report_id,
        reports_dir=reports_dir,
        chunks_path=chunks_path,
        top_k=top_k,
    )
    messages = build_messages(context)

    if client is None:
        client = LlamaCppClient()

    return client.chat(messages, temperature=0.0, max_tokens=max_tokens)
