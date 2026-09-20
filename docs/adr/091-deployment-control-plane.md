# 91. Enterprise Deployment Control Plane Architecture

Date: 2026-09-20

## Status
Accepted

## Context
As DocuTask Agent scales across multi-region Kubernetes clusters, hybrid cloud, and air-gapped environments, production deployments must not rely on fragmented CI scripts or raw `kubectl apply`. A centralized, authoritative control plane is required to govern the full delivery lifecycle.

## Decision
We implement `DeploymentControlPlane` backed by an explicit, deterministic state machine (`REQUESTED` -> `VALIDATING` -> `AWAITING_APPROVAL` -> `APPROVED` -> `PREPARING` -> `DEPLOYING` -> `VERIFYING` -> `CANARY` -> `PROMOTING` -> `ACTIVE` + failure states). All production deployments must originate and be reconciled through this control plane.

## Consequences
- Every state transition is recorded in an immutable audit log.
- Unauthorized transitions fail deterministically before touching infrastructure.
- Complete CQRS separation between command ingestion and status queries.
