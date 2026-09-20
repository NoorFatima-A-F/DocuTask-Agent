# ADR-097: GitOps Reconciliation Engine & Automated Drift Remediation

## Status
Accepted

## Context
Manual cluster mutations and ad-hoc infrastructure changes lead to configuration drift and reproducibility failures.

## Decision
1. Declarative manifests in Git serve as the single source of truth (`GitOpsController`).
2. Support pluggable providers: `ArgoCDProvider` and `FluxProvider`.
3. `DriftDetector` classifies drift into `EXPECTED_DRIFT`, `UNAUTHORIZED_DRIFT`, and `EMERGENCY_CHANGE`, automatically executing reconciliation loops when drift is detected.

## Consequences
- Zero configuration divergence between Git source and running Kubernetes clusters.
