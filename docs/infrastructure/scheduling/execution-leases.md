# Execution Lease Management Guide

## Single-Owner Execution Leases
`ExecutionLease` guarantees that exactly one worker holds the exclusive authority to process a workload attempt.

## Split-Brain Prevention
When a task is retried or reassigned:
1. The prior execution lease is marked `REVOKED`.
2. A new `ExecutionLease` is issued to the new worker.
3. If the old worker attempts to complete the task with an expired/revoked lease, the completion is rejected.
