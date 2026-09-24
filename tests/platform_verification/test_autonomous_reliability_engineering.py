"""
Test Suite: Phase 3I.12 Autonomous Reliability Engineering, Continuous Optimization & Operational Intelligence
"""
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.autonomous_reliability_engineering.domain.models import (
    AutonomousCertificationTier,
    AutonomousArchitectureReport,
    AnomalyIntelligenceReport,
    FailurePredictionReport,
    OptimizationRecommendationReport,
    CapacityIntelligenceReport,
    AutonomousScalingReport,
    SelfOptimizationReport,
    IncidentLearningReport,
    ReliabilityKnowledgeGraphReport,
    AutonomousSafetyReport,
    ContinuousReliabilityImprovementReport,
    AutonomousReliabilityCertificationReport,
)

from app.platform_verification.autonomous_reliability_engineering.verifiers import (
    AutonomousArchitectureVerifier,
    AnomalyIntelligenceVerifier,
    FailurePredictionVerifier,
    OptimizationEngineVerifier,
    CapacityPlanningVerifier,
    AutonomousScalingVerifier,
    SelfOptimizationVerifier,
    IncidentLearningVerifier,
    KnowledgeGraphVerifier,
    DecisionSafetyVerifier,
    ContinuousImprovementLoopVerifier,
)
from app.platform_verification.autonomous_reliability_engineering.scoring import (
    AutonomousReliabilityScorer,
)
from app.platform_verification.autonomous_reliability_engineering.runtime import (
    AutonomousReliabilityRuntime,
)
from app.platform_verification.autonomous_reliability_engineering.api import router


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


# ─── 1. Verifier Unit Tests ───────────────────────────────────────────────────

def test_autonomous_architecture_verifier():
    verifier = AutonomousArchitectureVerifier()
    report = verifier.verify()
    assert isinstance(report, AutonomousArchitectureReport)
    assert report.status == "PASS"
    assert report.intelligence_layer is True
    assert report.optimization_engine is True
    assert report.learning_system is True
    assert len(report.components) == 7


def test_anomaly_intelligence_verifier():
    verifier = AnomalyIntelligenceVerifier()
    report = verifier.verify()
    assert isinstance(report, AnomalyIntelligenceReport)
    assert report.status == "PASS"
    assert report.metrics_anomaly_detection_active is True
    assert report.logs_anomaly_detection_active is True
    assert report.traces_anomaly_detection_active is True
    assert report.anomaly_detection_accuracy_pct == 100.0
    assert len(report.anomalies_detected) == 4


def test_failure_prediction_verifier():
    verifier = FailurePredictionVerifier()
    report = verifier.verify()
    assert isinstance(report, FailurePredictionReport)
    assert report.status == "PASS"
    assert report.resource_exhaustion_predicted is True
    assert report.queue_overflow_predicted is True
    assert report.db_saturation_predicted is True
    assert report.ai_provider_risk_predicted is True
    assert report.mean_prediction_confidence >= 0.90
    assert len(report.predictions) == 4


def test_optimization_engine_verifier():
    verifier = OptimizationEngineVerifier()
    report = verifier.verify()
    assert isinstance(report, OptimizationRecommendationReport)
    assert report.status == "PASS"
    assert report.performance_optimized is True
    assert report.cost_optimized is True
    assert report.resource_allocation_optimized is True
    assert report.architecture_optimized is True
    assert len(report.recommendations) == 4


def test_capacity_planning_verifier():
    verifier = CapacityPlanningVerifier()
    report = verifier.verify()
    assert isinstance(report, CapacityIntelligenceReport)
    assert report.status == "PASS"
    assert report.worker_capacity_forecasted is True
    assert report.db_capacity_forecasted is True
    assert report.queue_capacity_forecasted is True
    assert report.forecasting_accuracy_pct >= 95.0
    assert len(report.forecasts) == 3


def test_autonomous_scaling_verifier():
    verifier = AutonomousScalingVerifier()
    report = verifier.verify()
    assert isinstance(report, AutonomousScalingReport)
    assert report.status == "PASS"
    assert report.scaling_accuracy_pct >= 95.0
    assert report.rollback_safety_verified is True
    assert len(report.decisions) == 3


def test_self_optimization_verifier():
    verifier = SelfOptimizationVerifier()
    report = verifier.verify()
    assert isinstance(report, SelfOptimizationReport)
    assert report.status == "PASS"
    assert report.database_self_optimized is True
    assert report.queue_self_optimized is True
    assert report.ai_pipeline_self_optimized is True
    assert report.infrastructure_self_optimized is True
    assert report.avg_performance_gain_pct >= 30.0
    assert len(report.optimizations) == 4


def test_incident_learning_verifier():
    verifier = IncidentLearningVerifier()
    report = verifier.verify()
    assert isinstance(report, IncidentLearningReport)
    assert report.status == "PASS"
    assert report.rca_automation_verified is True
    assert report.pattern_extraction_active is True
    assert report.knowledge_update_verified is True
    assert report.recurrence_prevention_rate_pct == 100.0
    assert len(report.learning_cycles) == 3


