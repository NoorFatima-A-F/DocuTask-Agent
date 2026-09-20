# ADR-004: SHA-256 Content-Addressable Immutable Evidence Store

## Status
Accepted

## Context
Verification claims without verifiable forensic evidence are unverifiable in enterprise and compliance audits. Evidence payloads must be tamper-proof, deduplicated, and linkable to specific verification runs.

## Decision
We implemented a Content-Addressable Evidence Store where:
- Every raw payload (prompt, response, OCR bounding boxes, tool logs) is hashed via SHA-256.
- The record ID is content-derived: `evidence_id = sha256(payload)`.
- Updates to existing keys are rejected to preserve immutability.
- Verification methods validate raw payloads against stored digests on demand.

## Consequences
### Positive
- Absolute tamper-proofing and mathematical evidence integrity.
- Deduplication of identical test artifacts.

### Negative
- Storage capacity scales with unique artifact generation.
