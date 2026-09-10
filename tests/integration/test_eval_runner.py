from pathlib import Path

from evals.runner import run_retrieval_eval


def test_eval_runner_produces_baseline_shape() -> None:
    run = run_retrieval_eval(
        eval_data=Path("evals/data/development.jsonl"),
        chunks=Path("corpus/processed/pytest-documentation/chunks.jsonl"),
        top_k=3,
    )

    assert run.item_count == 10
    assert run.top_k == 3
    assert 0 <= run.hit_count <= run.item_count
    assert 0.0 <= run.hit_rate <= 1.0
    assert len(run.results) == run.item_count
