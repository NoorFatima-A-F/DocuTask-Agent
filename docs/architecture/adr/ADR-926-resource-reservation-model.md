# ADR-926: Two-Phase Capacity Reservation and Concurrency Control

## Status
Accepted

## Context
High concurrent scheduling attempts on a small set of high-performing workers can lead to severe overcommit and OOM crashes if capacity is not reserved atomically prior to worker acknowledgment.

## Decision
Implement `ResourceReservationManager` providing atomic two-phase resource reservation:
1. `PENDING`: Capacity is reserved during candidate selection with a short TTL (30s).
2. `ACTIVE`: Activated upon worker assignment ACK.
3. `RELEASED`: Released upon job completion or assignment failure.
In addition, `ConcurrencyController` enforces hard concurrency limits across Platform, Region, Cluster, Worker, and Tenant.

## Consequences
- Prevents resource overcommit and race conditions during concurrent placement.
- Automatically releases leaked reservations if workers fail to ACK.
