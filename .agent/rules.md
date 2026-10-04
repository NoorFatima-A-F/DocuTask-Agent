# Agent Engineering Protocol

## Architectural Constraints
1. Clean Architecture: Maintain strict separation between `core/models`, `services/ocr`, `services/extraction`, and `api/`.
2. Type Safety: All domain models and API contracts must use Pydantic v2 schemas with explicit Field constraints.
3. Observability: Every agent workflow must emit structured OpenTelemetry spans with document ID, duration, and token usage attributes.

## Verification Checklist Prior to PR
- Run `make lint` to confirm zero Ruff and Mypy violations.
- Run `make test` to confirm unit test coverage >= 80%.
- Run `make eval` to verify extraction accuracy >= 90% against `evals/data/golden_v1.jsonl`.
