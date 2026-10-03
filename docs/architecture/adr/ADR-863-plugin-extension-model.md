# ADR-863: Plugin and Extension Framework Architecture

## Context
Organizations have unique compliance regimes, custom risk formulas, and domain-specific data loss prevention rules that cannot be hardcoded into core governance engines.

## Decision
Introduce a sandboxed Plugin Architecture with a 6-state lifecycle (`REGISTERED` -> `VALIDATED` -> `APPROVED` -> `ACTIVE` -> `DISABLED` -> `REMOVED`) and an Extension Registry with strict contracts (`PolicyExtensionContract`, `CustomRiskEvaluatorContract`, `MetricProviderContract`). Plugins execute inside an isolated sandbox enforcing execution timeouts and scoped permissions.

## Status
Accepted

## Consequences
- Safe extensibility without compromising kernel stability or leaking data across tenants.
- Admins retain approval control before untrusted plugins can execute.
