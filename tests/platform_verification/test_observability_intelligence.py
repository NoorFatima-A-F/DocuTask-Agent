"""
Test Suite: Phase 3I.9 Observability Intelligence, Predictive Reliability & AIOps Maturity
"""
import os
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.observability_intelligence.domain.models import (
    PredictiveCertificationTier,
    RiskLevel,
    TrendDirection,
    AIOpsArchitectureReport,
    OperationalDataQualityReport,
    FailurePredictionReport,
    CapacityForecastingReport,
    BehaviorBaselineReport,
    PredictiveAnomalyReport,
    ReliabilityIntelligenceReport,
    IncidentPreventionReport,
    DeploymentIntelligenceReport,
    AIReliabilityMonitoringReport,
    ContinuousOptimizationReport,
    AIOpsExplainabilityReport,
    AIOpsValidationReport,
    PredictiveCertificationReport,
)

from app.platform_verification.observability_intelligence.verifiers.aiops_architecture_verifier import (
    AIOpsArchitectureVerifier,
)
from app.platform_verification.observability_intelligence.verifiers.data_quality_verifier import (
    OperationalDataQualityVerifier,
)
from app.platform_verification.observability_intelligence.verifiers.failure_prediction_verifier import (
    FailurePredictionVerifier,
)
from app.platform_verification.observability_intelligence.verifiers.capacity_forecasting_verifier import (
    CapacityForecastingVerifier,
)
from app.platform_verification.observability_intelligence.verifiers.behavior_baseline_verifier import (
    BehaviorBaselineVerifier,
)
from app.platform_verification.observability_intelligence.verifiers.predictive_anomaly_verifier import (
    PredictiveAnomalyVerifier,
)
from app.platform_verification.observability_intelligence.verifiers.reliability_score_verifier import (
    ReliabilityScoreVerifier,
)
from app.platform_verification.observability_intelligence.verifiers.incident_prevention_verifier import (
    IncidentPreventionVerifier,
)
from app.platform_verification.observability_intelligence.verifiers.deployment_intelligence_verifier import (
    DeploymentIntelligenceVerifier,
)
from app.platform_verification.observability_intelligence.verifiers.ai_reliability_verifier import (
    AIReliabilityVerifier,
)
from app.platform_verification.observability_intelligence.verifiers.continuous_optimization_verifier import (
    ContinuousOptimizationVerifier,
)
from app.platform_verification.observability_intelligence.verifiers.aiops_explainability_verifier import (
    AIOpsExplainabilityVerifier,
)
from app.platform_verification.observability_intelligence.verifiers.aiops_validation_verifier import (
    AIOpsValidationVerifier,
)
from app.platform_verification.observability_intelligence.runtime.observability_intelligence_runtime import (
    ObservabilityIntelligenceRuntime,
)
from app.platform_verification.observability_intelligence.api.observability_intelligence_api import (
    router as intelligence_router,
)


# ─── 1. Individual Verifier Tests ─────────────────────────────────────────────

def test_aiops_architecture_verifier():
    verifier = AIOpsArchitectureVerifier()
    report = verifier.verify_aiops_architecture()

    assert isinstance(report, AIOpsArchitectureReport)
    assert report.components_count == 8
    assert len(report.components) == 8
    assert report.prediction_enabled is True
    assert report.feedback_loop is True
    assert report.status == "PASS"


def test_data_quality_verifier():
    verifier = OperationalDataQualityVerifier()
    report = verifier.verify_data_quality()

    assert isinstance(report, OperationalDataQualityReport)
    assert len(report.dimensions) == 4
    assert report.overall_quality_score_pct >= 95.0
    assert report.status == "PASS"


def test_failure_prediction_verifier():
    verifier = FailurePredictionVerifier()
    report = verifier.verify_failure_prediction()

    assert isinstance(report, FailurePredictionReport)
    assert len(report.predictions) >= 3
    assert report.average_prediction_confidence >= 0.85
    assert report.early_warning_lead_time_min >= 30
    assert report.status == "PASS"


def test_capacity_forecasting_verifier():
    verifier = CapacityForecastingVerifier()
    report = verifier.verify_capacity_forecasting()

    assert isinstance(report, CapacityForecastingReport)
    assert len(report.forecasts) >= 3
    assert report.headroom_guaranteed is True
    assert report.forecast_accuracy_pct >= 95.0


def test_behavior_baseline_verifier():
    verifier = BehaviorBaselineVerifier()
    report = verifier.verify_behavior_baselines()

    assert isinstance(report, BehaviorBaselineReport)
    assert len(report.patterns) >= 4
    assert report.adaptive_baselines_verified is True


def test_predictive_anomaly_verifier():
    verifier = PredictiveAnomalyVerifier()
    report = verifier.verify_predictive_anomalies()

    assert isinstance(report, PredictiveAnomalyReport)
    assert len(report.subtle_anomalies) >= 3
    assert report.proactive_detection_active is True


def test_reliability_score_verifier():
    verifier = ReliabilityScoreVerifier()
    report = verifier.verify_reliability_score()

    assert isinstance(report, ReliabilityIntelligenceReport)
    assert report.system_health_score >= 95.0
    assert report.risk_level == RiskLevel.LOW
    assert report.trend == TrendDirection.IMPROVING
    assert len(report.factors) == 5


def test_incident_prevention_verifier():
    verifier = IncidentPreventionVerifier()
    report = verifier.verify_incident_prevention()

    assert isinstance(report, IncidentPreventionReport)
    assert report.total_incidents_prevented >= 4
    assert report.prevention_success_rate_pct >= 95.0
    assert len(report.scenarios) >= 4


