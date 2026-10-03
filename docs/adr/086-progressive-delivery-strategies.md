# 86. Progressive Delivery Strategies Engine

Date: 2026-09-19

## Status
Accepted

## Context
Deployments to production must minimize blast radius and ensure zero user-visible downtime. Different workloads and services require different rollout methodologies.

## Decision
We implement four first-class progressive delivery strategies:
1. `RollingStrategy`: Incremental batch deployment with surge and unavailability constraints.
2. `BlueGreenStrategy`: Active/Standby slot isolation with instant atomic cutover.
3. `CanaryStrategy`: Stepwise traffic shifting (e.g. 5% -> 25% -> 50% -> 100%) with automated error rate and latency SLO gates.
4. `ShadowStrategy`: Asynchronous dark launching with live traffic mirroring and response parity validation.

## Consequences
- Service owners select the appropriate strategy based on risk profile.
- Unhealthy canary releases abort automatically before reaching significant user traffic.
