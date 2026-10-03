# ADR-962: GitOps Architecture & Continuous Reconciliation

## Status
Accepted

## Context
Direct cluster imperative mutations (e.g. `kubectl apply`, `helm upgrade`) create configuration drift where the actual running infrastructure differs from version-controlled declarations.

## Decision
We adopt a declarative GitOps operational model:
1. Version-controlled Git repositories serve as the single source of truth for desired cluster manifests.
2. `GitOpsSynchronizer` tracks commit revisions and manifest trees.
3. `GitOpsReconciler` continuously computes drift across desired vs. actual runtime state (`MISSING`, `MODIFIED`, `EXTRA`).
4. `GitOpsController` automatically corrects configuration drift back to the declared Git state.

## Consequences
- 100% auditable infrastructure changes through Git commits and pull requests.
- Instant automated remediation of manual or unauthorized cluster mutations.
- Repeatable environment recreation from bare infrastructure declarations.
