# Architecture Decision Record: ADR-019

## Title
Workflow Durability & Event-Sourced Checkpointing for Crash Recovery

## Status
**ACCEPTED** (2026-03-24)

## Context
Mission-critical business workflows can run for minutes, hours, or days (e.g., waiting for external human reviews or multi-party document validations). In-memory workflow state is vulnerable to process crashes, infrastructure node failovers, and rolling platform deployments.

## Decision
We mandate **Durable Execution with State Checkpointing**. The workflow runtime captures and persists an immutable `Checkpoint` after every task completion, branching decision, and external state transition. On node restart or worker reassignment, the runtime re-hydrates execution state from the latest durable checkpoint without re-executing completed idempotent side-effects.

## Consequences
### Positive
- Zero workflow state loss across infrastructure restarts and server crashes.
- Resumes long-running executions reliably.
### Negative / Trade-Offs
- Requires checkpoint persistence I/O after each task completion.
