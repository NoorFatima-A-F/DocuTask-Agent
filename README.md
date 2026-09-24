<div align="center">

# DocuTask Agent

**Enterprise-Grade Autonomous AI Document Processing Pipeline & Extraction Engine**

[![CI Pipeline](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions)
[![CodeQL Security Analysis](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/codeql.yml/badge.svg)](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/codeql.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.0-e92063.svg?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<p align="center">
  <a href="#system-architecture">Architecture</a> •
  <a href="#core-capabilities">Key Features</a> •
  <a href="#security--codeql-hardening">Security Baseline</a> •
  <a href="#quickstart">Quickstart</a> •
  <a href="#api-reference">API Reference</a> •
  <a href="#testing--verification">Verification</a>
</p>

</div>

---

## Overview

**DocuTask Agent** is an event-driven, asynchronous document processing platform engineered to parse, extract, validate, and structure data from high-volume, unstructured document streams (invoices, legal contracts, regulatory filings, and forms). 

By decoupling ingestion from multimodal extraction using an asynchronous task queue and enforcing strict Pydantic schemas, DocuTask Agent eliminates model hallucinations and delivers verified, deterministic JSON outputs ready for downstream enterprise data stores.

<p align="center">
  <img src="docs/assets/pipeline_demo.png" alt="DocuTask Extraction Demo" width="850">
</p>

---

## Core Capabilities

- **Asynchronous Task Architecture:** Non-blocking file ingestion powered by FastAPI, Celery, and Redis with integrated Dead-Letter Queues (DLQ) and idempotency guards.
- **Multimodal Extraction Agents:** Structured entity extraction utilizing multi-stage LLM prompting, OCR routing (PyMuPDF / Tesseract), and context-aware schema anchoring.
- **Strict Data Contracts:** Pydantic v2 validation layers with confidence thresholding, boundary validation, and automated field formatting.
- **Human-in-the-Loop (HITL) Routing:** Automatic fallback and routing of low-confidence extractions (< 85% threshold) to dedicated human review queues.
- **Enterprise-Grade Security:** Hardened filesystem operations with zero-trust path boundary validation, CRLF log-injection prevention, and cryptographic key hashing.
- **Self-Healing & Observability:** Granular audit trails, Prometheus metric collection, automated failure recovery runbooks, and structured logging.

---

## System Architecture

```mermaid
flowchart TB
    subgraph Ingestion ["Ingestion Layer"]
        A[Client / Webhook / S3 Drop] --> B[FastAPI Gateway]
        B --> C[Payload Sanitizer & Auth]
    end

    subgraph Broker ["Asynchronous Queue"]
        C --> D[(Redis Broker / DLQ)]
        D --> E[Worker Pool]
    end

    subgraph Processing ["Extraction & Verification Pipeline"]
        E --> F[Document Preprocessing\nPDF Parser / OCR Routing]
        F --> G[Multimodal LLM Agent\nStructured Prompting]
        G --> H[Pydantic v2 Validation Layer]
    end

    subgraph Evaluation ["Decision & Routing Engine"]
        H -->|Confidence >= 0.85| I[(PostgreSQL / MinIO Storage)]
        H -->|Confidence < 0.85 / Schema Drift| J[HITL Review Queue]
        I --> K[Enterprise Webhook / Event Bus]
    end

    subgraph Security ["Security Perimeter"]
        direction LR
        S1[Safe Path Canonicalizer] -.-> F
        S2[CRLF Log Sanitizer] -.-> E
        S3[PBKDF2 HMAC-SHA256 Auth] -.-> C
    end
```

---

## Security & CodeQL Hardening

DocuTask Agent enforces strict defense-in-depth security standards verified by GitHub CodeQL static analysis.

* **0 Active CodeQL Vulnerabilities:** Verified clean against `py/path-injection`, `py/log-injection`, `py/weak-sensitive-data-hashing`, and related CWE rules.
* **Path Traversal Mitigation (CWE-22, CWE-73):** All filesystem writes and dynamic output paths are strictly validated through `resolve_safe_path()` using `os.path.commonpath` boundary verification.
* **Log Injection Defense (CWE-117):** Dynamic logger parameters are passed through `sanitize_log_input()` to strip control sequences, carriage returns (`\r`), and newlines (`\n`).
* **Cryptographic Hardening (CWE-327):** Secure credential hashing using PBKDF2-HMAC-SHA256 with 100,000 rounds.

Full audit documentation is available in [`docs/security/codeql-dashboard-verification.md`](docs/security/codeql-dashboard-verification.md).

---

## Tech Stack

| Domain | Technology |
| --- | --- |
| **Backend Framework** | Python 3.11+, FastAPI, Uvicorn, Starlette |
| **Data Validation** | Pydantic v2, JSON Schema |
| **Worker Queue & Broker** | Celery, Redis, RabbitMQ |
| **Document Processing** | PyMuPDF (fitz), Tesseract OCR, Pillow |
| **AI / Orchestration** | LangChain, LlamaIndex, Google Gemini API / OpenAI API |
| **Database & Storage** | PostgreSQL, SQLAlchemy (AsyncIO), MinIO / Amazon S3 |
| **Static Analysis & Testing** | CodeQL (`security-extended`), Pytest, Ruff |
| **DevOps & Containers** | Docker, Docker Compose, GitHub Actions CI/CD |

---

## Quickstart

### Prerequisites

* Python 3.11+
* Docker and Docker Compose
* Tesseract OCR (`sudo apt install tesseract-ocr` or `brew install tesseract`)

### 1. Clone & Set Up Virtual Environment

```bash
git clone https://github.com/NoorFatima-A-F/DocuTask-Agent.git
cd DocuTask-Agent

python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the example environment file and configure your credentials:

```bash
cp .env.example .env
```

Key environment variables:

```env
PROJECT_NAME="DocuTask-Agent"
API_V1_STR="/api/v1"
SECRET_KEY="your-super-secret-key-change-in-production"
REDIS_URL="redis://localhost:6379/0"
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/docutask"
LLM_PROVIDER="gemini"
GEMINI_API_KEY="your-api-key-here"
```

### 3. Launch via Docker Compose

```bash
docker compose up -d --build
```

The API will be available at `http://localhost:8000`. Access interactive Swagger documentation at `http://localhost:8000/docs`.

---

## API Reference

### Ingest Document for Autonomous Extraction

```http
POST /api/v1/documents/process
Content-Type: multipart/form-data
```

**Request Parameters:**

* `file`: Raw binary (PDF, PNG, TIFF)
* `document_type`: `invoice` | `contract` | `identity` | `generic`
* `priority`: `low` | `standard` | `high`

**Sample cURL:**

```bash
curl -X POST "http://localhost:8000/api/v1/documents/process" \
     -H "Authorization: Bearer <API_TOKEN>" \
     -F "file=@invoice_2026_09.pdf" \
     -F "document_type=invoice"
```

**Structured JSON Response:**

```json
{
  "task_id": "9d8e7c6b-5a4f-4e3d-2c1b-0a9b8c7d6e5f",
  "status": "completed",
  "confidence_score": 0.962,
  "execution_time_ms": 782,
  "extracted_data": {
    "invoice_number": "INV-2026-9041",
    "vendor": {
      "name": "Acme Industrial Logistics",
      "tax_id": "US-84920194"
    },
    "totals": {
      "subtotal": 12450.00,
      "tax": 1027.13,
      "total_amount": 13477.13,
      "currency": "USD"
    },
    "line_items": [
      {
        "description": "Enterprise Automated OCR Nodes (Tier 1)",
        "quantity": 3,
        "unit_price": 4150.00,
        "amount": 12450.00
      }
    ]
  },
  "review_required": false
}
```

---

## Testing & Verification

The repository contains an exhaustive test suite covering security controls, API contracts, and platform resilience:

```bash
# Run security regressions (path traversal, symlinks, log sanitization)
pytest tests/security/ -v

# Run core pipeline & schema validation tests
pytest tests/core/ -v

# Run platform verification & integration tests
pytest tests/platform_verification/ -q

# Run full suite
pytest
```

---

## Project Structure

```text
DocuTask-Agent/
├── app/
│   ├── ai/                 # Multimodal extraction logic & prompt templates
│   ├── core/               # Security primitives, config, and database engines
│   ├── connectors/         # Storage and external platform adapters
│   ├── evaluation/         # Confidence thresholding & schema verification
│   ├── infrastructure/     # Failover planners, orchestrators, and incident monitors
│   ├── jobs/               # Celery task definitions, broker configs, and DLQ
│   ├── middleware/         # Request context, rate limiting, and exception handlers
│   ├── ocr/                # Layout parsers and OCR pipeline wrappers
│   └── services/           # Extraction, document, and auth service controllers
├── docs/                   # Architecture diagrams and security verification reports
├── migrations/             # Alembic database migrations
├── tests/
│   ├── connectors/         # Webhook and external storage mock suites
│   ├── core/               # Token hashing and configuration tests
│   ├── platform_verification/ # End-to-end integration and resilience tests
│   └── security/           # Path traversal, log injection, and boundary tests
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
