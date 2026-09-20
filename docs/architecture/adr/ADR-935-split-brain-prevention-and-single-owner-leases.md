# ADR-935: Split-Brain Prevention & Single-Owner Execution Lease Revocation

## Status
Accepted

## Context
During network partitions and regional failovers, there is a severe danger that workers in both the old and new primary regions continue executing the same critical workloads, leading to duplicate processing, data corruption, and financial inconsistencies.

## Decision
We enforce strict single-owner execution lease semantics (`ExecutionLeaseManager`) coupled with mandatory lease revocation hooks executed as an atomic pre-requisite step during regional failover orchestration.

## Consequences
- Guaranteed mutual exclusion: at most one worker owns a valid execution lease for any workload attempt.
- Expired or revoked leases immediately fail fence verification on write operations.
- Strong at-least-once processing guarantees without duplicate side-effects.
