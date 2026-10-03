# ADR-937: Point-in-Time Recovery, Checkpoint Integrity & Disaster Workflows

## Status
Accepted

## Context
Corrupted databases, lost block volumes, drained queue partitions, or catastrophic AI provider outages require standardized, executable recovery playbooks rather than manual panic-driven intervention.

## Decision
We introduce `CheckpointManager`, `RecoveryVerifier`, and `RecoveryWorkflowExecutor` providing cryptographically verified point-in-time state snapshots (`SHA256`) and parameterized workflows for Region Outages, DB Corruption, Storage Loss, Queue Loss, and AI Provider Fallback.

## Consequences
- Immediate, automated verification of restored data checksums, row counts, and schema versions before exposing services.
- Transactional step execution with automated rollbacks if any critical recovery step fails.
- Auditable post-recovery reports detailing end-to-end recovery duration against RTO targets.
