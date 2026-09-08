from __future__ import annotations

from pytest_support.prompts import SYSTEM_PROMPT, build_messages, build_user_prompt


def make_context() -> dict[str, object]:
    return {
        "report_summary": (
            "Report: run-test\n"
            "Summary: 1 total, 0 passed, 1 failed, 0 errors, 0 skipped\n"
            "Tests:\n"
            "- tests/test_demo.py::test_bad | outcome=failed | "
            "phase=call | message=AssertionError: assert 1 == 2"
        ),
        "docs_query": "failed call AssertionError: assert 1 == 2",
        "docs": [
            {
                "citation": "pytest docs p. 42",
                "chunk_id": "pytest-documentation-p0042-c01",
                "score": 9.123,
                "text": "pytest shows assertion introspection for failing asserts.",
            }
        ],
    }


def test_system_prompt_sets_support_rules() -> None:
    assert "pytest support assistant" in SYSTEM_PROMPT
    assert "Do not invent files" in SYSTEM_PROMPT
    assert "Cite pytest documentation pages" in SYSTEM_PROMPT


def test_build_user_prompt_includes_context_and_answer_format() -> None:
    prompt = build_user_prompt(make_context())

    assert "Use the following context" in prompt
    assert "Report: run-test" in prompt
    assert "AssertionError: assert 1 == 2" in prompt
    assert "pytest docs p. 42" in prompt
    assert "Answer format:" in prompt
    assert "What happened" in prompt
    assert "Documentation citations" in prompt


def test_build_messages_returns_system_and_user_messages() -> None:
    messages = build_messages(make_context())

    assert messages == [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": build_user_prompt(make_context()),
        },
    ]
