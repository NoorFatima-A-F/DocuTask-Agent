# Architecture Decision Record: ADR-024

## Title
Distributed Saga Orchestration & Reverse Compensation Pattern

## Status
**ACCEPTED** (2026-03-24)

## Context
Enterprise workflows orchestrate multiple external SaaS systems (e.g., Salesforce, SAP, Stripe). Distributed two-phase commit (2PC) is not supported by third-party REST APIs. When a workflow step fails midway, previous successful mutations (e.g., created invoice, allocated credit) must be cleanly rolled back to prevent inconsistent states.

## Decision
We implement **Saga-style Orchestrated Compensations** in `CompensationEngine`:
1. Every state-mutating forward task can declare a corresponding `compensation_action`.
2. The runtime tracks successful forward completions in chronological order.
3. Upon unrecoverable execution failure, the engine initiates a **Saga Rollback**, executing compensations in strict reverse order ($N \rightarrow N-1 \rightarrow \dots \rightarrow 1$).

## Consequences
### Positive
- Guaranteed distributed eventual consistency across heterogeneous external services.
- Eliminates manual administrative cleanup of orphaned third-party records.
### Negative / Trade-Offs
- Authors must implement idempotent compensation actions for all mutating tasks.
