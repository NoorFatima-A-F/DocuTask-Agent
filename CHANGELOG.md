# Changelog

All notable changes to **DocuTask Agent** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased] - remediation

### Changed (breaking)
- Extraction no longer fabricates data. A missing Gemini key, any non-200 response, a timeout,
  or unparseable output now fails with a typed error (`LLM_*`), an HTTP 5xx, and a persisted
  `FAILED` extraction record. OCR failures raise `OCR_ENGINE_UNAVAILABLE` (503), `OCR_FAILED`
  (500) or `OCR_NO_TEXT` (422) instead of storing placeholder text.
- Error responses for these failures carry `errors: {"error_code": "<CODE>"}`.
- `ExtractionResponse.result` gains `status`, `error_code`, `error_message`; `structured_json`
  and `confidence` are now nullable. `statistics.estimated_cost` is null when model pricing is unknown.
- OCR `confidence` / `average_confidence` are null when the engine reports no word confidences.
- `/readyz` returns 503 with `reasons` when tesseract is missing, or (outside dev/test) no LLM key is set.
- Removed `/health/metrics` (returned hard-coded latency/queue numbers) and `/health/healthz`, `/health/readyz` aliases.
- The Gemini API key is sent in the `x-goog-api-key` header instead of the URL.

### Removed
- Fake OCR provider classes (Textract, Document AI, Azure, Paddle), the shadowed `app/ocr/providers.py`,
  `app/ai/registry.py`, `app/ai/factory.py`, and `app/validation/` (benchmarks built on fabricated output).

### Database
- Alembic `007_extraction_failure_status`: `ai_extractions.status/error_code/error_message`;
  nullable `structured_json`, `raw_response`, `confidence`, `estimated_cost`, `extracted_texts.confidence`.

---

## [1.0.0] - 2026-09-21

### Added
- **AI Document Extraction Engine**:
  - Multimodal layout and text extraction with Pydantic structured output models.
  - Multi-provider support (Google Gemini 1.5/2.0 Flash/Pro, Claude, OpenAI).
  - Field-level confidence calibration and character-span grounding.
- **OCR & Document Ingestion Pipeline**:
  - Multi-page PDF, PNG, and TIFF processing with table structure recognition.
  - Asynchronous background task processing with FastAPI and Redis queues.
- **Authentication & RBAC Security**:
  - JWT authentication using HMAC-SHA256 with role-based access control.
  - Granular permission scopes (`Viewer`, `Operator`, `Auditor`, `Admin`).
- **Human-in-the-Loop (HITL) Workflow**:
  - Automatic exception routing for extractions below confidence threshold ($< 0.85$).
  - Review queue with change auditing and correction tracking.
- **CI/CD Security & Automation**:
  - CodeQL automated SAST security analysis ([`.github/workflows/codeql.yml`](.github/workflows/codeql.yml)).
  - Dependabot automated weekly vulnerability scanning ([`.github/dependabot.yml`](.github/dependabot.yml)).
  - Comprehensive quality gate enforcing tests, linting, type checks, and AST analysis.
- **Repository Governance**:
  - Added [SECURITY.md](SECURITY.md), [CONTRIBUTING.md](CONTRIBUTING.md), [CODEOWNERS](.github/CODEOWNERS), and issue/PR templates.

### Fixed
- **Dependency Vulnerabilities**:
  - Upgraded and pinned `rsa>=4.9` to remediate Bleichenbacher timing attacks (CVE-2020-25658).
  - Deprecated and removed unpatched `python-ecdsa` to eliminate Minerva timing side-channel attacks (CVE-2024-23342 / GHSA-wj6h-64fc-37mp), consolidating all cryptographic operations onto constant-time `cryptography>=43.0.3` and `python-jose[cryptography]`.
  - Upgraded `cryptography>=43.0.3` and `fastapi>=0.115.0`.
  - Upgraded `vitest>=4.1.11` and `@vitest/mocker>=4.1.11` to resolve path traversal / arbitrary file read vulnerability (CVE-2026-84373 / GHSA-82fw-gwwq-j7x9).

### Security
- **Credential Exposure Remediation**:
  - Completely eliminated vendor-like token fixtures from test suites and documentation.
  - Implemented centralized configuration management in `app/core/config.py` using `pydantic-settings`.
  - Created clean `.env.example` with zero credentials or mock tokens.
  - Established Git history sanitization guide and verification procedures in `docs/security/git-history-cleanup.md`.
