# ADR-031: Cognitive Planning & Goal Decomposition Architecture

## Status
Accepted

## Context
Enterprise users specify high-level business goals (e.g., "Process vendor invoice and post to ERP subject to tax compliance"), not low-level instruction steps. The platform needs an intelligent planning and decomposition engine that breaks down goals into dependency-ordered execution graphs without executing arbitrary, unconstrained, or unsafe actions.

## Decision
We implement `GoalManager`, `TaskDecomposer`, and `PlanningEngine`:
1. `GoalManager` manages high-level goals and parent-child subgoal hierarchies with explicit success/failure criteria and constraints.
2. `TaskDecomposer` supports Rule-Based, AI-Assisted, and Hybrid decomposition strategies, producing structured `AgentPlan`s.
3. `PlanningEngine` matches required skills/tools against registered agents in `AgentRegistry`, verifies acyclicity, estimates costs, and enforces policy constraints.
4. `TaskDecomposer.to_workflow_definition()` enables direct export of an `AgentPlan` into a Phase 3 `WorkflowDefinition`, bridging cognitive planning with durable workflow execution.

## Consequences
- Plans are strictly validated before execution starts, preventing invalid steps or circular dependencies.
- Seamless inter-operation between Phase 4 multi-agent planning and Phase 3 durable workflow DAG execution.
