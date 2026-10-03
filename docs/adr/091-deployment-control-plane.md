# ADR-091: Deployment Control Plane State Machine & CQRS Architecture

## Status
Accepted

## Context
Enterprise release delivery requires deterministic progression across multiple validation, approval, canary, and rollback phases. Traditional script-based CI/CD pipelines lack transactional state tracking, historical event logs, and programmatic rollback triggers.

## Decision
We implement a formal `DeploymentStateMachine` and CQRS-based `DeploymentControlPlane`:
1. All deployment requests are initiated as immutable `RequestDeploymentCommand` structures with mandatory `Idempotency-Key` headers.
2. The state machine enforces legal lifecycle transitions (`REQUESTED` -> `VALIDATING` -> `AWAITING_APPROVAL` -> `APPROVED` -> `PREPARING` -> `DEPLOYING` -> `VERIFYING` -> `CANARY` -> `PROMOTING` -> `ACTIVE`).
3. Every state transition is appended to an immutable `TransitionLog` recording the timestamp, actor, and rationale.

## Consequences
- **Positive**: Complete auditability, deterministic transition rules, elimination of illegal state jumps, and seamless automated recovery.
- **Negative**: Requires strict state tracking in distributed storage.
