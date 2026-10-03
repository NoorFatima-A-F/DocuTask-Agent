# ADR-803: Intelligent Governance-Driven Model Selection & Routing

## Status
Accepted

## Context
Autonomous agents and complex document workflows require different model capabilities (vision, reasoning, fast extraction) while adhering to latency constraints, regional data privacy rules, and token budgets.

## Decision
We implement `ModelSelectionService` and `ModelRouter`:
- Workflows specify declarative requirements: required capabilities, latency bounds, max token cost, target geographic region.
- The engine filters available models against active governance policy rules and lifecycle states.
- Remaining candidates are scored, ranked, and selected with primary + fallback chains.
- `ModelRouter` manages execution with automated circuit breaking and failover to candidate models.

## Consequences
- **Positive**: Resilient execution, cost optimization, dynamic failover without code modification.
- **Negative**: Adds negligible metadata lookup latency prior to execution.
