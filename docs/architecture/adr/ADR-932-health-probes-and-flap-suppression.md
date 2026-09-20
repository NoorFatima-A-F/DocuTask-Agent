# ADR-932: Deep Health Probing & Anti-Oscillation Flap Suppression

## Status
Accepted

## Context
Standard binary health checks fail to detect degraded dependencies, resource exhaustion, or intermittent failures. Furthermore, rapid state oscillations ("flapping") trigger cascading alert storms and unnecessary, disruptive failovers.

## Decision
We implement a deep 6-category health probing framework (`STARTUP`, `READINESS`, `LIVENESS`, `DEPENDENCY`, `RESOURCE`, `BUSINESS`) with configurable success/failure thresholds, and sliding-window `FlapDetector` dampening to suppress noisy status transitions.

## Consequences
- Deep composite health scoring (0-100) reflecting true operational capability across subsystems.
- Elimination of failover storms caused by transient network blips.
- Standardized probe contracts across all synchronous and asynchronous service handlers.
