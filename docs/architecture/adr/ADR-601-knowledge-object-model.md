# ADR-601: Knowledge as a First-Class Governed Platform Resource

## Status
Accepted

## Context
Traditional RAG prototypes treat knowledge as ad-hoc raw text blobs dumped into vector databases without governance, metadata, version history, or lifecycle management. In an enterprise automation platform, this leads to stale answers, lack of compliance auditability, and data security breaches.

## Decision
We establish `KnowledgeObject` as a first-class, governed platform resource. Every knowledge entity is explicitly assigned ownership, multi-level classification clearance (`PUBLIC` to `HIGHLY_RESTRICTED`), sensitivity ratings, version tags, and an enforced 9-state lifecycle:
$$\text{CREATED} \to \text{INGESTED} \to \text{VALIDATED} \to \text{CLASSIFIED} \to \text{INDEXED} \to \text{PUBLISHED} \to \text{ACTIVE} \to \text{SUPERSEDED} \to \text{ARCHIVED}$$

## Consequences
- Full provenance and compliance traceability across all knowledge ingested into the platform.
- Clean lifecycle progression guarantees that only validated, indexed, and active documents participate in AI grounding.
