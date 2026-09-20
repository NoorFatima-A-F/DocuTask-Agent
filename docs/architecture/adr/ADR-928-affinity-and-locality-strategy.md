# ADR-928: Multi-Factor Placement Scoring and Locality Awareness

## Status
Accepted

## Context
Worker candidate selection must optimize multiple competing objectives including resource headroom, capability match, data proximity, worker load, and tenant fairness.

## Decision
Implement `PlacementScoringEngine` combining configurable weights for:
- Resource Fit (CPU/RAM headroom)
- Capability Match (mandatory vs optional capabilities)
- Affinity and Data Locality (resolved via `DataLocalityResolver`)
- Worker Load and available slots
- Multi-Tenant Fairness Penalty

## Consequences
- High-efficiency worker packing or spreading based on operator configuration.
- Maximizes data locality and minimizes cross-region network egress costs.
