# Changelog

All notable changes to **DocuTask Agent** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-11-08

Remediation release: removes fabricated behaviour and simulated features, and makes every
claim in the README measurable. Upgrade notes: run `alembic upgrade head` (migrations 007-009);
set `JWT_SECRET` outside development/test; set `REDIS_URL` and run a worker for jobs.

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
- `GEMINI_MODEL` (default `gemini-3.8-flash`) is the only source of the model ID; the
  retired `gemini-1.5-flash` default is gone. `GEMINI_API_KEY` takes precedence over `GOOGLE_API_KEY`.
- Gemini calls use structured output (`responseSchema` derived from the Pydantic models) and
  a shared, lifespan-scoped HTTP client with explicit timeouts.
- Cost comes from a dated per-model pricing table; unlisted models report `estimated_cost: null`.
- Extraction schemas: receipt/purchase-order line items, bank transactions and resume education
  are now typed objects instead of free-form dicts.
- Removed unused `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` settings.

- Confidence is now evidence-based (`app/ai/confidence.py`): grounding of each value in the OCR
  text, required-field completeness, arithmetic/date consistency checks, and OCR word confidence.
  The old non-null-field ratio with a 0.5 floor is gone. `result.confidence_details` explains the score.
- Extractions below `CONFIDENCE_THRESHOLD_HITL`, with a missing/ungrounded required field, or with a
  failed consistency check get status `NEEDS_REVIEW` (document status `EXTRACTION_NEEDS_REVIEW`).
- `result.final_json` is the data to treat as final: set for auto-accepted results and after reviewer
  approval, null otherwise. `AIValidator.validate` now returns only the validated dict.
- Invoices gain an optional `subtotal` field.

- Startup fails when `ENVIRONMENT` is not `development`/`test` and `JWT_SECRET` is the built-in
  default or shorter than 32 bytes. Tokens without `exp`/`iat` claims are rejected.

- API trimmed to the document path (914 -> 36 operations). Only `/healthz`, `/readyz` and
  auth login/register/refresh are public; logout requires an access token. `/health/live`,
  `/health/ready` and `/api/v1/health` are gone. See `docs/remediation/deletions.md`.
- Background jobs run on Celery + Redis instead of an in-process asyncio queue. New API:
  `POST /api/v1/jobs` (202, idempotent: resubmissions or a reused `Idempotency-Key` return the
  existing job with 200), `GET /api/v1/jobs`, `GET /api/v1/jobs/{id}`, `POST /api/v1/jobs/{id}/retry`,
  `GET /api/v1/jobs/failed` (admin). Job statuses: QUEUED, RUNNING, RETRYING, COMPLETED,
  NEEDS_REVIEW, FAILED, with `error_code`/`last_error` on failure. Only transient LLM errors are
  retried (3 retries, exponential backoff honouring Retry-After). Without `REDIS_URL`, submission
  fails with 503 `QUEUE_UNAVAILABLE`.
- Removed `/jobs/submit`, `/jobs/extract/{id}`, `/jobs/dlq/*`, `/jobs/{id}/status` (returned a
  hard-coded 100% progress) and `DELETE /jobs/{id}`.
- `/readyz` also reports `QUEUE_UNAVAILABLE` when Redis is unset (outside dev/test) or unreachable.
- `postgres://` / `postgresql://` database URLs are rewritten to the asyncpg driver.
- docker-compose: secrets are required from the environment (no hard-coded JWT secret or DB
  password), a `worker` service was added, Postgres/Redis ports are no longer published.

### Changed (frontend)
- The web UI was rewritten against the real API (~1.3k lines including tests, replacing ~6k lines of simulated
  screens). Upload -> `POST /jobs` -> polling `GET /jobs/{id}` until COMPLETED / NEEDS_REVIEW /
  FAILED; results show per-field grounding ("Found in document" / "Not found in document"),
  failed consistency checks and OCR confidence; NEEDS_REVIEW results are labelled not final.
  Reviewers get a queue and a review page (document preview, OCR text, editable fields,
  approve with typed corrections, reject with reason). Failures show the backend error code.
- Removed: demo job/document IDs, hard-coded fallback telemetry (e.g. 1,284 documents, 94.2%
  confidence), simulated upload queue, DLQ screen and `/runtime/*` calls, command palette.
- Tailwind is compiled at build time (no CDN script). Tests: Vitest + Testing Library unit
  tests and Playwright end-to-end tests against the production build with a stubbed API.

