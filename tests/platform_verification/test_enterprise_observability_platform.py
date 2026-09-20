"""
Test Suite: Phase 3I.11 Enterprise Observability Intelligence Platform Integration & Global Reliability Control
"""
import os
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.enterprise_observability_platform.domain.models import (
    GlobalCertificationTier,
    EnvironmentType,
    GlobalRiskLevel,
    GlobalTrend,
    ControlPlaneArchitectureReport,
    TelemetryFederationReport,
    ObservabilityStandardizationReport,
    EnvironmentDriftReport,
    GlobalReliabilityReport,
    CrossEnvironmentIncidentReport,
    ProductionReadinessGateReport,
    MultiRegionReliabilityReport,
    CloudObservabilityIntegrationReport,
    DashboardFederationReport,
    GlobalAutomationControlReport,
    GlobalOperationsCertificationReport,
)

from app.platform_verification.enterprise_observability_platform.verifiers import (
    ControlPlaneVerifier,
    TelemetryFederationVerifier,
    ObservabilityStandardizationVerifier,
    DriftDetectionVerifier,
    GlobalReliabilityVerifier,
    CrossEnvironmentIncidentVerifier,
    ProductionReadinessVerifier,
    MultiRegionVerifier,
    CloudIntegrationVerifier,
    DashboardFederationVerifier,
    AutomationControlVerifier,
)
from app.platform_verification.enterprise_observability_platform.scoring import (
    GlobalOperationsScorer,
)
from app.platform_verification.enterprise_observability_platform.exporter import (
    EnterpriseObservabilityExporter,
)
from app.platform_verification.enterprise_observability_platform.runtime import (
    EnterpriseObservabilityRuntime,
)
from app.platform_verification.enterprise_observability_platform.api import router


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


# ─── 1. Verifier Unit Tests ───────────────────────────────────────────────────

def test_control_plane_verifier():
    verifier = ControlPlaneVerifier()
    report = verifier.verify()
    assert isinstance(report, ControlPlaneArchitectureReport)
    assert report.status == "PASS"
    assert report.environments_connected == 5
    assert report.central_control_enabled is True
    assert report.federation_status == "PASS"
    assert len(report.components) == 5


def test_telemetry_federation_verifier():
    verifier = TelemetryFederationVerifier()
    report = verifier.verify()
    assert isinstance(report, TelemetryFederationReport)
    assert report.status == "PASS"
    assert len(report.environments_federated) == 5
    assert report.metrics_federation_verified is True
    assert report.log_aggregation_verified is True
    assert report.trace_correlation_verified is True
    assert report.cross_env_comparison_enabled is True


def test_observability_standardization_verifier():
    verifier = ObservabilityStandardizationVerifier()
    report = verifier.verify()
    assert isinstance(report, ObservabilityStandardizationReport)
    assert report.status == "PASS"
    assert report.standardization_compliance_pct == 100.0
    assert len(report.required_metrics) == 7
    assert len(report.required_log_fields) == 6
    assert len(report.required_trace_spans) == 6


def test_drift_detection_verifier():
    verifier = DriftDetectionVerifier()
    report = verifier.verify()
    assert isinstance(report, EnvironmentDriftReport)
    assert report.status == "PASS"
    assert report.infrastructure_drift_monitored is True
    assert report.configuration_drift_monitored is True
    assert report.observability_drift_monitored is True
    assert report.zero_unauthorized_drift_verified is True
    assert len(report.drift_checks) == 5


def test_global_reliability_verifier():
    verifier = GlobalReliabilityVerifier()
    report = verifier.verify()
    assert isinstance(report, GlobalReliabilityReport)
    assert report.status == "PASS"
    assert report.global_reliability_score >= 95.0
    assert report.risk_level == GlobalRiskLevel.LOW
    assert report.trend == GlobalTrend.STABLE
    assert report.production_availability_pct >= 99.9
    assert len(report.dimensions) == 5


def test_cross_environment_incident_verifier():
    verifier = CrossEnvironmentIncidentVerifier()
    report = verifier.verify()
    assert isinstance(report, CrossEnvironmentIncidentReport)
    assert report.status == "PASS"
    assert report.incident_correlation_enabled is True
    assert report.historical_learning_active is True
    assert report.prevention_success_rate_pct == 100.0
    assert len(report.correlations) == 3


def test_production_readiness_verifier():
    verifier = ProductionReadinessVerifier()
    report = verifier.verify()
    assert isinstance(report, ProductionReadinessGateReport)
    assert report.status == "PASS"
    assert report.overall_health_score >= 90.0
    assert report.no_critical_vulnerabilities is True
    assert report.observability_complete is True
    assert report.rollback_available is True
    assert report.release_approval_granted is True
    assert len(report.stages) == 7


