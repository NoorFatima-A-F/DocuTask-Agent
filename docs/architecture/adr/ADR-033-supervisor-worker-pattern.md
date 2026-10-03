# ADR-033: Supervisor-Worker Multi-Agent Collaboration Pattern

## Status
Accepted

## Context
Universal monolithic agents that attempt to perform reasoning, domain extraction, tool invocation, and decision-making simultaneously suffer from high error rates, uncontained failures, and poor governance. We require clear role separation between supervisory orchestration and specialized worker execution.

## Decision
We implement the `SupervisorAgent` and `WorkerAgent` collaboration pattern:
1. `SupervisorAgent`:
   - Receives an `AgentPlan` and orchestrates step-by-step delegation.
   - Monitors execution progress, enforces budget limits, and resolves conflicts.
   - Terminates runaway loops (e.g., maximum iteration bounds).
   - Escalates to human reviewers when policy thresholds or low-confidence results occur.
   - Never directly performs specialized domain processing.
2. `WorkerAgent`:
   - Receives discrete subtasks via the message bus.
   - Executes domain skills (`SkillRegistry`) and tools (`ToolRegistry`).
   - Returns structured status, results, and execution telemetry to the supervisor.

## Consequences
- High modularity: Worker agents can be added or replaced without changing orchestration logic.
- Robust failure containment: Worker failures trigger supervisor recovery or retries without crashing the platform.
