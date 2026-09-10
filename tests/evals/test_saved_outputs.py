from pathlib import Path


def test_retrieval_baseline_artifact_exists() -> None:
    path = Path("artifacts/selected-runs/retrieval-development-baseline.json")

    assert path.exists()
