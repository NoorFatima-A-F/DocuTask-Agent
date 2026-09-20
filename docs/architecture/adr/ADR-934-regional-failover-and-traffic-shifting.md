# ADR-934: Multi-Region Dynamic Failover & Traffic Shifting

## Status
Accepted

## Context
When an entire cloud region experiences an outage, traffic must be redirected rapidly and safely without violating data residency regulations, exceeding target region capacity, or dropping in-flight transactions.

## Decision
We implement `RegionalFailoverPlanner`, `FailoverRouter`, and `FailoverOrchestrator` to generate validated `FailoverPlan` objects with automated pre-flight checks (data residency compliance, capacity headroom, replication lag within RPO) and dynamic traffic shifting.

## Consequences
- Zero-downtime traffic migration via weighted routing and source region draining.
- Compliance enforcement ensuring jurisdictional data boundaries are never breached during emergency failover.
- Post-failover verification ensures newly promoted primary services meet strict readiness criteria before full traffic exposure.
