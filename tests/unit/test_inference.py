from __future__ import annotations

import json
from typing import Any
from urllib.error import URLError
from urllib.request import Request

import pytest

from pytest_support.inference import (
    InferenceError,
    LlamaCppClient,
    parse_chat_response,
    validate_messages,
)


class FakeResponse:
    def __init__(self, payload: object) -> None:
        self.payload = payload

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def test_parse_chat_response_returns_assistant_content() -> None:
    assert (
        parse_chat_response(
            {"choices": [{"message": {"content": "  Helpful answer.  "}}]}
        )
        == "Helpful answer."
    )


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"choices": []},
        {"choices": [None]},
        {"choices": [{"message": None}]},
        {"choices": [{"message": {"content": ""}}]},
    ],
)
def test_parse_chat_response_rejects_malformed_payloads(payload: object) -> None:
    with pytest.raises(InferenceError):
        parse_chat_response(payload)


def test_validate_messages_accepts_chat_messages() -> None:
    validate_messages(
        [
            {"role": "system", "content": "Rules"},
            {"role": "user", "content": "Question"},
        ]
    )


@pytest.mark.parametrize(
    "messages",
    [
        [],
        [{"role": "tool", "content": "Question"}],
        [{"role": "user", "content": "   "}],
    ],
)
def test_validate_messages_rejects_invalid_messages(
    messages: list[dict[str, str]],
) -> None:
    with pytest.raises(InferenceError):
        validate_messages(messages)


def test_client_posts_openai_compatible_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    def fake_urlopen(request: Request, timeout: int) -> FakeResponse:
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        return FakeResponse(
            {"choices": [{"message": {"content": "Use the client fixture."}}]}
        )

    monkeypatch.setattr("pytest_support.inference.urlopen", fake_urlopen)

    client = LlamaCppClient(
        base_url="http://localhost:8080/",
        model="qwen2.5-3b",
        timeout_seconds=120,
    )
    answer = client.chat(
        [{"role": "user", "content": "Explain this pytest error."}],
        max_tokens=256,
    )

    assert answer == "Use the client fixture."
    assert captured["url"] == "http://localhost:8080/v1/chat/completions"
    assert captured["timeout"] == 120
    assert captured["payload"] == {
        "model": "qwen2.5-3b",
        "messages": [{"role": "user", "content": "Explain this pytest error."}],
        "temperature": 0.0,
        "max_tokens": 256,
        "stream": False,
    }


@pytest.mark.parametrize(
    "error",
    [
        TimeoutError("timed out"),
        URLError("connection refused"),
    ],
)
def test_client_wraps_connection_failures(
    monkeypatch: pytest.MonkeyPatch,
    error: Exception,
) -> None:
    def fake_urlopen(request: Request, timeout: int) -> FakeResponse:
        raise error

    monkeypatch.setattr("pytest_support.inference.urlopen", fake_urlopen)

    client = LlamaCppClient()

    with pytest.raises(InferenceError):
        client.chat([{"role": "user", "content": "Question"}])


def test_client_rejects_invalid_runtime_options() -> None:
    client = LlamaCppClient(timeout_seconds=0)

    with pytest.raises(InferenceError, match="timeout"):
        client.chat([{"role": "user", "content": "Question"}])
