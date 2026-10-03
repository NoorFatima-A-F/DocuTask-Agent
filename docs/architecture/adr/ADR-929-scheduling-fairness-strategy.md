# ADR-929: Multi-Tenant Scheduling Fairness and Priority Anti-Starvation

## Status
Accepted

## Context
High-volume tenants submitting thousands of batch requests can starve low-volume tenants of worker capacity. Additionally, static strict priority queues can permanently starve low-priority tasks.

## Decision
1. Implement `FairnessScheduler` using Deficit Fair Share queue interleaving to ensure fair multi-tenant access.
2. Implement `PriorityScheduler` with dynamic aging (`aging_rate_per_sec * wait_time`) so low-priority workloads gradually elevate in priority score over time.

## Consequences
- Guaranteed protection against tenant starvation under heavy multi-tenant load.
- Ensures all submitted workloads eventually execute without static starvation.
