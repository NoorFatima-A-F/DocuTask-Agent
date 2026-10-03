"""
Integration Tests for APDLE Planner REST API Endpoints.
"""

from fastapi.testclient import TestClient
from app.main import app


def test_get_planner_graph():
    client = TestClient(app)
    response = client.get("/api/v1/planner/graph/mission_api_01")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data
    assert "critical_path_duration_ms" in data
    assert len(data["nodes"]) == 5


def test_get_planner_critical_path():
    client = TestClient(app)
    response = client.get("/api/v1/planner/critical-path/mission_api_01")
    assert response.status_code == 200
    data = response.json()
    assert "total_critical_path_duration_ms" in data
    assert "critical_node_ids" in data


def test_get_planner_schedule():
    client = TestClient(app)
    response = client.get("/api/v1/planner/schedule/mission_api_01")
    assert response.status_code == 200
    data = response.json()
    assert "workers" in data
    assert "wavefronts" in data


def test_get_planner_simulation():
    client = TestClient(app)
    response = client.get("/api/v1/planner/simulation/mission_api_01?num_trials=25")
    assert response.status_code == 200
    data = response.json()
    assert data["trials_count"] == 25
    assert "p50_completion_ms" in data


def test_post_planner_replan():
    client = TestClient(app)
    response = client.post(
        "/api/v1/planner/replan/mission_api_01",
        json={"failed_node_id": "node_ocr_01", "error_reason": "Low image contrast"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "REPLANNED"
    assert "mutation" in data
    assert data["mutation"]["mutation_type"] == "INJECT_RECOVERY"


def test_get_planner_mutations():
    client = TestClient(app)
    response = client.get("/api/v1/planner/mutations/mission_api_01")
    assert response.status_code == 200
    mutations = response.json()
    assert isinstance(mutations, list)
