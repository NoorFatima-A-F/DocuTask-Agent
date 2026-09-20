import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api_get_beliefs():
    response = client.get("/api/v1/intelligence/beliefs")
    assert response.status_code == 200
    data = response.json()
    assert "mission_id" in data
    assert "beliefs" in data
    assert "total_entropy_bits" in data
    assert len(data["beliefs"]) > 0


def test_api_bayesian_update():
    payload = {
        "variable_name": "ocr_success",
        "observed_signal": "UNIT_TEST_SIGNAL",
        "success_increment": 4.0,
        "failure_increment": 1.0,
        "likelihood": 0.95,
        "worker_id": "test_worker",
    }
    response = client.post("/api/v1/intelligence/bayesian/update", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["variable_name"] == "ocr_success"
    assert "posterior_mean" in data
    assert "credible_interval_95" in data


def test_api_world_forecast():
    response = client.get("/api/v1/intelligence/world/forecast")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


def test_api_evoi_evaluate():
    response = client.get("/api/v1/intelligence/evoi/evaluate")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


def test_api_governance_verify():
    payload = {
        "mission_id": "m_test_fastapi",
        "strategy_id": "strat_delta_pareto",
        "total_cost_usd": 0.0022,
        "budget_limit_usd": 0.50,
        "critical_path_ms": 850.0,
        "sla_limit_ms": 10000.0,
        "peak_memory_mb": 4096.0,
        "estimated_accuracy": 0.98,
    }
    response = client.post("/api/v1/intelligence/governance/verify", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mission_id"] == "m_test_fastapi"
    assert data["is_fully_satisfiable"] is True


def test_api_benchmark_run():
    response = client.get("/api/v1/intelligence/benchmark/run")
    assert response.status_code == 200
    data = response.json()
    assert "winner_algorithm" in data
    assert "evaluated_algorithms" in data