def test_multi_region_verifier():
    verifier = MultiRegionVerifier()
    report = verifier.verify()
    assert isinstance(report, MultiRegionReliabilityReport)
    assert report.status == "PASS"
    assert report.regional_health_monitoring is True
    assert report.failover_visibility is True
    assert report.automated_failover_verified is True
    assert len(report.regions) == 2


def test_cloud_integration_verifier():
    verifier = CloudIntegrationVerifier()
    report = verifier.verify()
    assert isinstance(report, CloudObservabilityIntegrationReport)
    assert report.status == "PASS"
    assert report.unified_reliability_view_verified is True
    assert report.cross_cloud_portability_score_pct == 100.0
    assert len(report.integrations) == 4


def test_dashboard_federation_verifier():
    verifier = DashboardFederationVerifier()
    report = verifier.verify()
    assert isinstance(report, DashboardFederationReport)
    assert report.status == "PASS"
    assert report.federated_views_count == 4
    assert report.multi_tier_coverage_pct == 100.0
    assert len(report.dashboard_tiers) == 4


def test_automation_control_verifier():
    verifier = AutomationControlVerifier()
    report = verifier.verify()
    assert isinstance(report, GlobalAutomationControlReport)
    assert report.status == "PASS"
    assert report.action_authorization_verified is True
    assert report.automated_rollback_verified is True
    assert report.audit_logging_verified is True
    assert len(report.actions) == 3


# ─── 2. Scorer Unit Tests ─────────────────────────────────────────────────────

def test_global_operations_scorer():
    runtime = EnterpriseObservabilityRuntime()
    verification_results = runtime.execute_all_verifications()
    scorer = GlobalOperationsScorer()
    cert = scorer.compute_certification(verification_results)

    assert isinstance(cert, GlobalOperationsCertificationReport)
    assert cert.composite_global_score_pct >= 95.0
    assert cert.certification_tier == GlobalCertificationTier.ENTERPRISE_GLOBAL_OPERATIONS_READY
    assert cert.certification_granted is True
    assert len(cert.category_scores) == 7

    # Verify category weights sum to 100%
    total_weight = sum(c.weight_pct for c in cert.category_scores)
    assert total_weight == 100.0


# ─── 3. Exporter Unit Tests ───────────────────────────────────────────────────

def test_enterprise_observability_exporter(tmp_path):
    output_dir = tmp_path / "enterprise_obs_test"
    runtime = EnterpriseObservabilityRuntime(output_dir=str(output_dir))
    pipeline_result = runtime.run_pipeline()

    exported_files = pipeline_result["exported_files"]
    assert len(exported_files) == 13  # 11 reports + certification_report.json + metadata.json

    metadata_path = output_dir / "metadata.json"
    assert metadata_path.exists()
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["composite_global_score_pct"] >= 95.0
    assert metadata["certification_tier"] == GlobalCertificationTier.ENTERPRISE_GLOBAL_OPERATIONS_READY.value
    assert len(metadata["manifest"]) == 12


# ─── 4. REST API Integration Tests ────────────────────────────────────────────

def test_api_status_endpoint(api_client):
    response = api_client.get("/api/v1/enterprise-observability/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ONLINE"
    assert data["connected_environments"] == 5


def test_api_environments_endpoint(api_client):
    response = api_client.get("/api/v1/enterprise-observability/environments")
    assert response.status_code == 200
    data = response.json()
    assert len(data["environments_federated"]) == 5


def test_api_drift_endpoint(api_client):
    response = api_client.get("/api/v1/enterprise-observability/drift")
    assert response.status_code == 200
    data = response.json()
    assert data["zero_unauthorized_drift_verified"] is True


def test_api_readiness_gates_endpoint(api_client):
    response = api_client.get("/api/v1/enterprise-observability/readiness-gates")
    assert response.status_code == 200
    data = response.json()
    assert data["release_approval_granted"] is True
    assert data["overall_health_score"] >= 90.0


def test_api_multi_region_endpoint(api_client):
    response = api_client.get("/api/v1/enterprise-observability/multi-region")
    assert response.status_code == 200
    data = response.json()
    assert data["automated_failover_verified"] is True
    assert len(data["regions"]) == 2


def test_api_certification_endpoint(api_client):
    response = api_client.get("/api/v1/enterprise-observability/certification")
    assert response.status_code == 200
    data = response.json()
    assert data["composite_global_score_pct"] >= 95.0
    assert data["certification_tier"] == GlobalCertificationTier.ENTERPRISE_GLOBAL_OPERATIONS_READY.value


def test_api_run_verification_endpoint(api_client):
    response = api_client.post("/api/v1/enterprise-observability/run-verification")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["certification_granted"] is True
    assert data["composite_global_score_pct"] >= 95.0
    assert data["exported_files_count"] == 13
