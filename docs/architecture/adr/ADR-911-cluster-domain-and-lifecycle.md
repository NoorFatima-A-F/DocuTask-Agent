# ADR-911: 12-State Governed Cluster Lifecycle and Trust Boundaries

## Status
Accepted

## Context
In a distributed, multi-region enterprise AI platform, clusters transition through discovery, provisioning, validation, active workload serving, maintenance, draining, suspension (quarantine), and removal. Without formal state machine semantics, invalid transitions cause workload corruption and security policy violations.

## Decision
Implement `ClusterLifecycleStateMachine` enforcing strict transitions across 12 lifecycle states:
`DISCOVERED`, `REGISTERING`, `REGISTERED`, `VALIDATING`, `READY`, `ACTIVE`, `DEGRADED`, `DRAINING`, `MAINTENANCE`, `SUSPENDED`, `OFFLINE`, and `REMOVED`.
Enforce workload identity and cryptographic trust verification before enabling `ACTIVE` status.

## Consequences
- Prevents unverified clusters from receiving production traffic.
- Ensures graceful drain and maintenance flows without dropping in-flight tenant requests.
- Formally models quarantine (`SUSPENDED`) state for immediate policy violation containment.
