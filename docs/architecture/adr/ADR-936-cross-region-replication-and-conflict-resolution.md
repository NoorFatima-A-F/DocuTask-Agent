# ADR-936: Cross-Region Replication & Deterministic Conflict Resolution

## Status
Accepted

## Context
Multi-region distributed systems experience data synchronization latency and concurrent mutations during partitioned operations. Deterministic conflict resolution is mandatory to maintain data integrity across regions.

## Decision
We implement `ReplicationManager` and `ConflictResolver` supporting continuous lag monitoring against RPO objectives and 4 deterministic resolution strategies: `LAST_WRITE_WINS`, `VECTOR_CLOCK` causality, `QUORUM_BASED` consensus, and `MANUAL_REVIEW` escalation.

## Consequences
- Real-time visibility into replication lag (seconds, bytes, unapplied mutations) across all cross-region data streams.
- Mathematical determinism when resolving concurrent mutations across disparate availability zones.
- Automatic operator paging when unresolvable data divergence is detected.
