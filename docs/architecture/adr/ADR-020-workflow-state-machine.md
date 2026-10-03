# Architecture Decision Record: ADR-020

## Title
Workflow Definition and Instance Finite State Machines

## Status
**ACCEPTED** (2026-03-24)

## Context
Ad-hoc status strings lead to illegal transitions, unhandled corner cases, and opaque execution state. Enterprise workflows require formal, auditable state machine definitions for both workflow definitions and execution instances.

## Decision
We enforce two complementary state machines:
1. **Definition Lifecycle (15 States)**: `CREATED` -> `VALIDATING` -> `VALIDATED` -> `REGISTERED` -> `PUBLISHED` -> `ACTIVE` -> `RUNNING` -> `WAITING` -> `PAUSED` -> `RESUMED` -> `COMPLETED` / `FAILED` / `COMPENSATING` / `ARCHIVED` / `DEPRECATED`.
2. **Instance Execution State (10 States)**: `CREATED` -> `READY` -> `RUNNING` -> `WAITING` -> `SUSPENDED` -> `RETRYING` -> `FAILED` -> `COMPENSATING` -> `COMPLETED` / `CANCELLED`.
All transitions are validated against allowed transition tables and emitted to audit logs.

## Consequences
### Positive
- Prevents invalid or corrupted workflow states.
- Every state transition is traceable and reproducible.
### Negative / Trade-Offs
- State transitions must be explicitly managed through the state manager.
