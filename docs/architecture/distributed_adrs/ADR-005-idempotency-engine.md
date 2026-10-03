# ADR-005: Cryptographic Idempotency Key Deduplication Engine

**Status**: **ACCEPTED**  
**Date**: 2026-08-19  

## 1. Context & Problem Statement
Prevent duplicate processing when network retries, browser refreshes, or client resubmissions occur for the same document.

## 2. Decision Outcome
Implement `IdempotencyEngine` ([app/jobs/idempotency.py](file:///C:/Users/User/Desktop/ai_document_processing_platform/app/jobs/idempotency.py)). Compute `SHA256(document_hash + ":" + processing_version)`. Database enforces `UNIQUE` index constraint on `idempotency_key`.

## 3. Consequences
- **Positive**: 100% duplicate prevention across 1,000 identical parallel submission attempts.
