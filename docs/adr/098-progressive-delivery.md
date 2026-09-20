# 98. Progressive Delivery & Telemetry-Driven Automated Rollback

Date: 2026-09-20

## Status
Accepted

## Context
Deployments must minimize user impact and prevent latent regressions from propagating across all cluster nodes.

## Decision
We implement four progressive delivery strategies (Rolling, Blue-Green, Canary, Shadow) governed by `CanaryAnalysisEngine` and `ProgressiveDeliveryController`. Stepwise Canary transitions (1% -> 5% -> 10% -> 25% -> 50% -> 100%) continuously inspect error rate, p95 latency, workflow success, and safety violations. Breaching quality gates triggers an immediate automated abort and rollback via `RollbackController`.

## Consequences
- Reduces Mean Time to Recovery (MTTR) to seconds.
- Every rollback generates a machine-readable forensic incident report.
