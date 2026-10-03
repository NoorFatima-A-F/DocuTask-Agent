# ADR-052 / ADR-945: Multi-Dimensional Metrics Platform & Percentile Aggregation Design

## Status
Accepted

## Context
Accurate real-time operational metrics require multi-dimensional labeling (service, host, cluster, region, tenant, workflow) and low-latency percentile calculations (p50, p90, p95, p99, p99.9) for high-frequency workloads without lock contention or excessive memory usage.

## Decision
We implement an enterprise metric platform featuring:
1. Thread-safe `MetricRegistry` supporting 8 core metric types (`COUNTER`, `GAUGE`, `HISTOGRAM`, `SUMMARY`, `TIMER`, `RATE`, `PERCENTILE`, `DISTRIBUTION`).
2. Multi-dimensional label hashing and fast label subset filtering (`matches_labels`).
3. Domain-specific collectors for System (`SystemMetricCollector`), Workflows (`WorkflowMetricCollector`), and AI Models (`AIMetricCollector`).
4. High-performance `TimeWindowAggregator` capable of calculating statistical summaries, rates per second, and percentile distributions over arbitrary time windows.

## Consequences
- Ultra-fast metric ingestion with thread-safe lock mechanisms.
- Exact and approximate percentile aggregations across latency distributions.
- Native separation between system infrastructure, document processing, and AI token metrics.
