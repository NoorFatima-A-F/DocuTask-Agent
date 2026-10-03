# ADR-925: Generic Workload Definition and Pluggable Execution Contracts

## Status
Accepted

## Context
Orchestrating disparate AI operations (workflows, agents, OCR, embeddings, knowledge sync, connectors) requires a unified contract without coupling scheduler code to specific domain types.

## Decision
Create `WorkloadRequest` specifying normalized compute requirements, priority, required/optional capabilities, regional/cluster/worker constraints, affinity rules, deadline, timeout, and idempotency key.

## Consequences
- Uniform scheduling pipeline across all enterprise workloads.
- Pluggable extension for custom workload types without scheduler refactoring.
