# ADR 081: Service Level Objectives (SLO) & Error Budget Governance

## Status
Accepted

## Context
Engineering velocity and reliability must be balanced quantitatively. Uncontrolled deployments during active platform instability cause severe cascading outages.

## Decision
Establish quantitative SLO management (`SLOCalculator`, `ErrorBudgetEngine`):
1. Define SLIs across Availability, Latency, Error Rates, and Recovery Times.
2. Track rolling error budgets (30-day window) with multi-window burn rate alerts (1h, 6h, 24h).
3. Automatically trigger release freeze gates when error budgets are exhausted.

## Consequences
- **Positive**: Data-driven reliability commitments, objective release gating, proactive error burn containment.
- **Negative**: Feature deployment freezes during periods of budget exhaustion require SRE exception approval.
