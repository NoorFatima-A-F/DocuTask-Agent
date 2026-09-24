"""
AOIS-HROP Phase 13.7 - Pytest Test Suite
Tests operational runtime, health engine, incidents, diagnosis, self-healing, recovery, prediction, chaos, resilience, governance, and API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.runtime.operations import (
    OperationalRuntime,
    HealthEngine,
    IncidentEngine,
    DiagnosisEngine,
    HealingEngine,
    RecoveryEngine,
    ChaosEngine,
    ResilienceEngine,
    OperationalGovernance,
    FailurePredictor,
    RiskForecastEngine,
    SubsystemType,
)


@pytest.fixture
def client():
    return TestClient(app)


def test_operational_runtime_liveness():
    runtime = OperationalRuntime()
    overview = runtime.get_runtime_overview()
    assert overview["status"] == "OPERATIONAL_AUTONOMIC"
    assert overview["heartbeat"]["is_fresh"] is True
    assert overview["inspection"]["starvation_risk"] >= 0.0
    assert overview["supervision_summary"]["all_healthy"] is True


def test_watchdog_retry_storm_and_stalls():
    runtime = OperationalRuntime()
    # Simulate repeated retries
    for _ in range(6):
        runtime.watchdog.increment_task_retry("task-invoice-extract-01")

    alerts = runtime.watchdog.get_active_alerts()
    assert len(alerts) >= 1
    assert any(a.alert_type == "RETRY_STORM" for a in alerts)


def test_health_scoring_and_composite_index():
    health = HealthEngine()
    res = health.evaluate_platform_health()
    assert res["composite_score"] > 80.0
    assert "WORKERS" in res["subsystems"]
    assert "PLANNER" in res["subsystems"]
    assert res["forecast"]["sla_breach_risk_pct"] >= 0.0


def test_dependency_health_propagation():
    health = HealthEngine()
    impacts = health.dependency_graph.calculate_propagated_impact("DATABASE", initial_score=40.0)
    assert "DATABASE" in impacts
    assert impacts["DATABASE"] == 40.0
    # Downstream components should have damped impacts
    assert "WORKERS" in impacts
    assert impacts["WORKERS"] < 100.0


def test_incident_detection_and_timeline():
    incident_engine = IncidentEngine()
    result = incident_engine.record_or_detect_incident(
        subsystem=SubsystemType.WORKERS,
        error_rate=0.15,
        affected_missions=["m-001", "m-002"],
    )
    assert result is not None
    assert result["severity"] in ("MEDIUM", "HIGH", "CRITICAL")
    assert result["impact"]["affected_missions"] == 2
    assert len(result["timeline"]) >= 1


def test_autonomous_diagnosis_causal_reasoning():
    diag_engine = DiagnosisEngine()
    diag = diag_engine.diagnose_incident(
        incident_id="inc-test-01",
        affected_subsystems=["WORKERS", "PLANNER"],
        error_type="HUNG_WORKER",
    )
    assert diag["confidence"] > 0.60
    assert diag["primary_culprit"] in ("WORKERS", "PLANNER")
    assert diag["recommended_action"] == "WORKER_RESTART"
    assert len(diag["causal_chain"]) >= 2


def test_self_healing_execution_and_audit():
    healing_engine = HealingEngine()
    heal_res = healing_engine.execute_healing(
        incident_id="inc-test-01",
        subsystem=SubsystemType.WORKERS,
        error_type="WORKER_CRASH",
        target_resource="worker-th-04",
    )
    assert heal_res["status"] == "COMPLETED"
    assert heal_res["validation_passed"] is True
    assert len(heal_res["audit_hash"]) == 64
    assert healing_engine.audit_ledger.verify_integrity() is True


def test_recovery_orchestration():
    recovery_engine = RecoveryEngine()
    plan = recovery_engine.plan_recovery("mission-101", strategy="CHECKPOINT_ROLLBACK")
    assert len(plan.steps) == 5

    res = recovery_engine.execute_recovery("mission-101", strategy="CHECKPOINT_ROLLBACK")
    assert res["status"] == "COMPLETED"
    assert res["consistency_verified"] is True
    assert res["continuation"]["status"] == "EXECUTING_NORMAL"


def test_predictive_failure_and_risk_forecasting():
    predictor = FailurePredictor()
    risk_engine = RiskForecastEngine(predictor)
    predictions = predictor.generate_all_predictions()
    assert len(predictions) >= 4

    risk = risk_engine.compute_risk_forecast(predictions)
    assert 0.0 <= risk.composite_risk_index <= 1.0
    assert risk.financial_exposure_usd >= 0.0


def test_chaos_fault_injection_and_benchmark():
    chaos = ChaosEngine()
    exp = chaos.run_experiment(
        name="Worker Crash Chaos Test",
        target_subsystem="WORKERS",
        fault_type="WORKER_CRASH",
    )
    assert exp["status"] == "COMPLETED"
    assert exp["resilience_score"] > 70.0
    assert exp["invariants_preserved"] is True


def test_resilience_and_governance():
    resilience_engine = ResilienceEngine()
    prof = resilience_engine.generate_resilience_profile()
    assert prof.resilience_score > 90.0
    assert prof.availability_percentage > 99.0
    assert prof.mttr_seconds < 5.0

    gov = OperationalGovernance()
    gov_overview = gov.get_governance_overview()
    assert gov_overview["status"] == "COMPLIANT_ENFORCED"
    assert gov_overview["compliance"]["soc2_pct"] == 100.0


def test_operations_api_endpoints(client):
    # Health endpoint
    r = client.get("/api/v1/operations/health")
    assert r.status_code == 200
    assert "composite_score" in r.json()

    # Resilience endpoint
    r = client.get("/api/v1/operations/resilience")
    assert r.status_code == 200
    assert "availability_percentage" in r.json()

    # Predictions endpoint
    r = client.get("/api/v1/operations/predictions")
    assert r.status_code == 200
    assert "risk_forecast" in r.json()

    # Healing trigger POST
    r = client.post(
        "/api/v1/operations/heal",
        json={
            "incident_id": "inc-api-test-01",
            "subsystem": "WORKERS",
            "error_type": "WORKER_CRASH",
            "target_resource": "worker-pool-alpha",
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "COMPLETED"

    # Recovery trigger POST
    r = client.post(
        "/api/v1/operations/recover",
        json={
            "mission_id": "mission-api-01",
            "strategy": "CHECKPOINT_ROLLBACK",
            "snapshot_id": "snap_step_004",
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "COMPLETED"

    # Chaos trigger POST
    r = client.post(
        "/api/v1/operations/chaos/start",
        json={
            "name": "API Chaos Verification",
            "target_subsystem": "WORKERS",
            "fault_type": "WORKER_CRASH",
            "intensity": 0.5,
            "duration_sec": 2.0,
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "COMPLETED"
