# ADR-009: Provenance Model

## Status
Accepted

## Context
While lineage answers "what happened to the data?", provenance answers "can we cryptographically and historically prove it?". Reproducing AI outputs and satisfying legal audits requires immutable provenance records.

## Decision
1. Implement `ProvenanceHistoryEngine` capturing `ProvenanceSourceRecord` (origin URI, SHA-256 checksum, uploader, timestamp) and `ProvenanceTransformationRecord` (exact prompt version, model version, input artifact versions, policy decision IDs, and runtime parameters).
2. Provide output reproducibility verification by validating the presence of all required input artifacts and model identifiers.

## Consequences
- **Positive**: Cryptographically verifiable audit trails; full reproducibility of AI-assisted document analyses.
- **Trade-off**: Requires storing prompt and model version hashes alongside generated outputs.
