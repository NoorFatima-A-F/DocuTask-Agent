"""Tests for Metric Registry, Collectors, and Rolling Aggregation."""

import pytest
from app.observability.metrics.aggregation import RollingAggregationEngine
from app.observability.metrics.collector import PlatformMetricsCollector
from app.observability.metrics.registry import MetricRegistry


def test_metric_registry_types():
    registry = MetricRegistry()

    # Counter
    c = registry.counter("test_counter", "Test counter")
    c.inc(5.0)
    assert c.value == 5.0

    # Gauge
    g = registry.gauge("test_gauge", "Test gauge")
    g.set(100.0)
    g.dec(20.0)
    assert g.value == 80.0

    # Histogram
    h = registry.histogram("test_histogram", "Test histogram")
    for val in [0.01, 0.05, 0.1, 0.5, 1.0, 2.0]:
        h.observe(val)
    assert h.count == 6
    assert h.get_percentile(0.50) > 0


def test_platform_metrics_collector():
    registry = MetricRegistry()
    collector = PlatformMetricsCollector(registry=registry)

    # Collect across multiple layers
    collector.record_infrastructure("node-1", cpu_usage_pct=45.0, memory_usage_pct=60.0, disk_usage_pct=50.0)
    collector.record_runtime("cluster-1", worker_count=8, queue_depth=12, execution_rate_dpm=240.0)
    collector.record_workflow_execution("invoice_approval", "tenant-acme", duration_seconds=1.2, success=True)
    collector.record_agent_execution("doc_classifier", "tenant-acme", latency_seconds=0.8, tool_calls=2, reasoning_steps=3, token_usage=450, cost_usd=0.002, success=True)
    collector.record_ai_inference("gemini-1.5-flash", "google", latency_seconds=0.45, prompt_tokens=200, completion_tokens=100)

    snapshot = registry.dump_snapshot()
    assert len(snapshot["gauges"]) >= 4
    assert len(snapshot["counters"]) >= 4
    assert len(snapshot["histograms"]) >= 3


def test_rolling_aggregation_engine():
    engine = RollingAggregationEngine(window_seconds=60.0)
    for i in range(1, 11):
        engine.record("http_requests", float(i))

    agg = engine.aggregate("http_requests")
    assert agg.count == 10
    assert agg.sum_val == 55.0
    assert agg.min_val == 1.0
    assert agg.max_val == 10.0
    assert agg.avg_val == 5.5
    assert agg.p50 > 0
    assert agg.p95 >= agg.p50
