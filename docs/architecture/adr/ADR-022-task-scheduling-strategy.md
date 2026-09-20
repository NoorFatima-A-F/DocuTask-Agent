# Architecture Decision Record: ADR-022

## Title
Multi-Tier Priority Task Scheduling and Queue Routing Architecture

## Status
**ACCEPTED** (2026-03-24)

## Context
Running heterogeneous workflow tasks (e.g., fast validation tasks, slow LLM reasoning loops, human reviews, background data cleanup) on a single FIFO queue results in queue starvation, head-of-line blocking, and SLA breaches for high-priority customer requests.

## Decision
We implement a **10-Tier Specialized Task Scheduler**:
- Priority tiers: `critical`, `high`, `normal`, `low`, `background`
- Functional tiers: `ai`, `human`, `connector`, `retry`, `dead-letter`
Tasks are automatically routed to their optimal queue tier based on task type and declared priority. The scheduler pulls from highest-priority tiers first with weighted round-robin scheduling.

## Consequences
### Positive
- Eliminates head-of-line blocking by slow background tasks.
- Guarantees low latency for critical business transactions.
### Negative / Trade-Offs
- Requires multiple queues to be monitored and balanced.
