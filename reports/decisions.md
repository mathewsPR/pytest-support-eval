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
## Relevance audit

We added `evals/harness/relevance_audit.py` to inspect development-set labels against the processed corpus and current retrieval results.

The audit report is saved at `artifacts/selected-runs/relevance-audit-development.md`.

This step is required before retrieval tuning because the current baseline has low hit rate, and we need to distinguish ranking failures from label/page/corpus extraction problems.

## Page aggregation retrieval experiment

We added page-level retrieval aggregation as an explicit retrieval mode. The original chunk mode remains available and remains the default.

Development-set comparison at `top_k=3`:

- Chunk mode: `hit_rate@3 = 0.200`
- Page aggregation mode: `hit_rate@3 = 0.200`

Page aggregation changed the retrieved pages but did not improve the current development hit rate. We are keeping it as an experimental mode because documentation citations are page-oriented, but we are not treating it as a quality improvement yet.

## Query normalization retrieval experiment

We added deterministic pytest-specific query expansion to reduce wording mismatch between user-style questions and documentation text.

Development-set comparison at `top_k=3`:

- Previous chunk retrieval: `hit_rate@3 = 0.200`
- Query-normalized chunk retrieval: `hit_rate@3 = 0.300`
- Query-normalized page aggregation: `hit_rate@3 = 0.300`

This is the first measured retrieval improvement on the development set. The change remains deterministic and offline, so it is suitable for CI-covered retrieval behavior.