### Evaluation
- New synthetic dataset (36 documents, `evals/generate.py`, `evals/SOURCES.md`) and
  `evals/run_eval.py` with `routing` (offline, CI gate), `live` (tesseract + Gemini) and `replay`
  modes. Routing gate: 0/156 corrupted extractions auto-accepted, 36/36 correct ones accepted.
- Fixed (found by the eval): values containing digits (invoice/account numbers, addresses) were
  fuzzy-matched as grounded; they now require an exact match.
- The previous `evals/` harness and golden file were removed.
- README rewritten to describe only implemented behaviour; live accuracy is marked unmeasured.

### Build, CI and tooling
- Multi-stage Docker image: Node 20 builds the UI, Python 3.12 runtime with tesseract, non-root
  user, port 7860. Entrypoint roles: `web` (runs `alembic upgrade head`, then uvicorn), `worker`,
  `all-in-one` (local Redis + worker + web for single-container hosting).
- The schema is managed only by Alembic; startup no longer calls `create_all`. A test asserts the
  migrations produce exactly the ORM schema; CI runs upgrade/downgrade/upgrade on Postgres.
- Python 3.12 everywhere (Docker, CI, Render, pyproject).
- Ruff: the 21-rule ignore list is gone; rules E, F, W, I, B, UP, S, SIM, RUF, ASYNC are enforced.
  mypy: strict for all of `app/` (previously 24 error codes disabled); tests are type-checked.
- One CI workflow with no soft gates: backend (ruff, mypy, Postgres migrations, pytest with
  Redis and coverage >= 80%), security (bandit, pip-audit without ignores, npm audit), frontend
  (build, Vitest, Playwright), Docker build + smoke test. Separate CodeQL (Python, TS) and
  dependency-review workflows. The old evals/security workflows were removed.
- Test fixtures no longer fall back to `MagicMock` when imports fail.

### Security
- Rate limiting: client IP is the TCP peer unless it is in `TRUSTED_PROXIES` (then the right-most
  untrusted `X-Forwarded-For` hop), so a spoofed header no longer resets limits. Every `/api/`
  route is limited per IP (`RATE_LIMIT_PER_MINUTE`, default 120); login also has a per-account
  limit across IPs. Counters live in Redis when configured, else a bounded in-process LRU.
- Request bodies are capped while streaming (413): uploads at `MAX_UPLOAD_SIZE_MB`, other
  endpoints at 1 MB, including chunked bodies without `Content-Length`.
- Document text is no longer rewritten for "prompt-injection sanitization" (which changed real
  values). It is sent verbatim inside a random per-request delimiter, and the system instruction
  treats it as untrusted data. Unknown document types are not interpolated into prompts.
- All log output (app, uvicorn, Celery) is scrubbed of configured secrets, bearer tokens, JWTs,
  Google API keys, credential parameters and URL passwords.
- `LocalStorageProvider.read` no longer falls back to absolute or working-directory paths; reads
  outside the storage root are refused. Review downloads resolve paths through the storage root.
- Comma-separated list settings (`CORS_ORIGINS`, `TRUSTED_PROXIES`, ...) parse correctly
  (previously the documented `.env.example` format crashed startup).
- `bandit -r app`: no findings. `pip-audit -r requirements.txt`: no known vulnerabilities.

### Added
- Review API (`reviewer` role; admins inherit): `GET /api/v1/reviews`, `GET /api/v1/reviews/{id}`,
  `GET /api/v1/reviews/{id}/document`, `POST /api/v1/reviews/{id}/approve` (optional schema-validated
  corrections), `POST /api/v1/reviews/{id}/reject`. Decisions are recorded in `review_events`.

### Removed
- Fake OCR provider classes (Textract, Document AI, Azure, Paddle), the shadowed `app/ocr/providers.py`,
  `app/ai/registry.py`, `app/ai/factory.py`, and `app/validation/` (benchmarks built on fabricated output).

### Database
- Alembic `007_extraction_failure_status`: `ai_extractions.status/error_code/error_message`;
  nullable `structured_json`, `raw_response`, `confidence`, `estimated_cost`, `extracted_texts.confidence`.
- Alembic `008_review_queue`: `ai_extractions.confidence_details`, `ai_extractions.final_json`, `review_events` table.
- Alembic `009_celery_jobs`: `processing_jobs.document_type`, `idempotency_key` (unique), `error_code`;
  drops `job_type`, `priority`, `progress`, `worker_name`.

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
