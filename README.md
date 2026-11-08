---
title: DocuTask Agent
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# DocuTask Agent

Upload a PDF or image, get structured fields back (invoice, receipt, utility bill and 11 other
document types), with evidence for every value and a human review step for anything the system
cannot verify.

**What it does**

1. **OCR** with tesseract (text PDFs are read directly).
2. **Extraction** with Google Gemini using structured output (a JSON schema per document type).
3. **Validation** against Pydantic schemas, with up to two corrective retries on invalid output.
4. **Confidence from evidence**, not from the model: each value is checked against the OCR text
   ("grounding"), required fields must be present, and arithmetic/date checks must pass
   (line items sum to subtotal, subtotal + tax = total, due date after issue date).
5. **Routing**: fully verified results are `COMPLETED`; everything else is `NEEDS_REVIEW` and goes
   to a reviewer queue, where a person approves (optionally correcting fields) or rejects.
   Only `final_json` is final; it stays null until a result is auto-accepted or approved.

**What it does not do**

- It never invents data. Missing key, provider error, timeout, unreadable output or an image with
  no text all fail with a typed error code (`LLM_AUTH_FAILED`, `LLM_RATE_LIMITED`, `OCR_NO_TEXT`, ...),
  an HTTP 4xx/5xx, and a persisted `FAILED` record.
- Only Gemini is supported. There is no multi-agent system, no self-learning loop and no
  "certification"; earlier versions of this repository described such features but did not
  implement them (see `docs/remediation/`).
