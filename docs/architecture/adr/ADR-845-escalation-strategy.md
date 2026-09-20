# ADR-845: Hierarchical Escalation Strategy & SLA Management

## Status
Accepted

## Context
When human reviewers are unavailable, unresponsive, or encounter complex ambiguous cases, approval queues can stall critical business operations. AI platforms need automated, hierarchical escalation policies to prevent SLA breaches without compromising compliance.

## Decision
We implemented the Escalation Management Engine under `app/oversight/escalation/`:
1. **Hierarchical Tiers**: Defined 3 escalation tiers: `LEVEL_1_TEAM_LEAD`, `LEVEL_2_DEPARTMENT_HEAD`, and `LEVEL_3_EXECUTIVE`.
2. **Automated SLA Monitoring**: `EscalationEngine` evaluates elapsed queue time against configured timeouts, automatically reassigning review requests to higher-authority roles and bumping priority levels (e.g. HIGH -> URGENT -> CRITICAL).
3. **Audit & Notifications**: Generates `EscalationEvent` records and dispatches alerts across configured notification channels.

## Consequences
### Positive
- Eliminates workflow deadlocks and ensures adherence to enterprise SLAs.
- Guarantees high-risk items receive appropriate senior management oversight.
- Complete audit trail of escalation triggers and state transitions.

### Negative / Trade-offs
- Requires active monitoring routines or cron triggers to periodically evaluate review timeouts.
