"""HTTP client for llama.cpp OpenAI-compatible chat completions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "http://127.0.0.1:8080"
DEFAULT_MODEL = "local-model"
DEFAULT_TIMEOUT_SECONDS = 120


class InferenceError(RuntimeError):
    """Raised when model inference fails."""


@dataclass(frozen=True)
class LlamaCppClient:
    """Small llama.cpp chat-completions client."""

    base_url: str = DEFAULT_BASE_URL
    model: str = DEFAULT_MODEL
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.0,
        max_tokens: int = 512,
    ) -> str:
        """Send chat messages and return the assistant text."""
        validate_messages(messages)

        if self.timeout_seconds < 1:
            raise InferenceError("timeout_seconds must be at least 1")

        if max_tokens < 1:
            raise InferenceError("max_tokens must be at least 1")

        if temperature < 0:
            raise InferenceError("temperature must be non-negative")

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }

        request = Request(
            f"{self.base_url.rstrip('/')}/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")
            raise InferenceError(
                f"llama.cpp request failed with HTTP {error.code}: {detail}"
            ) from error
        except TimeoutError as error:
            raise InferenceError("llama.cpp request timed out") from error
        except URLError as error:
            raise InferenceError(f"could not connect to llama.cpp: {error}") from error
        except OSError as error:
            raise InferenceError(f"llama.cpp request failed: {error}") from error
        except json.JSONDecodeError as error:
            raise InferenceError("llama.cpp returned invalid JSON") from error

        return parse_chat_response(response_payload)


def validate_messages(messages: list[dict[str, str]]) -> None:
    """Validate chat messages before sending them to llama.cpp."""
    if not messages:
        raise InferenceError("messages must not be empty")

    for index, message in enumerate(messages):
        role = message.get("role")
        content = message.get("content")

        if role not in {"system", "user", "assistant"}:
            raise InferenceError(f"messages[{index}].role is invalid")

        if not isinstance(content, str) or not content.strip():
            raise InferenceError(f"messages[{index}].content must be non-empty")


def parse_chat_response(response_payload: object) -> str:
    """Extract assistant text from an OpenAI-compatible chat response."""
    if not isinstance(response_payload, dict):
        raise InferenceError("llama.cpp response must be a JSON object")

    choices = response_payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise InferenceError("llama.cpp response has no choices")

    first_choice = choices[0]
    if not isinstance(first_choice, dict):
        raise InferenceError("llama.cpp response choice must be a JSON object")

    message = first_choice.get("message")
    if not isinstance(message, dict):
        raise InferenceError("llama.cpp response choice has no message")

    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise InferenceError("llama.cpp response message content is empty")

    return content.strip()