- Accuracy on real-world scans has **not been measured yet** (see [Evaluation](#evaluation)).

## Architecture

```
Browser (React)  ──>  FastAPI  ──>  Postgres/SQLite   (documents, OCR text, extractions, jobs, review events)
                         │
                         └──> Redis ──> Celery worker ──> tesseract ──> Gemini ──> validation + confidence
```

- `app/api` – REST API (`/api/v1`, OpenAPI at `/api/v1/docs`); health probes `/healthz`, `/readyz`.
- `app/jobs` – Celery task and the job runner. Jobs are idempotent and retried only for
  transient errors (rate limit, unavailable, timeout), honouring `Retry-After`.
- `app/ai` – Gemini provider, prompts, schemas, validation, confidence.
- `app/ocr` – tesseract and PDF text extraction.
- `app/storage` – uploaded files on local disk or in an S3-compatible bucket.
- `frontend/` – upload, job progress, results with per-field evidence, review queue.

## Quick start (Docker Compose)

```bash
cp .env.example .env    # set JWT_SECRET, POSTGRES_PASSWORD, GEMINI_API_KEY
```

```bash
docker compose up --build
```

Open http://localhost:8000, register, upload a document. Compose runs the API (which applies
migrations on start), a Celery worker, Postgres and Redis. Only the API port is published.

To review extractions, give a user the `reviewer` role (admins inherit it):

```bash
docker compose exec db psql -U docutask -c "update users set role='reviewer' where username='alice'"
```

## Local development

Requires Python 3.12, Node 20, tesseract and (for background jobs) Redis.

```bash
make install
```

```bash
make run        # applies migrations, then uvicorn on :8000
```

```bash
make worker     # Celery worker (needs REDIS_URL)
```

```bash
cd frontend && npm run dev   # UI on :5173, proxies /api to :8000
```

`make lint`, `make test` and `make test-frontend` run the same checks as CI.

## Configuration

All settings are environment variables; `.env.example` documents each one. The important ones:

| Variable | Purpose |
|---|---|
| `ENVIRONMENT` | `development`/`test` relax checks. Anything else requires a strong `JWT_SECRET` (startup fails otherwise), and `/readyz` requires a Gemini key and Redis. |
| `GEMINI_API_KEY` | Gemini key (falls back to `GOOGLE_API_KEY`). |
| `GEMINI_MODEL` | Model ID, default `gemini-3.8-flash`. Cost is reported only for models in the dated price table in `app/core/config.py`; otherwise it is null. |
| `DATABASE_URL` | `sqlite+aiosqlite:///...` or Postgres (`postgres://` URLs are accepted). |
| `STORAGE_BACKEND` | `local` (disk shared by API and worker) or `s3` (any S3-compatible bucket: `S3_BUCKET`, `S3_REGION`, `S3_ENDPOINT_URL`, standard `AWS_*` credentials). |
| `REDIS_URL` | Celery broker and shared rate-limit counters. Without it, job submission returns 503 `QUEUE_UNAVAILABLE`. |
| `CONFIDENCE_THRESHOLD_HITL` | Scores below this (default 0.85) go to review. |
| `TRUSTED_PROXIES` | CIDRs of your reverse proxies; only then is `X-Forwarded-For` used for rate limiting. |

## API in brief

All routes except `/healthz`, `/readyz` and `auth/login|register|refresh` require a bearer token.

| | |
|---|---|
| `POST /api/v1/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout` | Accounts and tokens |
| `POST /api/v1/documents/upload` | Upload (PDF/PNG/JPEG/TIFF/BMP, size-capped while streaming) |
| `POST /api/v1/jobs` | Queue extraction `{document_id, document_type}`; idempotent (`Idempotency-Key` supported) |
| `GET /api/v1/jobs/{id}` | Poll: `QUEUED`, `RUNNING`, `RETRYING`, `COMPLETED`, `NEEDS_REVIEW`, `FAILED` (+ `error_code`) |
| `GET /api/v1/ai/result/{document_id}` | Latest extraction with `confidence_details` |
| `GET /api/v1/reviews`, `POST /api/v1/reviews/{id}/approve`, `/reject` | Review queue (reviewer role) |

## Deployment

- **Docker image** (`Dockerfile`): Python 3.12 + tesseract, non-root, port 7860. Roles via the
  first argument or `ROLE`: `web` (default; migrates then serves), `worker`, `all-in-one`.
- **Hugging Face Spaces**: set `ROLE=all-in-one` plus `JWT_SECRET`, `GEMINI_API_KEY` and
  `ENVIRONMENT=production` as Space secrets. Storage and the SQLite file are ephemeral there.
- **Render** (`render.yaml`): web + worker + Postgres + Redis, with uploads in an S3-compatible
  bucket (`STORAGE_BACKEND=s3`) because the services do not share a disk.

## Evaluation

`evals/` contains a synthetic dataset of 36 rendered documents (12 invoices, 12 receipts,
12 utility bills; see [evals/SOURCES.md](evals/SOURCES.md)) and `evals/run_eval.py`.

**Routing gate (measured, runs in CI).** Scores the ground truth and 156 corrupted extractions
(hallucinated name, wrong amount, wrong date, missing amount, off-by-one invoice number) against
the document text:

| Metric | Result (2026-11-08) |
|---|---|
| False-accept rate (corrupted extraction auto-accepted) | **0 / 156** |
| Correct extractions auto-accepted | **36 / 36** |

This run found a real bug: invoice numbers differing by one digit were fuzzy-matched as
"grounded". Values containing digits now require an exact match.

This measures the confidence gate on clean text. It says nothing about OCR quality or Gemini's
accuracy.

**Live extraction (not yet measured).** `python evals/run_eval.py --mode live --record DIR` runs
tesseract + Gemini on the images and reports field accuracy, document-level accuracy,
auto-accept/review/failure rates, false-accept rate, latency and cost. It has not been run for this
release because no working Gemini key was available; no accuracy figure is claimed until it is.
`--mode replay --recordings DIR` re-scores a recorded run offline.

## Security

Fail-closed JWT secret check, bcrypt passwords, PyJWT with required `exp`/`iat`, auth on every
non-public route (enforced by a test), trusted-proxy-aware rate limits with per-account login
limits, streamed upload size caps, storage reads confined to the storage root, document text sent
to the model as delimited untrusted data, and secret scrubbing in all logs. CI runs bandit,
pip-audit, npm audit, CodeQL and dependency review. Report vulnerabilities as described in
[SECURITY.md](SECURITY.md).

## Project status

Version 2.0.0 is the result of a remediation that removed ~8,900 files of unreachable or
simulated code. Before/after metrics and the deletion manifest are in
[docs/remediation/](docs/remediation/). See [CHANGELOG.md](CHANGELOG.md).
