# ADR-841: Centralized Human Oversight Architecture & Autonomy Control Plane

## Status
Accepted

## Context
Autonomous AI agents and automated document pipelines operating without centralized oversight risk unintended actions, compliance failures, and catastrophic downstream impacts. Ad-hoc, fragmented approval checks (e.g., `if confidence < threshold: ask_user()`) scattered across microservices lead to inconsistent governance, opaque decision histories, and audit gaps.

## Decision
We implemented a centralized Human Oversight and Autonomy Control Plane under `app/oversight/`:
1. **Centralized Engine**: `HumanOversightEngine` manages all human-in-the-loop interactions, dynamic policy evaluation, review request lifecycles, and decision tracking.
2. **Immutable Context**: Every decision evaluation is bound to an `OversightContext` containing operational, risk, compliance, model, and prompt metadata.
3. **Decoupled Governance**: Individual agents and workflow components never implement isolated approval logic; instead, they declare execution intent through the Oversight SDK or API, which dynamically determines intervention requirements based on real-time risk policies.

## Consequences
### Positive
- Consistent enterprise governance across all agent workflows and microservices.
- Full institutional provenance and auditability of human intervention points.
- Zero fragmentation of risk and threshold logic.

### Negative / Trade-offs
- Slight latency overhead when evaluating complex multi-condition oversight policies.
