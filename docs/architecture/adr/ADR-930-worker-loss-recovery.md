# ADR-930: Lost Worker Failure Detection and Safe Recovery Coordinator

## Status
Accepted

## Context
When a worker node experiences a hardware fault, OOM kill, or network loss, active tasks assigned to that worker must be safely identified, evaluated, and recovered without causing duplicate destructive mutations.

## Decision
Implement `LostWorkerRecoveryCoordinator` which scans for expired worker leases, transitions the worker to `UNAVAILABLE`, terminates stale assignments, releases execution leases, and evaluates task recovery safety (`SAFE_TO_RETRY`, `REQUIRES_COMPENSATION`, `REQUIRES_MANUAL_REVIEW`, `NON_RETRYABLE`).

## Consequences
- Automated detection and recovery of tasks stranded on dead workers.
- Safe segregation of non-idempotent workloads requiring review from safe-to-retry workloads.
