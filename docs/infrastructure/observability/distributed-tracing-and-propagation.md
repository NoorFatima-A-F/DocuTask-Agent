# Distributed Tracing & Context Propagation Guide

## 1. Trace Context Propagation (W3C & B3)
The platform seamlessly bridges HTTP, gRPC, and message queue boundaries via `TraceContextPropagator`.

### W3C Trace Context
- `traceparent`: `00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`
- `tracestate`: `rojo=1,congo=2`

### B3 Single and Multi-Header
- `b3`: `4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-1`
- `X-B3-TraceId`, `X-B3-SpanId`, `X-B3-Sampled`

```python
from app.infrastructure.observability.tracing import TraceContextPropagator, Tracer

# Inject into outgoing HTTP headers
headers = {}
TraceContextPropagator.inject_w3c(headers, current_span)

# Extract from incoming HTTP headers
context = TraceContextPropagator.extract_w3c(headers)
```

## 2. Span Lifecycle & Context Manager
```python
tracer = Tracer(service_name="document-classifier")

with tracer.trace("classify_document", kind=SpanKind.INTERNAL) as span:
    span.set_attribute("doc_type", "invoice")
    span.add_event("preprocessing_complete", {"page_count": 4})
    # Run classification logic
```

## 3. Critical Path & Bottleneck Analysis
`TraceTreeAnalyzer` analyzes trace trees to identify the critical latency path:
```python
from app.infrastructure.observability.tracing import TraceTreeAnalyzer

analyzer = TraceTreeAnalyzer()
tree = analyzer.build_tree(spans)
critical_path = analyzer.find_critical_path(tree)
bottlenecks = analyzer.identify_bottlenecks(tree, threshold_ms=100.0)
```
