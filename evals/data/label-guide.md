# Retrieval label guide

A page should be labeled relevant when it contains documentation that directly helps answer the query.

Use page labels conservatively:

- Include pages that define the feature, option, fixture, or behavior named by the query.
- Include pages that contain the primary example needed to answer the query.
- Exclude pages that only mention the same word without explaining the concept.
- Prefer source page numbers from the processed corpus metadata.

Labels may be incomplete during development. When a retrieved page appears useful but is unlabeled, record it in `evals/data/relevance-pool.jsonl` before changing labels.
