# ADR-006: Decoupled Worker Execution Model

**Status**: **ACCEPTED**  
**Date**: 2026-08-19  

## 1. Context & Problem Statement
OCR preprocessing, AI LLM extraction, Pydantic validation, and database storage have different CPU/RAM/network requirements.

## 2. Decision Outcome
Decouple worker pool into specialized roles: `OCRWorker`, `AIWorker`, `ValidationWorker`, and `PostProcessingWorker` ([app/jobs/workers.py](file:///C:/Users/User/Desktop/ai_document_processing_platform/app/jobs/workers.py)). Workers send 30-second heartbeats; jobs receive a 5-minute lease duration (`lease_expires_at`).

## 3. Consequences
- **Positive**: Each worker type scales independently based on bottleneck requirements.
