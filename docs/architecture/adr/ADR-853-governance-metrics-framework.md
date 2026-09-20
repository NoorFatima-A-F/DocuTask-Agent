# ADR-853: Modular Governance Metrics Calculation Framework

## Status
Accepted

## Context
Monitoring enterprise AI systems requires domain-specific KPI formulas (e.g. Decision Allow Rates, Policy Friction Index, Agent Intervention Rate, Model Drift Signals) computed dynamically across time windows. Hardcoding metric formulas across disparate endpoints creates metric inconsistencies.

## Decision
We implemented a modular metrics calculation engine under `app/governance/analytics/core/`:
1. **Domain Calculators**: Dedicated calculator components for `DecisionMetricsCalculator`, `PolicyMetricsCalculator`, `AgentMetricsCalculator`, `ModelMetricsCalculator`, and `PromptMetricsCalculator`.
2. **Composite Health Score**: Weighted calculation combining Policy Effectiveness (25%), Agent Safety (25%), Decision Compliance (25%), and Model Reliability (25%) into an aggregate 0–100 index.
3. **Time-Series Aggregation**: `TimeSeriesAggregator` computes rolling period metrics and delta percentages (`compare_periods`).

## Consequences
### Positive
- Single source of truth for governance KPIs and formulas.
- Consistent metrics across dashboards, reports, and SDK.
- Configurable weighting for organization-specific risk appetites.

### Negative / Trade-offs
- Adding new metric definitions requires updating respective domain calculators.
