# Worker Failure and Recovery Guide

## Lost Worker Detection
`LostWorkerRecoveryCoordinator` scans for workers whose heartbeat leases have lapsed beyond their TTL.

## Recovery Classification
- `SAFE_TO_RETRY`: Idempotent or read-only workloads (OCR, Embeddings, Evaluation) with remaining retry attempts.
- `REQUIRES_COMPENSATION`: Workflows requiring compensation steps before retry.
- `REQUIRES_MANUAL_REVIEW`: Non-idempotent connector mutations.
- `NON_RETRYABLE`: Exhausted max retry count.
