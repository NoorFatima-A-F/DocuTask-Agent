# ADR-006: Data Asset Model

## Status
Accepted

## Context
In enterprise AI platforms, data cannot be treated as passive database rows. Assets span raw input files, OCR outputs, prompts, embeddings, vector context, agent memory, and generated decisions. Every data asset must possess an immutable identity, cryptographic checksum, tenant ownership, and complete lifecycle auditability.

## Decision
Implement a canonical `DataAsset` model:
1. Every asset receives a globally unique `asset_id`, `organization_id`, `workspace_id`, and `project_id`.
2. Asset types encompass `DOCUMENT`, `PROMPT`, `EMBEDDING`, `RETRIEVAL_CONTEXT`, `AGENT_MEMORY`, `MODEL_OUTPUT`, `BUSINESS_DATA`, `LOG`, and `KNOWLEDGE_CHUNK`.
3. Strict 8-state lifecycle FSM (`DISCOVERED` $\to$ `REGISTERED` $\to$ `CLASSIFIED` $\to$ `ACTIVE` $\to$ `UPDATED` $\to$ `SUPERSEDED` $\to$ `ARCHIVED` $\to$ `DELETED`).
4. Explicit `DataOwnership` metadata capturing owner, team, department, and assigned data steward.

## Consequences
- **Positive**: Every piece of data used or produced by AI models has an accountable owner, provenance record, and auditable status.
- **Trade-off**: Requires lifecycle transition recording across all storage layers.
