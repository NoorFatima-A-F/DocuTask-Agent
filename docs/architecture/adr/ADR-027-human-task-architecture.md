# Architecture Decision Record: ADR-027

## Title
Human-in-the-Loop (HITL) Task Engine & Multi-Party Approval Architecture

## Status
**ACCEPTED** (2026-03-24)

## Context
Enterprise automation cannot always be 100% autonomous. High-stakes financial approvals, legal exceptions, and low-confidence AI document extractions require explicit human verification. Polling loops or blocked worker threads while waiting for human input cause server resource exhaustion.

## Decision
We implement a **Native Human Task & Approval Engine** (`ApprovalEngine`):
1. When a workflow hits a human gate, it safely records an `ApprovalRequest` and transitions into `SUSPENDED` state, fully releasing compute threads and database connections.
2. Supports flexible approval semantics: Single Approval, Sequential, Parallel Multi-Party, Role-Based, and Majority Voting.
3. Upon human decision callback, the runtime re-hydrates execution state and resumes downstream DAG steps.

## Consequences
### Positive
- Zero compute or thread consumption during long human review delays.
- Full compliance and audit trail for regulatory sign-offs.
### Negative / Trade-Offs
- Requires human review UI integration and webhook callback handlers.
