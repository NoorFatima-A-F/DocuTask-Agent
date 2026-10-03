# ADR-913: Lease-Based Heartbeat and Sub-Component Health Aggregation

## Status
Accepted

## Context
Failure detection in distributed multi-region systems requires fast, reliable heartbeat leases combined with deep telemetry across 9 critical subsystems (node, service, worker, queue, database, cache, storage, network, telemetry).

## Decision
Implement `ClusterHealthAggregator` with sliding-window TTL heartbeat leases (`ClusterLease`) and multi-component health synthesis. If a lease lapses, the cluster is automatically marked `UNREACHABLE` and evicted from routing eligibility.

## Consequences
- Fast sub-minute failover detection.
- Complete observability into sub-component degradation before catastrophic cluster failure.
