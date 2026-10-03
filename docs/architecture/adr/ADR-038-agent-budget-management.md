# ADR-038: Multi-Dimensional Agent Budgeting & Resource Management

## Status
Accepted

## Context
Autonomous agents running in background or continuous workflows risk consuming unbounded LLM tokens, API requests, storage, and financial cost if left unchecked. Enterprise multi-tenancy requires active quota and budget enforcement with progressive throttling and termination.

## Decision
We implement `BudgetManager` tracking multi-dimensional resource consumption:
- Total Tokens (input + output).
- Estimated Cost (USD).
- Execution Time (seconds).
- Tool Calls and External API Invocations.

The engine evaluates consumption against configured agent/tenant budgets and triggers progressive actions:
1. `CONTINUE` ($< 60\%$ consumption): Unrestricted execution.
2. `WARN` ($60\% - 79\%$): Emits telemetry warning event.
3. `REQUIRE_APPROVAL` ($80\% - 99\%$): Demands supervisor or human approval before expensive tool invocations.
4. `TERMINATE` ($\ge 100\%$): Immediately aborts agent execution to protect financial and system resources.

## Consequences
- Guaranteed upper-bound cost control for every autonomous agent execution.
- Enables granular cost chargeback and multi-tenant budget isolation.
