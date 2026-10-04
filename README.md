---
title: DocuTask Agent
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

<div align="center">

# DocuTask Agent

**Enterprise-Grade Autonomous AI Document Processing Pipeline & Extraction Engine**

[![CI Quality Gate](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/ci.yml)
[![Security & Vulnerability Gate](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/security.yml/badge.svg)](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/security.yml)
[![Autonomous Agent Evaluation](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/agent-evals.yml/badge.svg)](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/agent-evals.yml)
[![Release: v1.0.0](https://img.shields.io/badge/Release-v1.0.0-blue.svg)](https://github.com/NoorFatima-A-F/DocuTask-Agent/releases/tag/v1.0.0)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.0-e92063.svg?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<p align="center">
  <a href="#system-architecture--autonomous-evaluation-pipeline">Architecture</a> •
  <a href="#core-capabilities">Key Features</a> •
  <a href="#security--codeql-hardening">Security Baseline</a> •
  <a href="docs/architecture/technical_deep_dive.md">Technical Deep Dive</a> •
  <a href="docs/deployment/render_deployment_guide.md">Live Deployment</a> •
  <a href="#quickstart">Quickstart</a> •
  <a href="#api-reference">API Reference</a> •
  <a href="#testing--autonomous-verification">Verification</a>
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
- **Self-Healing & Observability:** OpenTelemetry distributed tracing with correlation IDs, granular audit trails, Prometheus metric collection, automated failure recovery runbooks, and structured JSON logs.

---

## System Architecture & Autonomous Evaluation Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor Client as Ingestion Client / Webhook
    participant API as FastAPI Gateway (/api/v1)
    participant Router as Hybrid Extraction Router
    participant LLM as Multimodal Vision / OCR Agent
    participant Contract as Pydantic V2 Contract Engine
    participant DLQ as Celery Dead-Letter Queue (Redis)
    participant Storage as PostgreSQL & Artifact Store

    Client->>API: POST /documents/extract (Payload / PDF)
    API->>Router: Native Text Density Check (< 15%)
    alt Low Text Density / Complex Table
        Router->>LLM: Dispatch to Vision OCR Agent
    else Digital PDF
        Router->>API: Fast-path PyMuPDF Extraction
    end
    LLM->>Contract: Validate Schema Conformance
    alt Schema Valid
        Contract->>Storage: Commit Structured Document JSON
        Storage-->>Client: 200 OK + Extraction Payload
    else Validation Failure
        Contract->>DLQ: Route to Dead-Letter Queue (Retry / Review)
        DLQ-->>Client: 202 Accepted (Flagged for Review)
    end
```

```mermaid
flowchart TB
    subgraph Ingestion ["Ingestion Layer"]
        A[Client / Webhook / S3 Drop] --> B[FastAPI Gateway]
        B --> C[Payload Sanitizer & Auth]
    end

    subgraph Broker ["Asynchronous Queue & DLQ"]
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

    subgraph Security ["Security Perimeter & Telemetry"]
        direction LR
        S1[Safe Path Canonicalizer] -.-> F
        S2[CRLF Log Sanitizer] -.-> E
        S3[PBKDF2 HMAC-SHA256 Auth] -.-> C
        S4[OpenTelemetry Tracing] -.-> B
    end
```

---

## Security & CodeQL Hardening

DocuTask Agent enforces strict defense-in-depth security standards verified by GitHub CodeQL static analysis.

* **0 Active CodeQL Vulnerabilities:** Verified clean against `py/path-injection`, `py/log-injection`, `py/weak-sensitive-data-hashing`, and related CWE rules.
* **Path Traversal Mitigation (CWE-22, CWE-73):** All filesystem writes and dynamic output paths are strictly validated through `resolve_safe_path()` using `os.path.commonpath` boundary verification.
* **Log Injection Defense (CWE-117):** Dynamic logger parameters are passed through `sanitize_log_input()` to strip control sequences, carriage returns (`\r`), and newlines (`\n`).
* **Cryptographic Hardening (CWE-327):** Secure credential hashing using PBKDF2-HMAC-SHA256 with 100,000 rounds.

Detailed security architecture explanations and static analysis remediation methodology are available in [`docs/architecture/technical_deep_dive.md`](docs/architecture/technical_deep_dive.md) and [`docs/security/codeql-dashboard-verification.md`](docs/security/codeql-dashboard-verification.md).

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

## Testing & Autonomous Verification

The platform features deterministic unit and integration test pyramids along with autonomous agent evaluation and synthetic OCR resilience harnesses:

```bash
# 1. Run all unit & integration tests
pytest tests/ -v

# 2. Run autonomous agent evaluation & accuracy benchmarks
python -m cli.agent_cli evaluate --suite all

# 3. Run adversarial synthetic OCR fuzzing drill
python -m cli.agent_cli fuzz-resilience --corruption-rate 0.08

# 4. Execute distributed chaos injection & multi-region failover drill
python -m cli.main simulate-failover --workers 10 --fault-rate 0.2

# 5. Execute static type checking & AST security analysis
mypy app/ --ignore-missing-imports
bandit -r app/ -ll -q
```

---

## Project Structure

```text
DocuTask-Agent/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                 # Linting (Ruff), Type checking (Mypy), AST Security (Bandit), Pytest
│   │   ├── security.yml           # Dependency audit (pip-audit), Secret scanning, Bandit SAST
│   │   └── agent-evals.yml        # Scheduled autonomous evaluation & chaos matrix
│   └── pull_request_template.md   # Standardized PR verification matrix
├── app/                           # Core production package
│   ├── api/                       # FastAPI routers, Kubernetes /health/live & /health/ready probes
│   ├── core/                      # Settings, OpenTelemetry tracing (telemetry.py), path config
│   ├── cli/                       # Centralized platform CLI implementation
│   ├── models/                    # SQLAlchemy Async ORM models
│   ├── schemas/                   # Pydantic v2 data contracts & DocumentExtractionSchema
│   ├── services/                  # Multimodal extraction, OCR routing, LLM orchestration
│   ├── agents/                    # Autonomous multi-agent framework
│   ├── pipeline/                  # Async pipeline processing
│   ├── runtime/                   # Distributed cloud runtime & fabric
│   └── workers/                   # Celery / Redis task queues, retry backoff & DLQ (tasks.py)
├── cli/                           # Unified Platform CLI Entrypoints
│   ├── main.py                    # Centralized platform CLI runner
│   └── agent_cli.py               # Autonomous evaluation, chaos, and OCR fuzzing runner
├── config/                        # Canonical declarative policy specifications
│   ├── health/                    # liveness_contract.yaml, readiness_policy.yaml, health_rules.yaml
│   ├── policies/                  # dependency_policy.yaml, repo_metadata.json
│   └── environments/              # staging.yaml, production configs
├── docs/                          # Enterprise technical documentation
│   ├── adr/                       # Architecture Decision Records (ADR 0001, 0002, etc.)
│   ├── architecture/              # Technical deep dives & architecture blueprints
│   ├── runbooks/                  # Incident response & operational procedures
│   └── security/                  # Threat models & security governance
├── evals/                         # AI evaluation benchmarks, fuzzing & accuracy datasets
│   ├── datasets/                  # Golden document samples (invoices_gold.json) & edge cases
│   ├── ground_truth/              # Validated Pydantic target schemas
│   ├── runners/                   # Extraction & synthetic OCR fuzzer runners (fuzz_ocr_resilience.py)
│   └── suites/                    # Consolidated verification logic (chaos, extraction, reliability)
├── infra/                         # Infrastructure as Code
│   ├── docker/                    # Dockerfiles & compose manifests
│   ├── k8s/                       # Kubernetes base & overlay manifests
│   └── observability/             # Grafana dashboards & Prometheus alerts
├── migrations/                    # Alembic migration scripts
├── scripts/                       # Maintenance, database seeds, and operational runbooks
├── tests/                         # Consolidated test suite (2,880+ tests)
├── .env.example
├── .gitignore                     # Hardened against telemetry dumps, bytecode, and scratch files
├── .pre-commit-config.yaml        # Standard hooks: Ruff, secret detection, large file block
├── CONTRIBUTING.md                # Engineering standards & PR contribution guide
├── Dockerfile
├── pyproject.toml                 # Unified packaging, build system, and tool configs
└── README.md
```

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
