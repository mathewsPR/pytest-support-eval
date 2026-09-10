from __future__ import annotations

from pytest_support.rag import answer_report


class FakeClient:
    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float,
        max_tokens: int,
    ) -> str:
        assert messages
        assert temperature == 0.0
        assert max_tokens == 128

        return (
            "What happened: the test failed.\n\n"
            "Likely cause: the assertion does not match.\n\n"
            "Suggested fix: update the expected value.\n\n"
            "Documentation citations: page 1."
        )


def test_rag_pipeline_uses_fixture_report_and_fake_client() -> None:
    answer = answer_report(
        "run-002",
        client=FakeClient(),
        top_k=2,
        max_tokens=128,
    )

    assert "What happened" in answer
    assert "Likely cause" in answer
    assert "Suggested fix" in answer
