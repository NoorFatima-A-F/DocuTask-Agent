# ADR-701: Multi-Tenant Isolation Strategy

## Status
Accepted

## Context
DocuTask Agent is transitioning from a single-tenant enterprise deployment to a multi-tenant enterprise SaaS operating system (ESP-MOOS) serving thousands of independent organizations. Multi-tenancy must be a first-class platform primitive across all execution layers (Kernel, Workflows, Agents, Connectors, Knowledge Fabric), preventing cross-tenant leakage while maintaining operational simplicity.

## Decision
1. Introduce a mandatory `TenantContext` containing `organization_id`, `workspace_id`, `environment_id`, `project_id`, `user_id`, `permissions`, and `compliance_profile`.
2. Propagate `TenantContext` synchronously via Python `contextvars` for HTTP requests and asynchronously via worker job metadata for background tasks, DAG workflows, and autonomous agents.
3. Enforce zero-trust resource identity tagging (`ResourceIdentity`) on all platform assets.

## Consequences
- **Positive**: Strict compile-time and runtime isolation guarantees; impossible for requests to execute without tenant ownership context.
- **Trade-off**: Context must be explicitly carried across async boundary dispatches.
