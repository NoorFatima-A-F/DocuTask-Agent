# AI Document Processing Platform Backend

Production-grade, Clean Architecture backend for multi-format document text extraction, OCR detection, LLM structured extraction, authentication, and document lifecycle management.

---

## Technical Stack & Architecture

- **Framework**: FastAPI (Async Python 3.10+)
- **Architecture**: Clean Architecture (API, Core, Auth, Database, Models, Repositories, Schemas, Services, Dependencies, Middleware)
- **Database**: PostgreSQL (SQLAlchemy 2.0 Async + Alembic, with SQLite `aiosqlite` in-memory test runner)
- **Authentication**: JWT Access Tokens + JWT Refresh Tokens (Token Rotation, SHA-256 token hash storage, bcrypt password hashing)
- **Validation**: Pydantic v2 & `pydantic-settings`

---

## API Response Format

All endpoints strictly adhere to the unified envelope:

```json
{
  "success": true,
  "message": "Human readable status summary",
  "data": { ... },
  "errors": null
}
```

Error responses:

```json
{
  "success": false,
  "message": "Error summary",
  "data": null,
  "errors": { ... }
}
```

---

## Implemented Authentication API Endpoints (Phase 2)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET`  | `/api/v1/health` | System health check | No |
| `POST` | `/api/v1/auth/register` | Register new user account | No |
| `POST` | `/api/v1/auth/login` | Authenticate user & issue tokens | No |
| `POST` | `/api/v1/auth/refresh` | Refresh tokens using Rotation | No |
| `POST` | `/api/v1/auth/logout` | Revoke specific refresh token | No |
| `POST` | `/api/v1/auth/logout-all` | Revoke all sessions across devices | Bearer JWT |
| `GET`  | `/api/v1/auth/me` | Fetch authenticated user profile | Bearer JWT |
| `POST` | `/api/v1/auth/change-password` | Change user password & invalidate sessions | Bearer JWT |
| `POST` | `/api/v1/documents/upload` | Upload document file with SHA256 deduplication | Bearer JWT |
| `GET`  | `/api/v1/documents` | List user documents (paginated) | Bearer JWT |
| `GET`  | `/api/v1/documents/search` | Search user documents by query string | Bearer JWT |
| `GET`  | `/api/v1/documents/{id}` | Get document metadata details | Bearer JWT |
| `DELETE`| `/api/v1/documents/{id}` | Delete document file and metadata | Bearer JWT |
| `POST` | `/api/v1/ocr/extract/{document_id}` | Trigger text extraction (Native PDF vs OCR) | Bearer JWT |
| `GET`  | `/api/v1/ocr/text/{document_id}` | Retrieve aggregated document extracted text | Bearer JWT |
| `GET`  | `/api/v1/ocr/pages/{document_id}` | Retrieve per-page extracted text breakdown | Bearer JWT |
| `POST` | `/api/v1/ai/extract/{document_id}` | Trigger structured AI extraction (Invoice, Resume, etc.) | Bearer JWT |
| `GET`  | `/api/v1/ai/result/{document_id}` | Retrieve latest structured extraction result | Bearer JWT |
| `GET`  | `/api/v1/ai/history/{document_id}` | Retrieve historical extractions for document | Bearer JWT |
| `DELETE`| `/api/v1/ai/result/{document_id}` | Delete AI extraction result | Bearer JWT |
| `POST` | `/api/v1/jobs/extract/{document_id}` | Enqueue async document extraction job (202 Accepted) | Bearer JWT |
| `GET`  | `/api/v1/jobs/{job_id}` | Get background job status and progress (0-100%) | Bearer JWT |
| `GET`  | `/api/v1/jobs` | List user background processing jobs (paginated) | Bearer JWT |
| `DELETE`| `/api/v1/jobs/{job_id}` | Cancel background processing job | Bearer JWT |

---

## Asynchronous Worker Architecture (Phase 6)

- **Lightweight Async API**: Long-running document pipeline processing (OCR + AI extraction) is dispatched asynchronously to background workers. The API returns `202 Accepted` with a `job_id` immediately.
- **Queue Abstraction**: `JobQueueProvider` interface decouples business logic from queue engines. Initial implementation: `AsyncInMemoryJobQueue` backed by `asyncio.Queue`, designed for zero-code-change drop-in migration to Redis/Celery/RabbitMQ.
- **Progress Tracking & Duplicate Prevention**: Tracks progress (0% -> 10% -> 40% -> 80% -> 100%). Enforces active job duplicate prevention so a single document cannot be queued twice simultaneously.
- **Exponential Backoff Retry Strategy**: Automatically retries failed jobs up to `max_attempts` (default 3) using exponential backoff delays (2s, 4s, 8s).

---

## AI Engine & Structured Extraction Architecture (Phase 5)

- **Provider Abstraction**: Decoupled `LLMProvider` interface. Initial implementation: `GeminiProvider`. Zero Gemini SDK imports exist outside `app/ai/providers/gemini.py`.
- **Supported Document Schemas**: `invoice`, `resume`, `contract`, `medical_report`, `receipt`, `purchase_order`, `generic`.
- **Automatic Validation & Retry Loop**: Raw LLM output is validated against Pydantic target schemas. If parsing fails, retries up to 3 times with corrective feedback instructions.
- **Cost & Token Tracking**: Automatically counts input/output tokens, measures processing latency (ms), and computes estimated USD cost per extraction.
- **Automated Pipeline Integration**: Automatically executes OCR text extraction if not already present before triggering AI extraction.

---

## OCR & Extraction Architecture (Phase 4)

- **Smart PDF Processing**: Detects whether a PDF page contains native selectable text. If selectable text exists (`processing_method="native_pdf"`), extracts text directly with 1.0 confidence score without invoking OCR engines.
- **Scanned PDF & Image Fallback**: Automatically converts scanned PDF pages and images to binary image streams and processes them via `TesseractOCRProvider` (`processing_method="ocr"`).
- **Extracted Text Persistence & Caching**: Extracted page text, confidence scores, and processing methods are stored in `extracted_texts` database table. Subsequent calls return cached results unless `force_reextract=true` is specified.
- **Provider Independence**: `OCRProvider` abstract base interface allows hot-swapping Tesseract with AWS Textract, Azure OCR, or Google Cloud Vision.

---

## Storage Architecture (Phase 3)

The platform implements a decoupled `StorageProvider` abstract base interface.
Current provider implementation:
- `LocalStorageProvider`: Persists binary files under date-partitioned paths (`storage/uploads/YYYY/MM/DD/<uuid>.<ext>`).
- Built-in path traversal safeguards checking resolved paths against storage root.
- Collision-resistant UUID filename generation.
- Deduplication via SHA-256 binary content hashing.

---

## Running Locally & Testing

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
alembic upgrade head
```

### 3. Run Development Server
```bash
uvicorn app.main:app --reload --port 8000
```
Interactive Documentation: `http://localhost:8000/api/v1/docs`

### 4. Run Pytest Test Suite
```bash
pytest -v
```
