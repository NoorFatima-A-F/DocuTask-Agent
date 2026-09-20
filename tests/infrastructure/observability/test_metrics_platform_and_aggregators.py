"""
Tests for Metrics Registry, Slicing, Specialized Collectors, and Time-Window Aggregators.
"""

import time
import pytest

from app.infrastructure.observability.metrics.types import (
    MetricPoint,
    MetricSeries,
    MetricType,
)
from app.infrastructure.observability.metrics.registry import (
    MetricRegistry,
)
from app.infrastructure.observability.metrics.collectors import (
    AIMetricCollector,
    SystemMetricCollector,
    WorkflowMetricCollector,
)
from app.infrastructure.observability.metrics.aggregators import (
    TimeWindowAggregator,
)


def test_metric_registry_and_labels():
    registry = MetricRegistry()

    # Record metrics with different labels
    registry.record("http_requests_total", 10.0, MetricType.COUNTER, labels={"method": "GET", "status": "200"})
    registry.record("http_requests_total", 2.0, MetricType.COUNTER, labels={"method": "POST", "status": "500"})

    s1 = registry.get_series("http_requests_total", labels={"method": "GET", "status": "200"})
    assert s1 is not None
    assert len(s1.points) == 1
    assert s1.points[0].value == 10.0

    # Test increment
    registry.increment("task_counter", 5.0)
    registry.increment("task_counter", 3.0)
    s2 = registry.get_series("task_counter")
    assert s2.points[-1].value == 8.0


def test_specialized_collectors():
    registry = MetricRegistry()
    sys_collector = SystemMetricCollector(registry)
    wf_collector = WorkflowMetricCollector(registry)
    ai_collector = AIMetricCollector(registry)

    # 1. System
    sys_collector.collect(cpu_usage_pct=45.0, memory_usage_pct=60.0, disk_usage_pct=70.0)
    assert registry.get_series("system_cpu_usage_percent").points[-1].value == 45.0

    # 2. Workflow
    wf_collector.record_task_execution(workflow_type="document_extraction", duration_seconds=1.45, success=True)
    wf_collector.record_queue_depth(queue_name="high_priority", depth=42)
    assert registry.get_series("queue_depth_messages", labels={"queue_name": "high_priority"}).points[-1].value == 42.0

    # 3. AI Runtime
    ai_collector.record_inference(
        model_id="gemini-1.5-pro",
        provider="google",
        prompt_tokens=500,
        completion_tokens=150,
        latency_seconds=0.82,
        cost_usd=0.0025,
        safety_violation=False,
        hallucination_score=0.05,
    )
    prompt_series = registry.get_series("ai_prompt_tokens_total", labels={"model_id": "gemini-1.5-pro", "provider": "google"})
    assert prompt_series.points[-1].value == 500.0


def test_time_window_aggregator_percentiles():
    series = MetricSeries(name="latency_ms", metric_type=MetricType.HISTOGRAM)
    now = time.time()

    # Populate 100 sample latencies (1.0 to 100.0 ms)
    for i in range(1, 101):
        series.points.append(MetricPoint(timestamp=now - 50.0 + (i * 0.4), value=float(i)))

    summary = TimeWindowAggregator.aggregate(series, window_seconds=60.0, now=now)
    assert summary.count == 100
    assert summary.min == 1.0
    assert summary.max == 100.0
    assert summary.avg == 50.5
    assert 49.0 <= summary.p50 <= 51.0
    assert 89.0 <= summary.p90 <= 91.0
    assert 94.0 <= summary.p95 <= 96.0
    assert 98.0 <= summary.p99 <= 100.0
    assert summary.rate_per_sec > 0.0
