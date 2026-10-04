# Antigravity Operating Rules for DocuTask-Agent

## 1. Architectural Boundaries
- Strict Layering: `src/api` -> `src/services` -> `src/core/models`.
- No inline prompt strings: Extract all system instructions and schema definitions into `src/agents/prompts/` and `src/schemas/`.
- Observability: Wrap all LLM and OCR operations in OpenTelemetry spans.

## 2. Testing & Evaluation Mandate
- Any change to OCR extraction logic requires a matching test fixture in `tests/fixtures/` and an evaluation case in `evals/data/golden_v1.jsonl`.
- PRs that degrade eval accuracy below 90% must be rejected.
