# ADR-053 / ADR-946: Service Level Objectives (SLO) & Error Budget Burn Rate Policy

## Status
Accepted

## Context
Traditional static threshold alerting causes alert fatigue, ignores cumulative user experience impact, and does not provide predictive indicators of impending SLA violations.

## Decision
We adopt Google SRE-style Service Level Objectives (SLOs) and multi-window Error Budget Burn Rate tracking:
1. `SLOObjective` defines target reliability percentages over a rolling window (e.g., 99.9% over 30 days).
2. `ErrorBudgetTracker` continuously measures good vs. total events and computes remaining error budgets.
3. Multi-window burn rate detection (1h, 6h, 24h, 3d windows) with configurable thresholds (e.g., 14.4x burn over 1h, 6x burn over 6h).
4. `AlertRuleEvaluator` triggers fast-burn emergency pages and slow-burn ticket alerts based on mathematical burn rates.

## Consequences
- High-fidelity alerting with near-zero false alarms during transient spikes.
- Clear alignment between engineering velocity and operational reliability targets.
- Automated escalation when error budget consumption exceeds critical velocity thresholds.