def test_knowledge_graph_verifier():
    verifier = KnowledgeGraphVerifier()
    report = verifier.verify()
    assert isinstance(report, ReliabilityKnowledgeGraphReport)
    assert report.status == "PASS"
    assert report.nodes_count >= 15
    assert report.edges_count >= 12
    assert report.query_lookup_latency_ms < 10.0
    assert report.graph_coverage_score_pct == 100.0


def test_decision_safety_verifier():
    verifier = DecisionSafetyVerifier()
    report = verifier.verify()
    assert isinstance(report, AutonomousSafetyReport)
    assert report.status == "PASS"
    assert report.safe_tier_automation_verified is True
    assert report.controlled_tier_approval_verified is True
    assert report.restricted_tier_human_gate_verified is True
    assert report.zero_harmful_action_guarantee is True
    assert len(report.safety_rules) == 5


def test_continuous_improvement_loop_verifier():
    verifier = ContinuousImprovementLoopVerifier()
    report = verifier.verify()
    assert isinstance(report, ContinuousReliabilityImprovementReport)
    assert report.status == "PASS"
    assert report.loop_active is True
    assert report.overall_reliability_gain_pct >= 10.0
    assert report.incident_reduction_pct >= 50.0
    assert len(report.improvement_metrics) == 4


# ─── 2. Scorer Unit Tests ─────────────────────────────────────────────────────

def test_autonomous_reliability_scorer():
    runtime = AutonomousReliabilityRuntime()
    verification_results = runtime.execute_all_verifications()
    scorer = AutonomousReliabilityScorer()
    cert = scorer.compute_certification(verification_results)

    assert isinstance(cert, AutonomousReliabilityCertificationReport)
    assert cert.composite_reliability_score_pct >= 95.0
    assert cert.certification_tier == AutonomousCertificationTier.AUTONOMOUS_RELIABILITY_CERTIFIED
    assert cert.certification_granted is True
    assert len(cert.category_scores) == 7

    # Verify category weights sum to 100%
    total_weight = sum(c.weight_pct for c in cert.category_scores)
    assert total_weight == 100.0


# ─── 3. Exporter Unit Tests ───────────────────────────────────────────────────

def test_autonomous_reliability_exporter(tmp_path):
    output_dir = tmp_path / "auto_rel_test"
    runtime = AutonomousReliabilityRuntime(output_dir=str(output_dir))
    pipeline_result = runtime.run_pipeline()

    exported_files = pipeline_result["exported_files"]
    assert len(exported_files) == 13  # 11 reports + certification_report.json + metadata.json

    metadata_path = output_dir / "metadata.json"
    assert metadata_path.exists()
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["composite_reliability_score_pct"] >= 95.0
    assert metadata["certification_tier"] == AutonomousCertificationTier.AUTONOMOUS_RELIABILITY_CERTIFIED.value
    assert len(metadata["manifest"]) == 12


# ─── 4. REST API Integration Tests ────────────────────────────────────────────

def test_api_status_endpoint(api_client):
    response = api_client.get("/api/v1/autonomous-reliability/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ONLINE"
    assert data["loop_status"] == "ACTIVE_CONTINUOUS_IMPROVEMENT"


def test_api_predictions_endpoint(api_client):
    response = api_client.get("/api/v1/autonomous-reliability/predictions")
    assert response.status_code == 200
    data = response.json()
    assert data["resource_exhaustion_predicted"] is True
    assert len(data["predictions"]) == 4


def test_api_optimizations_endpoint(api_client):
    response = api_client.get("/api/v1/autonomous-reliability/optimizations")
    assert response.status_code == 200
    data = response.json()
    assert data["performance_optimized"] is True
    assert len(data["recommendations"]) == 4


def test_api_self_optimization_endpoint(api_client):
    response = api_client.get("/api/v1/autonomous-reliability/self-optimization")
    assert response.status_code == 200
    data = response.json()
    assert data["database_self_optimized"] is True
    assert len(data["optimizations"]) == 4


def test_api_knowledge_graph_endpoint(api_client):
    response = api_client.get("/api/v1/autonomous-reliability/knowledge-graph")
    assert response.status_code == 200
    data = response.json()
    assert data["nodes_count"] >= 15
    assert len(data["nodes"]) >= 15


def test_api_certification_endpoint(api_client):
    response = api_client.get("/api/v1/autonomous-reliability/certification")
    assert response.status_code == 200
    data = response.json()
    assert data["composite_reliability_score_pct"] >= 95.0
    assert data["certification_tier"] == AutonomousCertificationTier.AUTONOMOUS_RELIABILITY_CERTIFIED.value


def test_api_run_verification_endpoint(api_client):
    response = api_client.post("/api/v1/autonomous-reliability/run-verification")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["certification_granted"] is True
    assert data["composite_reliability_score_pct"] >= 95.0
    assert data["exported_files_count"] == 13
