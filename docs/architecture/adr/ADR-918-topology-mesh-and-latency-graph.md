# ADR-918: Mesh Graph Dijkstra Routing and Cross-Region Latency Topologies

## Status
Accepted

## Context
Global networks require dynamic topology representation with latency, bandwidth, and health metrics to compute optimal routing paths across regions and clusters.

## Decision
Implement `TopologyGraph` and `TopologyDiscoveryService` modeling nodes (regions, clusters, gateways) and weighted edges with Dijkstra's shortest path computation based on real-time latency.

## Consequences
- Dynamic calculation of optimal inter-region transit paths.
- Accurate discovery of nearest compute resources for incoming document traffic.
