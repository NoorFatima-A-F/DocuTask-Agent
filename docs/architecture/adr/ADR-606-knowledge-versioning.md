# ADR-606: Knowledge Versioning & Historical Immutability

## Status
Accepted

## Context
Enterprise policies, SOPs, and contracts evolve over time. If a workflow made a decision based on Version 1.0 of a policy, auditing and reproducing that decision requires querying the exact historical version of the knowledge asset rather than the current active draft.

## Decision
We implement immutable `KnowledgeVersion` tracking within the `KnowledgeRegistry`. Each version preserves a content checksum, creator ID, change summary, and publication timestamp. Workflows can pin specific version numbers during execution.

## Consequences
- Full compliance and legal defensibility for automated AI decisions.
- Safe rollbacks to previous policy versions in the event of drafting errors.
