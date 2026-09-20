# ADR-920: Multi-Factor Deterministic Workload Routing Engine

## Status
Accepted

## Context
Routing AI inference and document processing workloads across a multi-cluster, multi-region platform requires synthesizing 7 distinct governance and technical constraints (lifecycle state, lease validity, region jurisdiction, tenant affinity, supported workload, capability hardware, capacity thresholds, label selectors).

## Decision
Implement `RoutingEligibilityEngine` which performs deterministic multi-factor candidate filtering and scores viable clusters by available allocatable capacity.

## Consequences
- 100% deterministic and explainable routing decisions with full rejection reasons when unroutable.
- Guarantees strict adherence to all governance, isolation, hardware, and capacity constraints.
