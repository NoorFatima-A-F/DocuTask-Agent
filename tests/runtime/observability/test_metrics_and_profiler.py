"""
Unit & Integration Tests for MetricsEngine, ExecutionProfiler, AnomalyDetector, and HealthEvaluator.
"""

import pytest
from app.runtime.observability.schemas import (
    CostEvent,
    EventCategory,
    ExecutionEvent,
    MissionEvent,
    TraceContext,
    WorkerEvent,
)
from app.runtime.observability.anomaly_detection import AnomalyDetector
from app.runtime.observability.execution_profiler import ExecutionProfiler
from app.runtime.observability.metrics_engine import MetricsEngine
from app.runtime.observability.resource_monitor import ResourceMonitor
from app.runtime.observability.runtime_health import RuntimeHealthEvaluator


def test_metrics_engine_computation():
    """Verifies that operational metrics are accurately computed from event sequences."""
    engine = MetricsEngine()

    # Emit mission lifecycle
    engine.handle_event(MissionEvent(category=EventCategory.MISSION, event_type="MISSION_CREATED", mission_id="m1"))
    engine.handle_event(ExecutionEvent(category=EventCategory.EXECUTION, event_type="NODE_EXEC", mission_id="m1", duration_ms=120.0, status="SUCCESS"))
    engine.handle_event(ExecutionEvent(category=EventCategory.EXECUTION, event_type="NODE_EXEC", mission_id="m1", duration_ms=250.0, status="FAILED"))
    engine.handle_event(CostEvent(category=EventCategory.COST, event_type="COST_RECORDED", mission_id="m1", payload={"cost_usd": 0.0042, "total_tokens": 1500}))
    engine.handle_event(MissionEvent(category=EventCategory.MISSION, event_type="MISSION_COMPLETED", mission_id="m1"))

    summary = engine.get_summary()
    assert summary["derived"]["total_cost_usd"] == 0.0042
    assert summary["derived"]["total_tokens"] == 1500
    assert summary["derived"]["node_success_rate"] == 0.50
    assert summary["derived"]["mission_success_rate"] == 1.0


def test_execution_profiler_flame_graph():
    """Verifies that ExecutionProfiler correctly reconstructs span trees and identifies critical paths."""
    events = [
        ExecutionEvent(
            category=EventCategory.EXECUTION,
            event_type="ROOT_SPAN",
            mission_id="m1",
            duration_ms=500.0,
            trace_context=TraceContext(span_id="s_root", parent_span_id=None, operation="root", component="planner"),
        ),
        ExecutionEvent(
            category=EventCategory.EXECUTION,
            event_type="CHILD_A",
            mission_id="m1",
            duration_ms=200.0,
            trace_context=TraceContext(span_id="s_a", parent_span_id="s_root", operation="ocr", component="worker"),
        ),
        ExecutionEvent(
            category=EventCategory.EXECUTION,
            event_type="CHILD_B",
            mission_id="m1",
            duration_ms=300.0,
            trace_context=TraceContext(span_id="s_b", parent_span_id="s_root", operation="llm_extract", component="worker"),
        ),
    ]

    span_tree = ExecutionProfiler.build_span_tree(events)
    assert len(span_tree) == 1
    assert len(span_tree[0].children) == 2

    flame = ExecutionProfiler.generate_flame_graph(span_tree)
    assert flame.name == "planner:root"
    assert flame.is_critical_path is True

    bottlenecks = ExecutionProfiler.find_bottlenecks(events, top_k=2)
    assert len(bottlenecks) == 2
    assert bottlenecks[0]["duration_ms"] == 500.0


def test_anomaly_detector_z_score():
    """Verifies that statistical outliers (> 3 sigma) trigger AnomalyReports."""
    detector = AnomalyDetector(z_score_threshold=3.0, min_history=10)

    # Populate baseline latency ~ 100ms
    for _ in range(20):
        detector.observe("worker_latency", 100.0)

    # Normal latency (105ms) -> No anomaly
    rep_normal = detector.observe("worker_latency", 105.0)
    assert rep_normal is None

    # Massive spike (1000ms) -> Anomaly triggered
    rep_spike = detector.observe("worker_latency", 1000.0, anomaly_type="LATENCY_SPIKE")
    assert rep_spike is not None
    assert rep_spike.anomaly_type == "LATENCY_SPIKE"
    assert rep_spike.z_score >= 3.0


def test_runtime_health_evaluator():
    """Verifies that RuntimeHealthEvaluator computes composite score and component scores."""
    engine = MetricsEngine()
    monitor = ResourceMonitor()
    detector = AnomalyDetector()

    evaluator = RuntimeHealthEvaluator(engine, monitor, detector)
    health = evaluator.evaluate_health()

    assert 0.0 <= health.overall_score <= 1.0
    assert "failure_resilience" in health.component_scores
    assert "cpu_headroom" in health.component_scores
    assert health.is_healthy is True
