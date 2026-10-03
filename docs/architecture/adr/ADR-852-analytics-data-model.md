# ADR-852: Governance Data Warehouse Fact & Dimension Model

## Status
Accepted

## Context
Aggregating disparate governance telemetry requires an extensible star/snowflake schema optimized for high-throughput insertion and low-latency dimensional slice-and-dice queries across tenants, time intervals, policies, models, and agents.

## Decision
We implemented a relational analytical data model under `app/governance/analytics/warehouse/`:
1. **Fact Tables**:
   - `fact_governance_decisions`: Decision outcomes, risk scores, latencies.
   - `fact_policy_events`: Policy violations, rule triggers, severities.
   - `fact_ai_execution`: Agent, model, prompt executions, token costs, latencies.
   - `fact_risk_events`: Safety incidents, risk categories, threat levels.
   - `fact_compliance_events`: Control statuses, framework evaluations, evidence IDs.
   - `fact_approvals`: Human reviews, turnaround durations, overrides.
2. **Dimension Tables**:
   - `dim_tenant`, `dim_user`, `dim_agent`, `dim_model`, `dim_policy`, `dim_workflow`, `dim_time`.
3. **Partition & Tenant Isolation**: All queries enforce strict tenant boundary filtering.

## Consequences
### Positive
- High-efficiency multi-dimensional OLAP queries.
- Clean separation between immutable fact logs and dimensional metadata.
- Prepares platform for external warehouse synchronization (e.g. Snowflake/BigQuery).

### Negative / Trade-offs
- Dimension tables must be synchronized upon new entity creation.
