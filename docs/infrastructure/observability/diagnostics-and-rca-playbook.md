# Automated Diagnostics & Root Cause Analysis (RCA) Playbook

## 1. Dynamic Service Dependency Graph
The `ServiceDependencyGraph` constructs real-time topology models directly from distributed trace spans:
- Node attributes: service type, current error rate, p95 latency, health score.
- Edge attributes: call volume, average latency, error count, protocol.

```python
from app.infrastructure.observability.diagnostics import ServiceDependencyGraph

graph = ServiceDependencyGraph()
graph.ingest_spans(completed_spans)
topology = graph.get_topology_snapshot()
upstream_services = graph.get_upstream_dependencies("ai-inference-service")
```

## 2. Cross-Layer Platform Health Analysis
`CrossLayerHealthAnalyzer` synthesizes signals across:
- **Infrastructure Layer**: CPU utilization, Memory pressure, Disk IOPS, Network latency.
- **Workflow & Queue Layer**: Queue depth, Task retry rate, Execution failure rate.
- **AI Runtime Layer**: Token throughput, Model error rates, Prompt injection filter trips.

## 3. Automated Root Cause Analysis (RCA) Engine
When an incident is declared or an alert fires, `RootCauseAnalyzer` produces an `RCAReport`:
1. Correlates anomaly timestamps across metric time series.
2. Traverses the service dependency tree to find the earliest fault origin.
3. Identifies offending trace spans and unhandled log exceptions.
4. Generates prioritized remediation actions with confidence scores (0.0 to 1.0).
