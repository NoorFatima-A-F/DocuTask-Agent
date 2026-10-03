# ADR 079: Unified Telemetry & Multidimensional Context Standard

## Status
Accepted

## Context
Telemetry without consistent context cannot be correlated across distributed hops, leading to blind spots and slow incident resolution.

## Decision
Enforce a universal `ObservabilityContext` across all telemetry signals containing:
- Request ID, Trace ID, Span ID
- Tenant ID, Organization ID, Workspace ID
- Service Name, Version, Environment, Region, Cluster ID, Node ID
- Workflow ID, Agent ID, Task ID, User ID

## Consequences
- **Positive**: Seamless multi-tenant partitioning, end-to-end trace correlation, pinpoint auditability.
- **Negative**: Requires context propagation across all thread and asynchronous runtime boundaries.
