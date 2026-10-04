# ADR 0003: Autonomous Evaluation Harness for LLM Drift

## Status
Accepted

## Context
Non-deterministic LLMs and OCR engines drift over time due to upstream model revisions, document layout variances, and visual noise. Traditional unit tests with static string mocks fail to detect semantic hallucination, confidence scoring degradation, or schema boundary breakage.

## Decision
Implement a standalone evaluation harness (`evals/`) executed via `cli/agent_cli.py`:
1. **Gold-Standard Benchmarks:** Uses ground-truth invoice datasets (`invoices_gold.json`) to calculate schema conformance and hallucination rates.
2. **Adversarial OCR Fuzzing:** Injects common optical character recognition errors into payloads to verify Pydantic self-healing logic.
3. **CI Summary Telemetry:** Automatically compiles evaluation outputs into `$GITHUB_STEP_SUMMARY` on Pull Requests.

## Consequences
- **Positive:** Catches model prompt regressions before deployment without blocking standard unit test execution.
- **Negative:** Requires maintaining ground-truth datasets for each document category.
