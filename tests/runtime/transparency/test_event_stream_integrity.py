"""
Test Suite: Event Stream Integrity & Timeline Builder
Validates unforgeable timeline construction, state machine transitions, worker monitor, and runtime metrics.
"""
import time
from app.runtime.observability.timeline_builder import TimelineBuilder
from app.runtime.observability.execution_state import ExecutionStateManager
from app.runtime.observability.worker_monitor import WorkerMonitor
from app.runtime.observability.runtime_metrics import LiveRuntimeMetrics


def test_timeline_builder_event_sorting_and_transformation():
    raw_events = [
        {
            "event_id": "ev_2",
            "type": "WORKER_COMPLETED",
            "actor": "Worker-LLM-1",
            "timestamp": time.time() + 0.5,
            "payload": {"duration_ms": 420.0, "cost_usd": 0.0018, "confidence": 0.98},
        },
        {
            "event_id": "ev_1",
            "type": "PLANNER_DECISION",
            "actor": "APDLE-Planner",
            "timestamp": time.time(),
            "payload": {"decision": "ROUTE_GEMINI_FLASH"},
        },
    ]

    entries = TimelineBuilder.build_timeline_from_events("mission_integ_001", raw_events)
    assert len(entries) == 2
    # Verify sorting: ev_1 should come first
    assert entries[0].event_id == "ev_1"
    assert entries[0].actor == "APDLE-Planner"
    assert entries[0].category == "PLANNER"
    assert entries[1].event_id == "ev_2"
    assert entries[1].category == "WORKER"
    assert entries[1].duration_ms == 420.0


def test_execution_state_manager_lifecycle():
    manager = ExecutionStateManager()
    
    # Check default active mission
    snap = manager.get_mission_snapshot("mission_live_001")
    assert snap is not None
    assert snap["mission_id"] == "mission_live_001"
    assert snap["total_tasks"] >= 3

    # Update task state
    updated = manager.update_task_state(
        task_id="task_extract_1",
        mission_id="mission_live_001",
        status="COMPLETED",
        duration_ms=450.0,
        cost_usd=0.0018,
        confidence=0.985,
    )
    assert updated is not None
    assert updated.status == "COMPLETED"
    assert updated.confidence_score == 0.985


def test_worker_monitor_telemetry():
    monitor = WorkerMonitor()
    
    workers = monitor.list_workers()
    assert len(workers) >= 4

    monitor.record_worker_heartbeat(
        worker_id="worker_ocr_1",
        queue_depth=1,
        is_busy=True,
        latency_ms=190.0,
    )
    cluster = monitor.get_cluster_summary()
    assert cluster["total_workers"] >= 4
    assert cluster["total_queued_tasks"] >= 1
    assert cluster["cluster_health"] == "HEALTHY"


def test_live_runtime_metrics_aggregation():
    metrics = LiveRuntimeMetrics(window_seconds=30.0)
    
    metrics.record_mission_completion(latency_ms=350.0, tokens=1500)
    metrics.record_mission_completion(latency_ms=400.0, tokens=2000)

    summary = metrics.get_live_metrics_summary()
    assert summary["missions_processed_in_window"] > 0
    assert summary["throughput_documents_per_sec"] >= 0.0
    assert summary["latency_p50_ms"] > 0.0
