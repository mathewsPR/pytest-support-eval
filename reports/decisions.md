## Retrieval development baseline

We added `evals/runner.py` to run the retrieval evaluation against the development query set and the processed pytest documentation chunks.

Baseline run:

- Eval data: `evals/data/development.jsonl`
- Chunks: `corpus/processed/pytest-documentation/chunks.jsonl`
- Metric: hit rate at k
- k: 3
- Items: 10
- Hits: 2
- Hit rate@3: 0.200
- Output artifact: `artifacts/selected-runs/retrieval-development-baseline.json`

Definition: a query is counted as a hit when at least one retrieved source page matches at least one labeled relevant page.

Interpretation: this is a starting baseline, not a release-quality retrieval score. The current retriever is lexical and exact-token based, so it misses queries where the user wording differs from the documentation wording. The result gives us a concrete baseline before retrieval improvements.