# ADR-050 / ADR-943: Distributed Tracing & Context Propagation Standard

## Status
Accepted

## Context
Complex document pipelines span HTTP gateways, message queues, workflow engines, OCR workers, and remote LLM providers. Distributed trace continuity is required to identify bottlenecks and trace end-to-end request lifecycles without losing causality across asynchronous boundaries.

## Decision
We adopt an OpenTelemetry-compatible distributed tracing model supporting:
1. W3C `traceparent` / `tracestate` and B3 propagation formats via `TraceContextPropagator`.
2. Hierarchical `Span` lifecycle management (`SpanKind`, `SpanStatus`, `SpanEvent`, `SpanLink`).
3. Sampling strategies (`TraceSampler`) including probabilistic, rate-limiting, and error-adaptive sampling.
4. `TraceTreeAnalyzer` to compute critical path latencies, identify bottleneck spans, and detect asynchronous forks.

## Consequences
- End-to-end trace preservation across synchronous REST calls and asynchronous message queues.
- Standardized span metadata across Python runtime and external API gateways.
- Deterministic critical path calculation for automated performance optimization.
