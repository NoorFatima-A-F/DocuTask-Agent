# ADR-812: Immutable Prompt Versioning & Semantic Diff Engine

## Status
Accepted

## Context
Modifying prompt instructions directly in production without immutable historical snapshots leads to unreproducible agent behaviors, untracked regressions, and difficult rollbacks.

## Decision
We enforce an immutable prompt versioning architecture:
- Every prompt edit creates an immutable `PromptVersion` record with a cryptographic SHA-256 content hash, semantic version number, author attribution, and change rationale.
- Historical prompt versions cannot be overwritten or altered in-place.
- A structural & semantic `PromptDiffEngine` computes changes in instructions, dynamic variables, constraints, and expected output schemas across versions.
- A `PromptRollbackService` enables deterministic, one-click restoration of prior validated releases.

## Consequences
- **Positive**: 100% historical execution auditability, deterministic rollbacks, comprehensive changelogs.
- **Negative**: Adds storage requirement for maintaining all historical prompt revisions.
