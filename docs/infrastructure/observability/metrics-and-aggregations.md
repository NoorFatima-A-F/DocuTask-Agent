# Metrics Platform & Percentile Aggregations Guide

## 1. Metric Types & Data Model
The metrics platform supports 8 metric types:
- `COUNTER`: Monotonically increasing cumulative values.
- `GAUGE`: Instantaneous point-in-time measurements (CPU %, Queue Depth).
- `HISTOGRAM`: Latency & size buckets for distribution analysis.
- `SUMMARY`: Streaming statistical summaries (count, sum, min, max, mean).
- `TIMER`: Execution duration measurements in milliseconds.
- `RATE`: Events per second / minute.
- `PERCENTILE`: Accurate p50, p90, p95, p99, p99.9 latencies.
- `DISTRIBUTION`: Complete frequency distributions.

## 2. Multi-Dimensional Metric Recording
```python
from app.infrastructure.observability.metrics import MetricRegistry, MetricType

registry = MetricRegistry()
registry.record(
    name="document.processing.latency_ms",
    metric_type=MetricType.TIMER,
    value=45.2,
    labels={"tenant_id": "tenant-01", "stage": "ocr", "status": "success"}
)
```

## 3. Windowed Statistical Aggregations
`TimeWindowAggregator` provides multi-dimensional rollups:
```python
from app.infrastructure.observability.metrics import TimeWindowAggregator

aggregator = TimeWindowAggregator(registry)
summary = aggregator.aggregate(
    metric_name="document.processing.latency_ms",
    window_seconds=300,
    labels={"stage": "ocr"}
)
# Returns: p50, p90, p95, p99, p99.9, mean, min, max, count, sum, rate_per_second
```
