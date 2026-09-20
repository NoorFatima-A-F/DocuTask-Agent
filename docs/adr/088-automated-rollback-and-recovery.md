# 88. Automated Post-Deployment Telemetry Recovery & Coordinated Rollback

Date: 2026-09-19

## Status
Accepted

## Context
When a newly deployed release introduces latent regressions (e.g. error rate spikes or tail latency degradation), relying purely on manual operator intervention causes prolonged outages.

## Decision
We implement `AutomatedRecoveryEngine` and `RollbackManager`.
The recovery engine continuously inspects telemetry metrics during post-deployment verification. If predefined safety thresholds (e.g. 2% error rate or 300ms p99 latency) are breached, the engine autonomously initiates a coordinated rollback to the prior verified release.

## Consequences
- Mean Time to Recovery (MTTR) is reduced from minutes to seconds.
- Every rollback generates a forensic audit record detailing the breach cause.
