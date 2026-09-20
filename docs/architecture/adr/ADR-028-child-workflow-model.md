# Architecture Decision Record: ADR-028

## Title
Hierarchical Sub-Workflow & Child Orchestration Model

## Status
**ACCEPTED** (2026-03-24)

## Context
Large enterprise business processes (e.g., global vendor onboarding) consist of modular, reusable sub-processes (e.g., tax ID verification, bank account validation, sanction list check). Monolithic single-DAG workflows become unmaintainable and cannot be reused across different business units.

## Decision
We implement **Hierarchical Sub-Workflow Orchestration** (`SubWorkflowNode`):
1. Workflows can invoke child workflows as independent sub-DAGs.
2. Child workflows maintain their own execution state, retry policies, and checkpoints while passing structured context and outputs back to the parent workflow.
3. Supports recursive multi-level nesting (`Parent -> Child -> Grandchild`) with full audit trace propagation (`parent_execution`).

## Consequences
### Positive
- Modular, composable, and reusable workflow building blocks.
- Isolated failure domains and localized error recovery.
### Negative / Trade-Offs
- State management must track parent-child execution correlation.
