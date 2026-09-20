# Business & System Impact: INC-2026-DR-001

## Impacted Services
- `document-ingestion-api` (HTTP 503 for 1.8 minutes, queued in edge buffers)
- `ocr-worker-pipeline` (Jobs paused in Celery broker, 0 jobs lost)
- `rag-vector-indexing` (Suspended batch inserts for 3.5 minutes)

## Customer Impact
- 0 document records lost or corrupted.
- 12 active API calls received transient 503 retryable status codes; all retried successfully.
- SLA Compliance: Monthly availability 99.98% (Exceeds 99.95% target).
