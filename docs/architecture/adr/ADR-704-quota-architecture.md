# ADR-704: Quota Architecture

## Status
Accepted

## Context
Resource over-consumption and noisy neighbors can degrade overall cluster performance and cause cost overruns.

## Decision
Implement a 5-state multi-resource quota tracking engine (`QuotaManager`):
$$\text{NORMAL (0–79\%)} \longrightarrow \text{WARNING (80–99\%)} \longrightarrow \text{LIMITED (100\%)} \longrightarrow \text{EXCEEDED (>100\%)} \longrightarrow \text{SUSPENDED}$$
Resources tracked: Users, Workspaces, Projects, Workflows, Concurrent Executions, Agents, AI Tokens, Storage, Embeddings, and Connector Calls.

## Consequences
- **Positive**: Proactive alerting at 80% threshold and strict rejection of unauthorized excess operations.
- **Trade-off**: Requires lightweight atomic increment operations for high-frequency events.
