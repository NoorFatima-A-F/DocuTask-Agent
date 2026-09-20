"""
API Integration Tests for Replay, Decision, Audit, and Export Endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api_get_replay_state():
    response = client.get("/api/v1/replay/mission_api_01")
    assert response.status_code == 200
    data = response.json()
    assert data["mission_id"] == "mission_api_01"
    assert "cursor" in data
    assert "state" in data
    assert "total_events" in data


def test_api_get_replay_timeline():
    response = client.get("/api/v1/replay/mission_api_01/timeline")
    assert response.status_code == 200
    data = response.json()
    assert "timeline" in data
    assert data["total_entries"] > 0


def test_api_get_decision_graph():
    response = client.get("/api/v1/replay/mission_api_01/decision-graph")
    assert response.status_code == 200
    data = response.json()
    assert "decision_graph" in data
    assert "coverage_metrics" in data
    assert data["coverage_metrics"]["provenance_coverage_ratio"] == 1.0


def test_api_get_audit_trail():
    response = client.get("/api/v1/replay/mission_api_01/audit")
    assert response.status_code == 200
    data = response.json()
    assert "audit_records" in data
    assert "verification_report" in data
    assert data["verification_report"]["is_valid"] is True


def test_api_seek_and_verify():
    # Seek
    seek_res = client.post("/api/v1/replay/mission_api_01/seek", json={"target_index": 3})
    assert seek_res.status_code == 200
    seek_data = seek_res.json()
    assert seek_data["cursor"]["current_index"] == 3

    # Verify
    verify_res = client.post("/api/v1/replay/mission_api_01/verify")
    assert verify_res.status_code == 200
    verify_data = verify_res.json()
    assert verify_data["integrity"]["is_valid"] is True
    assert verify_data["determinism"]["is_deterministic"] is True


def test_api_export_formats():
    # JSON export
    json_res = client.get("/api/v1/replay/mission_api_01/export?format=json")
    assert json_res.status_code == 200
    assert "package_signature" in json_res.json()

    # CSV export
    csv_res = client.get("/api/v1/replay/mission_api_01/export?format=csv")
    assert csv_res.status_code == 200
    assert "text/csv" in csv_res.headers["content-type"]
