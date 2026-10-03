# ADR-004: Dead Letter Queue (DLQ) & Manual Replay Engine

**Status**: **ACCEPTED**  
**Date**: 2026-08-19  

## 1. Context & Problem Statement
Jobs that fail continuously due to upstream provider outages, corrupted PDF files, or schema changes must not cause infinite retry loops.

## 2. Decision Outcome
Implement `DeadLetterQueueEngine` ([app/jobs/dlq.py](file:///C:/Users/User/Desktop/ai_document_processing_platform/app/jobs/dlq.py)). Jobs exceeding `max_attempts = 3` are moved to DLQ with full stack traces, error codes, and original payloads. Operations teams can inspect items via `GET /api/v1/jobs/dlq/list` and replay them via `POST /api/v1/jobs/dlq/replay/{job_id}` after resolving issues.

## 3. Consequences
- **Positive**: Zero queue poisoning; manual replay restores failed jobs without data loss.
