# ADR-851: AI Governance Intelligence Platform & Analytics Architecture

## Status
Accepted

## Context
Enterprise AI platforms generate vast volumes of governance signals across policy control planes, data lineage, model registries, prompt evaluation suites, safety gateways, audit ledgers, and human oversight queues. Directly running complex analytical, aggregation, and reporting queries against transactional tables creates performance bottlenecks, lock contention, and cross-system coupling.

## Decision
We implemented a decoupled **AI Governance Intelligence Platform** under `app/governance/analytics/`:
1. **Decoupled Stream-Based Ingestion**: Operational subsystems emit standardized events into the `GovernanceEventConsumer` without blocking transactional execution.
2. **Canonical Normalization**: All governance events are mapped into a unified `GovernanceAnalyticsEvent` schema with tenant and workspace isolation metadata.
3. **Dedicated OLAP Warehouse**: Events are routed to dedicated Fact tables (`fact_governance_decisions`, `fact_policy_events`, `fact_ai_execution`, `fact_risk_events`, `fact_compliance_events`, `fact_approvals`) and Dimension tables.
4. **Multi-Role Intelligence**: Built-in specialized services provide real-time dashboards for Executives, Administrators, and Developers.

## Consequences
### Positive
- Zero performance impact or lock contention on transactional agent workflows.
- Unified, normalized institutional intelligence across all AI operations.
- Strong tenant isolation across analytical aggregations.

### Negative / Trade-offs
- Requires memory and compute for continuous event normalization and warehousing.
