# ADR-917: Separation of Global and Regional Control Planes

## Status
Accepted

## Context
A single centralized control plane becomes a single point of failure and bottleneck across global multi-region deployments.

## Decision
Establish hierarchical control plane architecture:
1. `GlobalControlPlane`: Maintains global topology, coordinates cross-region sync, manages epoch consensus, and provides global health snapshots.
2. `RegionalControlPlane`: Operates autonomously inside each region, admitting local clusters, reconciling heartbeats, and maintaining local availability during global partition events.

## Consequences
- Regions continue processing local traffic even if global control plane network connectivity is interrupted.
- Clean separation of global coordination concerns from regional execution.
