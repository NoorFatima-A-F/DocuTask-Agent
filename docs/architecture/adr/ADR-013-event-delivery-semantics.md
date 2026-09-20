# Architecture Decision Record: ADR-013

## Title
Event Bus Architecture: At-Least-Once Delivery, Idempotent Consumers, and Dead-Letter Queue Handling

## Status
**ACCEPTED** (2026-03-24)

## Context
Distributed document processing platforms cannot guarantee exactly-once delivery across network boundaries without crippling performance overhead. Systems must withstand transient network disconnects, subscriber crashes, and slow message consumption.

## Decision
We adopt **At-Least-Once Delivery with Idempotent Consumers** on the Platform Event Bus:
1. Publishers transmit CloudEvents 1.0 envelopes.
2. The Event Bus handles retry with exponential backoff on subscriber errors.
3. Unrecoverable failures are routed to the `DeadLetterQueue` with error context and attempt counts.
4. Consumers use `IdempotentConsumer` deduplication wrappers to ensure deterministic side-effect execution.

## Consequences
### Positive
- High message throughput without distributed 2PC locking.
- Resilient recovery from transient worker crashes.
- Complete auditability and replay capability via `EventReplayEngine`.
### Negative / Trade-Offs
- Consumers must explicitly maintain idempotency keys or wrap execution in `IdempotentConsumer`.
