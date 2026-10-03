# Resource Reservations and Concurrency Guide

## Two-Phase Reservation Flow
1. **Pending**: Reservation created with 30s TTL while assignment is dispatched.
2. **Active**: Activated upon worker acknowledgment.
3. **Released**: Released upon task completion, failure, or cancellation.

## Concurrency Bounds
`ConcurrencyController` tracks simultaneous executions at 5 distinct levels:
- Platform (Global cap)
- Region (Regional cap)
- Cluster (Cluster cap)
- Worker (Worker slot limit)
- Tenant (Tenant maximum concurrent executions)
