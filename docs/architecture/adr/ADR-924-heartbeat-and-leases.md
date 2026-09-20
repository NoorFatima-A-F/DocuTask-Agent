# ADR-924: Heartbeat Telemetry and Worker Lease Consensus

## Status
Accepted

## Context
Failure detection must be resilient against transient network latency while rapidly identifying hung or terminated workers.

## Decision
Implement `WorkerLeaseManager` and `WorkerHeartbeatManager` using sliding-window TTL leases (`WorkerLease`). Workers continuously report CPU, memory, GPU, queue pressure, and active slot telemetry. When a lease lapses, the worker is automatically marked `UNAVAILABLE`.

## Consequences
- Fast, deterministic detection of dead or unresponsive workers.
- Up-to-date resource telemetry drives accurate placement scoring.
