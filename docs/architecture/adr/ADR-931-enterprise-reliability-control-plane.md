# ADR-931: Enterprise Reliability Control Plane & 7-State Lifecycle

## Status
Accepted

## Context
Mission-critical cloud operations require an explicit, formal control plane to manage reliability targets, RTO/RPO margins, SLA commitments, and failure domain boundaries. Ad-hoc recovery leads to unpredictable downtimes and SLA violations.

## Decision
We implement a centralized `ReliabilityControlPlane` anchored by a formal 7-state lifecycle state machine (`OPTIMAL`, `DEGRADED`, `FAILING`, `PARTIALLY_FAILED`, `RECOVERING`, `RECOVERED`, `OUTAGE`) and the `ReliabilityCoordinator` to continuously evaluate operational margins against declarative `ReliabilityTarget` definitions.

## Consequences
- Deterministic, observable state transitions across all platform components and fault domains.
- Early warning detection when RTO or RPO margins degrade before customer SLA breaches occur.
- Non-interference guarantee: reliability control plane governs health and resilience without intercepting normal workload execution paths.
