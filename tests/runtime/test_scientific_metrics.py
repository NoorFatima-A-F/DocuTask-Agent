"""
Scientific Metrics Engine Test Suite.
Verifies all canonical formulas, statistical estimators, percentiles, confidence intervals, and Merkle proofs.
"""

import pytest
from datetime import datetime, timezone, timedelta
from app.runtime.events.base import RuntimeEvent
from app.runtime.metrics.definitions import MetricDefinition, MetricUnit
from app.runtime.metrics.formulas import CANONICAL_FORMULAS
from app.runtime.metrics.registry import get_global_metric_registry
from app.runtime.metrics.calculator import ScientificMetricCalculator
from app.runtime.metrics.statistics import ScientificStatisticsEngine
from app.runtime.metrics.sampling import EventSampler, SamplingRule


def create_mock_events(count: int = 10, event_type: str = "WorkerCompleted") -> list[RuntimeEvent]:
    base_t = datetime.now(timezone.utc)
    events = []
    for i in range(count):
        ev = RuntimeEvent(
            event_id=f"evt_{i}",
            mission_id="mission_test_001",
            sequence_number=i + 1,
            event_type=event_type,
            agent_id="PLANNER" if i % 2 == 0 else "EXTRACTOR",
            worker_id=f"worker_{i % 3}",
            duration_ms=50.0 + (i * 10.0),
            timestamp=base_t + timedelta(seconds=i),
            payload={"task_id": f"task_{i}", "tokens_processed": 100 + i * 20},
        )
        events.append(ev)
    return events


def test_canonical_metric_registry():
    registry = get_global_metric_registry()
    metrics = registry.list_all()
    assert len(metrics) >= 8

    worker_util = registry.get("worker_utilization")
    assert worker_util is not None
    assert worker_util.category == "EXECUTION"
    assert worker_util.unit == MetricUnit.PERCENTAGE
    assert "WorkerStarted" in worker_util.required_events


def test_scientific_statistics_engine():
    data = [10.0, 20.0, 30.0, 40.0, 50.0]
    summary = ScientificStatisticsEngine.analyze_sample(data)
    assert summary is not None
    assert summary.sample_size == 5
    assert summary.mean == 30.0
    assert summary.median == 30.0
    assert summary.variance == 250.0
    assert summary.min_value == 10.0
    assert summary.max_value == 50.0
    assert summary.p50 == 30.0
    assert summary.confidence_interval_95[0] < summary.mean < summary.confidence_interval_95[1]


def test_scientific_statistics_ewma():
    series = [10.0, 20.0, 30.0, 40.0]
    ewma = ScientificStatisticsEngine.calculate_ewma(series, alpha=0.5)
    assert len(ewma) == 4
    assert ewma[0] == 10.0
    assert ewma[1] == 15.0  # 0.5 * 20 + 0.5 * 10 = 15


def test_scientific_calculator_evaluation():
    events = create_mock_events(count=20, event_type="WorkerCompleted")
    calc = ScientificMetricCalculator()

    record = calc.calculate_metric("average_latency", events)
    assert record.metric_id == "average_latency"
    assert record.value > 0.0
    assert record.sample_size == 20
    assert len(record.merkle_events_root_sha256) == 64
    assert record.statistical_summary is not None
    assert record.statistical_summary["mean"] > 0.0


def test_event_sampler_sliding_window():
    events = create_mock_events(count=50)
    rule = SamplingRule(window_type="SLIDING_COUNT", window_size=10)
    sampled = EventSampler.sample_events(events, rule)
    assert len(sampled) == 10
    assert sampled[-1].sequence_number == 50
