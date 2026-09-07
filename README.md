# Pytest Support Evaluation

A reproducible evaluation project for a small local RAG application and a two-tool agent built around pytest documentation and report fixtures.

## Project status

Early development. Results, metrics, and conclusions will be added only after the corresponding experiments are completed.

## Objectives

- Build a small pytest-support RAG application.
- Build an agent restricted to two approved tools.
- Compare two local language models served through `llama.cpp`.
- Evaluate retrieval, answer quality, tool use, safety, and performance.
- Validate a Gemini-based semantic judge against human-reviewed outputs.
- Separate deterministic release checks from diagnostic semantic metrics.
- Document uncertainty, failures, costs, and study limitations.

## Planned evaluation areas

- Retrieval quality
- RAG answer quality
- Agent tool-call accuracy
- Agent trajectory and task success
- Abstention behavior
- Prompt-injection resistance
- Guardrail performance
- Judge agreement and bias probes
- Latency, throughput, timeouts, and context handling
- Regression and controlled-fault testing

## Technology

- Windows 11
- Git Bash
- Python 3.11
- `llama.cpp`
- pytest
- Ragas
- DeepEval
- Arize Phoenix
- Promptfoo
- Gemini API

Tools will be introduced incrementally. Dependency versions will be recorded after compatibility checks.

## Current limitations

This project uses a small, deliberately designed dataset, one primary human annotator, two local models, one documentation domain, and three report fixtures. The local pilot will not represent production traffic or establish production readiness.

Semantic metrics and model-based judging will be treated as diagnostic unless supported by separate validation evidence. Deterministic checks will remain the hard gates for tool permissions, report facts, citation validity, schemas, context limits, and termination behavior.

## Setup

The project uses Python 3.11 in a local virtual environment.

```bash
py -3.11 -m venv .venv
source .venv/Scripts/activate
python --version