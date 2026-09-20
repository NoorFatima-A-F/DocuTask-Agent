# 97. GitOps Reconciliation & Drift Detection Strategy

Date: 2026-09-20

## Status
Accepted

## Context
Declarative infrastructure as code ensures that production state matches version-controlled Git repositories while automatically detecting and resolving unauthorized drift.

## Decision
We implement `GitOpsController` with pluggable `GitOpsProvider` adapters (Argo CD, Flux, Generic Git Reconciler). The controller tracks desired vs observed version states and classifies drift into `EXPECTED_DRIFT`, `UNAUTHORIZED_DRIFT`, `EMERGENCY_CHANGE`, or `UNKNOWN_DRIFT`.

## Consequences
- Automatic reconciliation restores desired states upon unauthorized manual cluster modifications.
- Decouples platform delivery logic from specific vendor implementations (e.g. Argo CD vs Flux).
