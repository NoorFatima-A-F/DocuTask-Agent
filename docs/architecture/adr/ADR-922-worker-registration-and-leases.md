# ADR-922: Worker Domain, 11-State Lifecycle, and Identity Verification

## Status
Accepted

## Context
Worker nodes in distributed environments transition through discovery, registration, readiness, reservations, task execution, draining, and failure. Without strict lifecycle modeling, workers can accept tasks during maintenance or after ungraceful disconnects.

## Decision
Implement `WorkerLifecycleStateMachine` enforcing transitions across 11 states:
`DISCOVERED`, `REGISTERING`, `REGISTERED`, `AVAILABLE`, `RESERVED`, `ASSIGNED`, `RUNNING`, `DRAINING`, `UNAVAILABLE`, `RECOVERING`, and `TERMINATED`.
Only `AVAILABLE`, `RESERVED`, and `RUNNING` workers are schedulable.

## Consequences
- Guaranteed safety against dispatching tasks to draining or unverified workers.
- Formal handling of node evacuation and recovery.
