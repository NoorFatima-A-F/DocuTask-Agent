# Architecture Decision Record: ADR-021

## Title
Directed Acyclic Graph (DAG) Execution Model & Topological Dependency Solver

## Status
**ACCEPTED** (2026-03-24)

## Context
Complex business processes require non-linear execution topologies including parallel fan-out, barrier synchronization, conditional branching, and join points. Linear execution scripts cannot model these dependencies effectively.

## Decision
We implement a **Declarative DAG Execution Model** using `ExecutionGraph`:
1. Graph nodes represent discrete tasks, decisions, approvals, timers, agent actions, and sub-workflows.
2. Graph edges declare typed dependencies (`SUCCESS`, `FAILURE`, `CONDITIONAL`, `COMPENSATION`).
3. Kahn's topological sort algorithm resolves execution ordering while Tarjan's DFS detects cycles before runtime execution.

## Consequences
### Positive
- Flexible representation of arbitrary parallel workflows and decision trees.
- Compile-time cycle detection guarantees termination.
### Negative / Trade-Offs
- Requires compilation and validation steps before execution.
