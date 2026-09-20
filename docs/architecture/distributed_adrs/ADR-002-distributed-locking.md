# ADR-002: Distributed Locking & Mutual Exclusion Engine

**Status**: **ACCEPTED**  
**Date**: 2026-08-19  

## 1. Context & Problem Statement
Prevent race conditions where two concurrent background workers process the same document simultaneously, leading to duplicate OCR, duplicate Gemini AI API calls, or duplicate database writes.

## 2. Decision Outcome
Use **PostgreSQL Advisory Locks** (`pg_advisory_xact_lock`) combined with `DistributedLockManager` (`app/jobs/locking.py`). Locks are tied to the document ID resource. If a second worker attempts to acquire an active lock, it receives `acquired = False` and yields processing cleanly.

## 3. Consequences
- **Positive**: Zero duplicate AI extraction calls or duplicate billing under concurrent worker competition.
- **Negative**: Requires 5-second lock acquisition timeout handling.
