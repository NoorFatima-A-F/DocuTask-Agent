# ADR-098: Metric-Driven Progressive Delivery (Canary, Blue-Green, Shadow)

## Status
Accepted

## Context
Deploying direct all-at-once releases risks widespread customer impact if subtle bugs or performance degradations occur.

## Decision
1. Implement 4 progressive strategies: `RollingStrategy`, `BlueGreenStrategy`, `CanaryStrategy`, and `ShadowStrategy`.
2. `CanaryAnalysisEngine` evaluates real-time telemetry (error rates, P99 latency, CPU) against `QualityGatePolicy`.
3. Breaches trigger automated aborts and instant rollback execution via `RollbackController`.

## Consequences
- Reduces blast radius of defects to single-digit percentages with sub-minute automated recovery.
