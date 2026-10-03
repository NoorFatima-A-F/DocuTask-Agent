"""End-to-End Planning Runtime and FastAPI Integration Tests."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.runtime.planning import AutonomousPlanningRuntime


@pytest.fixture
def client():
    return TestClient(app)


def test_autonomous_planning_runtime_e2e():
    runtime = AutonomousPlanningRuntime()
    mission_id = "test_e2e_m1"
    raw_intent = "Process multi-page financial statement, extract tables, and check balance sheet equation"

    plan = runtime.plan_mission(mission_id, raw_intent, user_constraints={"budget_usd": 0.20})

    assert plan.mission_id == mission_id
    assert len(plan.candidate_strategies) == 4
    assert plan.selected_dag is not None
    assert len(plan.selected_dag.nodes) >= 4
    assert len(plan.counterfactual_explanations) >= 4

    # Perform outcome self-evaluation with realistic metrics
    sel_id = plan.selection_record.selected_strategy_id
    pred_lat = plan.latency_predictions[sel_id].critical_path_ms
    pred_cost = plan.cost_predictions[sel_id].total_cost_usd

    calib = runtime.evaluate_mission_outcome(
        mission_id=mission_id,
        actual_latency_ms=pred_lat * 1.02,
        actual_cost_usd=pred_cost * 1.02,
        actual_accuracy=0.985,
        actual_failure=False,
    )
    assert calib.overall_calibration_score >= 0.70
    assert len(calib.root_causes) > 0


def test_fastapi_planning_endpoints(client):
    # 1. Plan Mission via API
    plan_resp = client.post("/api/v1/planning/plan", json={
        "mission_id": "api_mission_001",
        "intent": "Extract bill of lading and customs clearance entities",
        "user_constraints": {"budget_usd": 0.50, "max_latency_ms": 4000.0},
    })
    assert plan_resp.status_code == 200
    plan_data = plan_resp.json()
    assert plan_data["mission_id"] == "api_mission_001"
    assert len(plan_data["candidate_strategies"]) == 4

    # 2. Get Strategy Matrix
    matrix_resp = client.get("/api/v1/planning/strategies/api_mission_001")
    assert matrix_resp.status_code == 200
    matrix_data = matrix_resp.json()
    assert len(matrix_data["entries"]) == 4

    # 3. Query Counterfactuals
    cf_resp = client.post("/api/v1/planning/counterfactuals/query", json={
        "mission_id": "api_mission_001",
        "query_type": "WHAT_IF_WEIGHT_CHANGED",
        "weight_overrides": {"w_accuracy": 0.8, "w_latency": 0.1, "w_cost": 0.05, "w_risk": 0.05},
    })
    assert cf_resp.status_code == 200
    assert "winner" in cf_resp.json()["summary_explanation"].lower() or "winning" in cf_resp.json()["summary_explanation"].lower()

    # 4. Get Active Mutable DAG
    dag_resp = client.get("/api/v1/planning/dag/api_mission_001")
    assert dag_resp.status_code == 200
    dag_data = dag_resp.json()
    first_node_id = list(dag_data["nodes"].keys())[0]

    # 5. Mutate Active DAG (Split node)
    mutate_resp = client.post("/api/v1/planning/dag/api_mission_001/mutate", json={
        "mutation_type": "NODE_SPLIT",
        "target_node_id": first_node_id,
        "split_count": 2,
        "rationale": "Parallel page chunking",
    })
    assert mutate_resp.status_code == 200
    assert mutate_resp.json()["version"] > 1

    # 6. Adaptive Replan
    replan_resp = client.post("/api/v1/planning/replan/api_mission_001", json={
        "trigger_type": "LATENCY_DRIFT",
        "rationale": "Upstream latency spike detected",
    })
    assert replan_resp.status_code == 200

    # 7. Evaluate Mission Outcome
    eval_resp = client.post("/api/v1/planning/evaluate/api_mission_001", json={
        "mission_id": "api_mission_001",
        "actual_latency_ms": 1950.0,
        "actual_cost_usd": 0.0045,
        "actual_accuracy": 0.99,
    })
    assert eval_resp.status_code == 200
    assert eval_resp.json()["overall_calibration_score"] > 0

    # 8. List Capabilities
    caps_resp = client.get("/api/v1/planning/capabilities")
    assert caps_resp.status_code == 200
    assert len(caps_resp.json()) >= 6
