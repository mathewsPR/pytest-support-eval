"""Prompt templates for pytest support answers."""

from __future__ import annotations

from typing import Any

from pytest_support.context import format_context

SYSTEM_PROMPT = """\
You are a pytest support assistant.

Your job is to explain pytest failures using only the provided test report and
retrieved pytest documentation context.

Rules:
- Identify the failing or errored test.
- Explain the likely cause in plain language.
- Cite pytest documentation pages when documentation is used.
- Suggest a minimal next action.
- If the report has no failures or errors, say the test run passed.
- Do not invent files, fixtures, command output, or documentation.
"""


def build_user_prompt(context: dict[str, Any]) -> str:
    """Build the user prompt from prepared context."""
    return f"""\
Use the following context to write a concise pytest support answer.

{format_context(context)}

Answer format:
1. What happened
2. Likely cause
3. Suggested fix
4. Documentation citations
"""


def build_messages(context: dict[str, Any]) -> list[dict[str, str]]:
    """Build chat-style messages for the model client."""
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": build_user_prompt(context),
        },
    ]
