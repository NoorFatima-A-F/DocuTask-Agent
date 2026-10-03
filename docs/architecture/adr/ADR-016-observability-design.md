# Architecture Decision Record: ADR-016

## Title
Unified Observability Framework: Structured JSON Logging, Golden Signal Metrics, and W3C Distributed Tracing

## Status
**ACCEPTED** (2026-03-24)

## Context
Debugging distributed autonomous agent workflows across multiple asynchronous queues, LLM inferences, and external API connectors requires unified correlation across logs, metrics, traces, and health probes.

## Decision
We implement a native, **OpenTelemetry-compatible Observability Architecture**:
1. **Structured Logging**: Strict JSON logs with contextual `trace_id`, `request_id`, `organization_id`, `workflow_id`, `agent_id` via async `ContextVar` propagation. Plain print statements are strictly forbidden.
2. **Golden Signal Metrics**: `Counter`, `Gauge`, `Histogram`, `Timer` tracking latency, error rates, token costs, and queue depths.
3. **Distributed Tracing**: Spans following the trace hierarchy: `Request Trace -> Workflow Span -> Agent Span -> Tool Span -> Database Span -> External API Span` with W3C TraceContext headers.
4. **Health Framework**: 6-level hierarchical evaluation (`Org -> Platform -> Module -> Service -> Worker -> Connector`) with Kubernetes-compatible `/live`, `/ready`, `/startup` probes.

## Consequences
### Positive
- Instant end-to-end root-cause analysis for failed document operations.
- Real-time visibility into LLM token expenditure and agent latency bottlenecks.
### Negative / Trade-Offs
- Async tasks must propagate context variables to preserve distributed trace continuity.
