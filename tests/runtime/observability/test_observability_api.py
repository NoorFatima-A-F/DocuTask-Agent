"""
Integration Tests for AROL REST API Endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.runtime.observability.runtime_monitor import get_runtime_monitor
from app.runtime.observability.schemas import (
    EventCategory,
    ExecutionEvent,
    MissionEvent,
)


@pytest.fixture(autouse=True)
def setup_teardown_arol():
    monitor = get_runtime_monitor()
    monitor.clear()
    
    # Emit some sample real events
    m_id = "test_mission_101"
    e1 = MissionEvent(category=EventCategory.MISSION, event_type="MISSION_STARTED", mission_id=m_id)
    e2 = ExecutionEvent(category=EventCategory.EXECUTION, event_type="OCR_TASK", mission_id=m_id, duration_ms=180.0, status="SUCCESS")
    monitor.emit_event_sync(e1)
    monitor.emit_event_sync(e2)
    yield
    monitor.clear()


def test_get_arol_runtime_dashboard():
    client = TestClient(app)
    response = client.get("/api/v1/runtime/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "health" in data
    assert "metrics" in data
    assert "resources" in data
    assert data["total_events_stored"] >= 2


def test_get_arol_runtime_health():
    client = TestClient(app)
    response = client.get("/api/v1/runtime/health/score")
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert "component_scores" in data
    assert 0.0 <= data["overall_score"] <= 1.0


def test_get_arol_mission_timeline():
    client = TestClient(app)
    response = client.get("/api/v1/runtime/missions/test_mission_101/timeline")
    assert response.status_code == 200
    timeline = response.json()
    assert len(timeline) >= 2
    assert timeline[0]["event_type"] == "MISSION_STARTED"
    assert timeline[1]["event_type"] == "OCR_TASK"


def test_get_arol_mission_profile():
    client = TestClient(app)
    response = client.get("/api/v1/runtime/missions/test_mission_101/profile")
    assert response.status_code == 200
    profile = response.json()
    assert "flame_graph" in profile
    assert "bottlenecks" in profile


def test_get_arol_prometheus_metrics():
    client = TestClient(app)
    response = client.get("/api/v1/runtime/metrics/prometheus")
    assert response.status_code == 200
    assert "docutask_" in response.text
