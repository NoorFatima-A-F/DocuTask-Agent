# DocuTask Agent

**AI-Powered Enterprise Document Intelligence & Autonomous Extraction Platform**

[![CI Quality Gate](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/ci.yml/badge.svg)](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/ci.yml)
[![CodeQL Security](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/codeql.yml/badge.svg)](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/codeql.yml)
[![Security Scan](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/security.yml/badge.svg)](https://github.com/NoorFatima-A-F/DocuTask-Agent/actions/workflows/security.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.9+-E92063.svg?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v1.0.0-informational.svg)](CHANGELOG.md)

---

## Overview

**DocuTask Agent** is an asynchronous, high-throughput document intelligence platform designed to ingest, parse, validate, and extract structured data from unstructured and semi-structured documents (invoices, receipts, tax forms, financial statements, and contracts).

The platform bridges multimodal computer vision, optical character recognition (OCR), and large language models (LLMs) with strict schema validation, field-level confidence scoring, and automated human-in-the-loop (HITL) review routing.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              DOCUTASK AGENT ARCHITECTURE                               │
├─────────────────────┬──────────────────────┬────────────────────┬──────────────────────┤
│  1. INGESTION & OCR │  2. AI EXTRACTION    │  3. HITL REVIEW    │  4. DATA PERSISTENCE │
│  - Multi-page PDF   │  - Multimodal Vision │  - Confidence Gate │  - PostgreSQL Async  │
│  - Image Pre-proc   │  - Pydantic Schemas  │  - Low Conf (<85%) │  - ACID Transactions │
│  - Layout & Tables  │  - Field Confidence  │  - Audit Trail     │  - Cryptographic Hash│
└──────────┬──────────┴──────────┬───────────┴─────────┬──────────┴──────────┬───────────┘
           │                     │                     │                     │
           └─────────────────────┴──────────┬──────────┴─────────────────────┘
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                           SECURITY & ENTERPRISE GOVERNANCE                             │
│  - Centralized Pydantic Settings (.env)        - Automated CodeQL & Bandit SAST        │
│  - JWT Authentication & RBAC Access Control    - Zero Hardcoded Secret Policy          │
│  - OpenTelemetry Tracing & Structured Logs     - Dependabot Continuous CVE Audits      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Problem & Solution

### The Challenge
- **High Error Rates**: Legacy template OCR breaks when layouts, fonts, or invoice formats deviate.
- **Hallucination Risk**: Naive LLM prompts produce ungrounded extractions without confidence bounds or bounding-box provenance.
- **Operational Silos**: Lack of integrated exception queues results in silent failures on low-resolution or corrupted documents.

### The DocuTask Solution
- **Deterministic Schema Grounding**: All extractions map to strictly typed Pydantic models with field-level confidence scores (0.00 – 1.00).
- **Confidence-Gated Human-in-the-Loop**: Extractions falling below the quality threshold ($< 0.85$) are automatically dispatched to a reviewer queue.
- **Defense-in-Depth Security**: Parameterized database queries, path traversal prevention, JWT authentication, and zero hardcoded credentials.

---

## Core Features

- **Multimodal Document Parsing**: Ingests PDFs, PNGs, and TIFF scans with layout preservation, OCR text fallback, and table structure recognition.
- **Multi-Model LLM Extraction**: Native support for Google Gemini 1.5/2.0 Flash/Pro with extensible adapters for Anthropic Claude and OpenAI.
- **Field Confidence Calibration**: Evaluates extraction accuracy across line items, totals, dates, and entity identifiers.
- **Human-in-the-Loop (HITL) Workflow**: Real-time review queue capturing manual corrections with full audit lineage.
- **Asynchronous Task Architecture**: Built on FastAPI, SQLAlchemy asyncpg, and Redis task dispatching for horizontal scalability.
- **Comprehensive Verification Suite**: 300+ automated unit, integration, and security tests.

---

## Technology Stack

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **API Framework** | **FastAPI 0.115+** | High-performance asynchronous REST API with automatic OpenAPI documentation. |
| **Data Validation** | **Pydantic v2.9+ / Settings** | Strict type enforcement, JSON schema generation, and centralized `.env` configuration. |
| **AI & Multimodal** | **Google GenAI SDK / Gemini** | High-accuracy document layout understanding and native multimodal token processing. |
| **OCR & Imaging** | **PDFPlumber / Pillow / Tesseract** | Fast local text and table extraction with image binarization and pre-processing. |
| **Database & ORM** | **SQLAlchemy 2.0 (Async) / Alembic** | Non-blocking database transactions with asyncpg (PostgreSQL) and aiosqlite. |
| **Security & Auth** | **python-jose / Passlib / Cryptography** | Secure JWT authentication, password hashing with bcrypt, and Ed25519 digital signatures. |
| **Quality & SAST** | **Pytest / Ruff / MyPy / Bandit** | Automated testing, linting, type validation, and AST security analysis. |

---

## Quickstart & Installation

### 1. Prerequisites
- Python 3.11 or 3.12
- Git
- Tesseract OCR (optional, for local image OCR)

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/NoorFatima-A-F/DocuTask-Agent.git
cd DocuTask-Agent

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
# Copy the example environment template
cp .env.example .env

# Edit .env and supply your local configuration and API keys:
# GOOGLE_API_KEY=your_gemini_api_key_here
# JWT_SECRET=$(openssl rand -hex 32)
```

### 4. Start the Application
```bash
# Start FastAPI application with hot reload
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive API documentation will be available at: `http://localhost:8000/docs`

---

## API Documentation

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/api/v1/auth/login` | Authenticate user and receive JWT bearer token | No |
| `POST` | `/api/v1/documents/upload` | Upload PDF or image document for asynchronous processing | Yes |
| `GET` | `/api/v1/documents/{id}/status` | Check document ingestion and extraction pipeline state | Yes |
| `GET` | `/api/v1/documents/{id}/results` | Retrieve validated structured JSON extraction and confidence scores | Yes |
| `POST` | `/api/v1/documents/{id}/review` | Submit human-in-the-loop correction for low-confidence fields | Yes |
| `GET` | `/health` | Liveness and readiness health check probe | No |

---

## Testing & Quality Assurance

DocuTask Agent maintains a comprehensive automated testing suite:

```bash
# Run all unit, integration, and platform verification tests
pytest tests/ -v

# Run tests with code coverage report
pytest tests/ --cov=app --cov-report=term-missing

# Run code style linting
ruff check .

# Run static type checking
mypy app/ --ignore-missing-imports

# Run AST security vulnerability analysis
bandit -r app/ -ll -q
```

---

## Security & Governance

- **Zero Hardcoded Secrets**: All credentials and tokens are read exclusively from environment variables via typed Pydantic Settings.
- **Automated SAST & CodeQL**: Continuous vulnerability scanning via GitHub Actions ([`.github/workflows/codeql.yml`](.github/workflows/codeql.yml)).
- **Vulnerability Reporting**: Follow the coordinated disclosure guidelines in [SECURITY.md](SECURITY.md).
- **Dependency Management**: Weekly Dependabot scans ([`.github/dependabot.yml`](.github/dependabot.yml)) and automated `pip-audit` checks.

---

## Project Structure

```
DocuTask-Agent/
├── .github/
│   ├── workflows/           # CI, CodeQL, Security, and Verification pipelines
│   ├── ISSUE_TEMPLATE/      # Bug, Feature, and Security issue templates
│   ├── dependabot.yml       # Automated dependency update configuration
│   └── CODEOWNERS           # Code ownership and reviewer routing
├── app/
│   ├── core/                # Centralized Pydantic configuration and security
│   ├── agents/              # Multimodal extraction and processing agents
│   └── platform_delivery/   # Platform services, storage, and database layer
├── enterprise_audit_engine/ # Verification baseline and reality testing platform
├── docs/
│   └── security/            # Security incident reports and dependency audit documentation
├── tests/                   # Automated pytest unit and integration test suite
├── .env.example             # Clean environment configuration template
├── pyproject.toml           # Project metadata, dependencies, and tool settings
├── requirements.txt         # Pinned application dependencies
├── CHANGELOG.md             # Project release history and change tracking
├── CONTRIBUTING.md          # Open-source contribution guidelines
├── LICENSE                  # MIT License
├── README.md                # Project documentation
└── SECURITY.md              # Enterprise security and disclosure policy
```

---

## Roadmap

- [x] **v1.0.0**: Core multimodal ingestion, Pydantic structured extraction, JWT authentication, and CI/CD security hardening.
- [ ] **v1.1.0**: Celery / Redis asynchronous worker pool for high-throughput batch ingestion (10,000+ documents).
- [ ] **v1.2.0**: OpenTelemetry distributed tracing and Grafana / Prometheus latency dashboards.
- [ ] **v1.3.0**: RAG integration with pgvector for cross-document query and financial contract comparison.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
