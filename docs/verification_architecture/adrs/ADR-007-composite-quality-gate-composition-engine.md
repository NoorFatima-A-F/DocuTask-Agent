# ADR-007: Composite Quality Gate Composition Engine

## Status
Accepted

## Context
Different environments (Development, Staging, Production) require varying gate rigor. A single static pass/fail rule cannot handle flexible multi-condition criteria.

## Decision
We implemented a Composite Quality Gate Engine:
- Evaluates `QualityGatePolicy` with customizable criteria:
  - `min_overall_score` (e.g., 0.85)
  - `max_critical_failures` (typically 0)
  - `mandatory_invariants` (must pass 100%)
  - `metric_thresholds` (custom per-metric lower bounds)
  - `require_all_invariants` boolean flag
- Yields structured `QualityGateEvaluation` detailing passed criteria and violation reasons.

## Consequences
### Positive
- Flexible policy configuration per suite or target environment.
- Explicit violation reporting for rapid root-cause debugging.

### Negative
- Policies must be maintained alongside test suites.
