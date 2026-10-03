# ADR 080: Distributed Tracing & OpenTelemetry Correlation Strategy

## Status
Accepted

## Context
Tracing long-running agent workflows and multi-step document pipelines requires standardized context propagation and span hierarchy across disparate components.

## Decision
Adopt OpenTelemetry-compatible tracing models (`TracingEngine`, `Span`, `SpanContext`) supporting:
1. W3C `traceparent` and B3 distributed header propagation.
2. Adaptive and ratio-based trace sampling.
3. Span event attachments (exceptions, model evaluations, tool invocations).

## Consequences
- **Positive**: Complete visual dependency graphs, pinpoint bottleneck identification, industry-standard interoperability.
- **Negative**: Trace data generation overhead mitigated by configurable sampling rates.
