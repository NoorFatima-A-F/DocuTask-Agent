from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api_strategy_synthesize():
    response = client.post("/api/v1/evolution/strategy/synthesize", json={"goal_intent": "extract_financial_invoice", "branch_index": 0})
    assert response.status_code == 200
    data = response.json()
    assert "strategy_id" in data
    assert "dag" in data
    assert "evaluation" in data
    assert data["evaluation"]["novelty_score"] >= 0


def test_api_strategy_mutate():
    response = client.post("/api/v1/evolution/strategy/mutate", json={"mutation_type": "OPERATOR_SWAP"})
    assert response.status_code == 200
    data = response.json()
    assert "mutated_dag" in data
    assert "novelty_delta" in data


def test_api_planner_evolve():
    response = client.post("/api/v1/evolution/planner/evolve", json={"weakness_diagnosis": "Tail latency spike", "simulated_trials": 100})
    assert response.status_code == 200
    data = response.json()
    assert data["is_promoted"] is True
    assert "candidate_version" in data


def test_api_planner_generations():
    response = client.get("/api/v1/evolution/planner/generations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


def test_api_simulation_run():
    response = client.post("/api/v1/evolution/simulation/run", json={"mission_count": 20, "arrival_rate_per_sec": 5.0, "chaos_fault_rate": 0.01})
    assert response.status_code == 200
    data = response.json()
    assert data["processed_missions_count"] == 20
    assert data["total_virtual_workers"] == 1000


def test_api_causal_intervene():
    response = client.post("/api/v1/evolution/causal/intervene", json={"treatment_variable": "worker_concurrency", "treatment_value": 8.0, "outcome_variable": "total_latency_ms"})
    assert response.status_code == 200
    data = response.json()
    assert "causal_effect_ate" in data
    assert data["target_outcome_variable"] == "total_latency_ms"


def test_api_deliberation_session():
    response = client.post("/api/v1/evolution/deliberation/session", json={"mission_id": "api_test_mission"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["participating_agents"]) == 8
    assert "final_ratified_strategy_id" in data
