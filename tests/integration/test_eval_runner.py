from pathlib import Path

from evals.runner import run_retrieval_eval


def test_eval_runner_produces_baseline_shape_with_fixture_corpus() -> None:
    run = run_retrieval_eval(
        eval_data=Path("tests/fixtures/evals/small-development.jsonl"),
        chunks=Path("tests/fixtures/chunks/small-chunks.jsonl"),
        top_k=2,
    )

    assert run.item_count == 2
    assert run.top_k == 2
    assert 0 <= run.hit_count <= run.item_count
    assert 0.0 <= run.hit_rate <= 1.0
    assert len(run.results) == run.item_count
