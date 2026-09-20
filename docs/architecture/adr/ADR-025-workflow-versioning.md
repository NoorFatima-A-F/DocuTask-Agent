# Architecture Decision Record: ADR-025

## Title
Workflow Versioning and Immutable In-Flight Execution Pinning

## Status
**ACCEPTED** (2026-03-24)

## Context
Deploying a new version of a workflow definition (e.g., adding or removing tasks, changing schemas) while hundreds of existing workflow executions are running can corrupt state if active workflows are abruptly migrated to the new definition structure.

## Decision
We enforce **Immutable Version Pinning** via `WorkflowVersionManager`:
1. Workflow definitions are versioned with SemVer 2.0.0 (`v1.0.0`, `v1.1.0`, `v2.0.0`).
2. When a workflow execution starts, it is immutably pinned to the exact workflow version active at start time.
3. Subsequent workflow deployments do not mutate in-flight executions; they continue executing against their original definition until completion.

## Consequences
### Positive
- Zero runtime corruption or task mapping mismatch during production workflow updates.
- Supports side-by-side execution of multiple active workflow versions.
### Negative / Trade-Offs
- Historical workflow definitions must be retained until all executions against them terminate.
