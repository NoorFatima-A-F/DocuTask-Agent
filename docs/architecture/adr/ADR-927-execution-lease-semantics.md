# ADR-927: Single-Owner Execution Lease Semantics and At-Least-Once Delivery

## Status
Accepted

## Context
Distributed network partitions and worker restarts can lead to split-brain scenarios where two workers simultaneously believe they own the same active execution attempt.

## Decision
Implement `ExecutionLeaseManager` issuing cryptographic, single-owner `ExecutionLease` instances with sliding-window TTLs. When a retry or reassignment attempt is created, all prior execution leases for the workload are revoked. The platform operates on at-least-once delivery with workload idempotency keys.

## Consequences
- Eliminates duplicate active execution attempts.
- Guarantees strict lease boundaries across retries.
