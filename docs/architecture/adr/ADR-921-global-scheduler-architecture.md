# ADR-921: Global vs. Regional Scheduling Architecture

## Status
Accepted

## Context
A centralized single scheduler coordinating worker placement across multiple global regions creates a bottleneck and failure domain. Conversely, isolated regional schedulers cannot enforce global data residency or multi-region routing.

## Decision
Split scheduling into a two-level hierarchy:
1. `GlobalScheduler`: Evaluates data residency, tenant regional affinity, and regional capacity to select destination regions.
2. `RegionalScheduler`: Executes fine-grained cluster selection, worker candidate filtering, scoring, reservation, and assignment inside the chosen region.

## Consequences
- Global governance and data residency are strictly enforced at ingress.
- Regional schedulers operate autonomously and provide low-latency worker placement.