def test_deployment_intelligence_verifier():
    verifier = DeploymentIntelligenceVerifier()
    report = verifier.verify_deployment_intelligence()

    assert isinstance(report, DeploymentIntelligenceReport)
    assert len(report.metrics_audited) >= 4
    assert report.deployment_safe_to_promote is True
    assert report.zero_regression_verified is True


def test_ai_reliability_verifier():
    verifier = AIReliabilityVerifier()
    report = verifier.verify_ai_reliability()

    assert isinstance(report, AIReliabilityMonitoringReport)
    assert len(report.dimensions) >= 5
    assert report.ai_pipeline_healthy is True
    assert report.model_version == "gemini-2.5-flash"


def test_continuous_optimization_verifier():
    verifier = ContinuousOptimizationVerifier()
    report = verifier.verify_continuous_optimization()

    assert isinstance(report, ContinuousOptimizationReport)
    assert len(report.recommendations) >= 3
    assert report.optimization_engine_active is True


def test_aiops_explainability_verifier():
    verifier = AIOpsExplainabilityVerifier()
    report = verifier.verify_aiops_explainability()

    assert isinstance(report, AIOpsExplainabilityReport)
    assert len(report.decisions) >= 3
    assert report.all_decisions_explainable is True


def test_aiops_validation_verifier():
    verifier = AIOpsValidationVerifier()
    report = verifier.verify_aiops_validation()

    assert isinstance(report, AIOpsValidationReport)
    assert len(report.validation_tests) >= 4
    assert report.all_evaluations_passed is True


# ─── 2. Scorer Tests ──────────────────────────────────────────────────────────

def test_predictive_reliability_scorer():
    runtime = ObservabilityIntelligenceRuntime()
    scorer = runtime.scorer

    cert = scorer.calculate_certification_score(
        arch_report=runtime.arch_verifier.verify_aiops_architecture(),
        data_report=runtime.data_verifier.verify_data_quality(),
        pred_report=runtime.pred_verifier.verify_failure_prediction(),
        capacity_report=runtime.capacity_verifier.verify_capacity_forecasting(),
        baseline_report=runtime.baseline_verifier.verify_behavior_baselines(),
        anomaly_report=runtime.anomaly_verifier.verify_predictive_anomalies(),
        score_report=runtime.score_verifier.verify_reliability_score(),
        prevention_report=runtime.prevention_verifier.verify_incident_prevention(),
        deploy_report=runtime.deploy_verifier.verify_deployment_intelligence(),
        ai_report=runtime.ai_verifier.verify_ai_reliability(),
        opt_report=runtime.opt_verifier.verify_continuous_optimization(),
        explain_report=runtime.explain_verifier.verify_aiops_explainability(),
        val_report=runtime.val_verifier.verify_aiops_validation(),
    )

    assert isinstance(cert, PredictiveCertificationReport)
    assert len(cert.pillar_scores) == 6
    assert cert.overall_score_pct >= 95.0
    assert cert.certification_granted is True
    assert cert.certification_tier == PredictiveCertificationTier.PREDICTIVE_RELIABILITY_READY

    total_weight = sum(p.weight_pct for p in cert.pillar_scores)
    assert total_weight == 100.0


# ─── 3. Exporter & Artifact Verification ──────────────────────────────────────

def test_observability_intelligence_evidence_exporter(tmp_path):
    output_dir = str(tmp_path / "intelligence_test_export")
    runtime = ObservabilityIntelligenceRuntime(output_dir=output_dir)
    results = runtime.run_full_verification()

    assert results["status"] == "SUCCESS"
    assert os.path.exists(output_dir)

    expected_files = [
        "aiops_architecture_report.json",
        "data_quality_report.json",
        "prediction_report.json",
        "capacity_report.json",
        "baseline_report.json",
        "anomaly_prediction_report.json",
        "reliability_score_report.json",
        "prevention_report.json",
        "deployment_intelligence_report.json",
        "ai_reliability_report.json",
        "optimization_report.json",
        "explainability_report.json",
        "validation_report.json",
        "certification_report.json",
        "metadata.json",
    ]

    for fname in expected_files:
        fpath = os.path.join(output_dir, fname)
        assert os.path.exists(fpath), f"Missing artifact: {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert len(data) > 0


# ─── 4. REST API Endpoints ───────────────────────────────────────────────────

@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(intelligence_router)
    return TestClient(app)


def test_api_run_verification(api_client):
    response = api_client.post("/api/v1/observability-intelligence/run-verification")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["certification_granted"] is True
    assert data["overall_score_pct"] >= 95.0


def test_api_status(api_client):
    response = api_client.get("/api/v1/observability-intelligence/status")
    assert response.status_code == 200
    data = response.json()
    assert data["certification_granted"] is True
    assert data["overall_score_pct"] >= 95.0
    assert len(data["pillar_scores"]) == 6


def test_api_predictions(api_client):
    response = api_client.get("/api/v1/observability-intelligence/predictions")
    assert response.status_code == 200
    data = response.json()
    assert "failure_predictions" in data
    assert "predictive_anomalies" in data
    assert "explainable_decisions" in data


def test_api_capacity_forecast(api_client):
    response = api_client.get("/api/v1/observability-intelligence/capacity-forecast")
    assert response.status_code == 200
    data = response.json()
    assert "capacity_forecasts" in data
    assert "behavioral_baselines" in data


def test_api_ai_reliability(api_client):
    response = api_client.get("/api/v1/observability-intelligence/ai-reliability")
    assert response.status_code == 200
    data = response.json()
    assert "ai_model_reliability" in data
    assert "continuous_optimizations" in data
    assert "deployment_impact" in data
