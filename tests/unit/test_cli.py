from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from pytest_support import cli
from pytest_support.tools import ToolError


def test_build_parser_accepts_report_id() -> None:
    args = cli.build_parser().parse_args(["run-002"])

    assert args.report_id == "run-002"
    assert args.top_k == 3
    assert args.max_tokens == 512


def test_main_calls_answer_report_with_cli_options(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
) -> None:
    captured: dict[str, Any] = {}

    def fake_answer_report(report_id: str, **kwargs: Any) -> str:
        captured["report_id"] = report_id
        captured.update(kwargs)
        return "Generated support answer."

    monkeypatch.setattr(cli, "answer_report", fake_answer_report)

    reports_dir = tmp_path / "reports"
    chunks_path = tmp_path / "chunks.jsonl"

    exit_code = cli.main(
        [
            "run-002",
            "--reports-dir",
            str(reports_dir),
            "--chunks",
            str(chunks_path),
            "--top-k",
            "2",
            "--base-url",
            "http://localhost:8080",
            "--model",
            "qwen2.5-3b",
            "--timeout",
            "120",
            "--max-tokens",
            "256",
        ]
    )

    assert exit_code == 0
    assert capsys.readouterr().out == "Generated support answer.\n"
    assert captured["report_id"] == "run-002"
    assert captured["reports_dir"] == reports_dir
    assert captured["chunks_path"] == chunks_path
    assert captured["top_k"] == 2
    assert captured["max_tokens"] == 256
    assert captured["client"].base_url == "http://localhost:8080"
    assert captured["client"].model == "qwen2.5-3b"
    assert captured["client"].timeout_seconds == 120


def test_main_returns_error_for_tool_failure(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_answer_report(_report_id: str, **_kwargs: Any) -> str:
        raise ToolError("unknown report_id: missing")

    monkeypatch.setattr(cli, "answer_report", fake_answer_report)

    with pytest.raises(SystemExit) as error:
        cli.main(["missing"])

    assert error.value.code == 1
    assert capsys.readouterr().err == "error: unknown report_id: missing\n"


def test_main_returns_error_for_invalid_runtime_option(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_answer_report(_report_id: str, **_kwargs: Any) -> str:
        raise ValueError("top_k must be at least 1")

    monkeypatch.setattr(cli, "answer_report", fake_answer_report)

    with pytest.raises(SystemExit) as error:
        cli.main(["run-002", "--top-k", "0"])

    assert error.value.code == 1
    assert capsys.readouterr().err == "error: top_k must be at least 1\n"
