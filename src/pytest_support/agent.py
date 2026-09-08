"""Agent runner for pytest support answers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from pytest_support.rag import answer_report


class ChatClient(Protocol):
    """Minimal chat client interface used by the support agent."""

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.0,
        max_tokens: int = 512,
    ) -> str:
        """Return assistant text for chat messages."""


@dataclass(frozen=True)
class AgentRun:
    """Result of one support-agent run."""

    report_id: str
    answer: str


@dataclass(frozen=True)
class PytestSupportAgent:
    """Small orchestration wrapper around the RAG answer path."""

    client: ChatClient | None = None
    reports_dir: Path | None = None
    chunks_path: Path | None = None
    top_k: int = 3
    max_tokens: int = 512

    def run(self, report_id: str) -> AgentRun:
        """Generate one support answer for a report fixture."""
        answer = answer_report(
            report_id,
            client=self.client,
            reports_dir=self.reports_dir,
            chunks_path=self.chunks_path,
            top_k=self.top_k,
            max_tokens=self.max_tokens,
        )

        return AgentRun(report_id=report_id, answer=answer)
