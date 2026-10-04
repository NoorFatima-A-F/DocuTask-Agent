# DocuTask-Agent System Context & Constraints

## System Boundaries
- `src/api`: FastAPI routes, request validation, dependency injection.
- `src/core`: Settings, telemetry instrumentation, database engines.
- `src/services`: Deterministic business logic (OCR adapters, image preprocessing).
- `src/agents`: Non-deterministic LLM tool routing, prompt assemblies, schema extractors.
- `evals`: Deterministic golden datasets and offline accuracy evaluation suites.

## Quality Invariants
- Pydantic v2 schemas for all external inputs and tool outputs (`src/schemas/`).
- Zero secret leakage: No credentials logged in stdout or telemetry spans.
- Test coverage must maintain >= 80% on all deterministic service modules.
