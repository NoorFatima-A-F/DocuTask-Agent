"""
Test Suite: Phase 3I.10 Observability Intelligence Governance, Reliability Automation Maturity & Enterprise Operations Certification
"""
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.observability_operations_governance.domain.models import (
    OperationsCertificationTier,
    MaturityLevel,
    GovernanceArchitectureReport,
    ObservabilityPolicyReport,
    ReliabilityMaturityReport,
    SREManagementReport,
    RunbookAutomationReport,
    AutomationSafetyGovernanceReport,
    ChangeManagementReport,
    IncidentGovernanceReport,
    ContinuousImprovementReport,
    OperationsDashboardReport,
    EnterpriseOperationsCertificationReport,
)

from app.platform_verification.observability_operations_governance.verifiers import (
    GovernanceArchitectureVerifier,
    PolicyManagementVerifier,
    ReliabilityMaturityVerifier,
    SREManagementVerifier,
    RunbookAutomationVerifier,
    AutomationSafetyVerifier,
    ChangeManagementVerifier,
    IncidentGovernanceVerifier,
    ContinuousImprovementVerifier,
    OperationsDashboardVerifier,
)
from app.platform_verification.observability_operations_governance.scoring import (
    OperationsCertificationScorer,
)
from app.platform_verification.observability_operations_governance.runtime import (
    ObservabilityOperationsRuntime,
)
from app.platform_verification.observability_operations_governance.api import router


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


# ─── 1. Verifier Unit Tests ───────────────────────────────────────────────────

def test_governance_architecture_verifier():
    verifier = GovernanceArchitectureVerifier()
    report = verifier.verify()
    assert isinstance(report, GovernanceArchitectureReport)
    assert report.status == "PASS"
    assert report.policy_engine_active is True
    assert report.decision_audit_system_active is True
    assert report.reliability_review_system_active is True
    assert report.compliance_score_pct == 100.0
    assert len(report.components) == 5


def test_policy_management_verifier():
    verifier = PolicyManagementVerifier()
    report = verifier.verify()
    assert isinstance(report, ObservabilityPolicyReport)
    assert report.status == "PASS"
    assert report.alert_policies_count >= 3
    assert report.automation_permissions_count >= 3
    assert report.escalation_policies_count >= 2
    assert report.policy_coverage_pct == 100.0
    assert len(report.policies) == 8


def test_maturity_model_verifier():
    verifier = ReliabilityMaturityVerifier()
    report = verifier.verify()
    assert isinstance(report, ReliabilityMaturityReport)
    assert report.status == "PASS"
    assert report.overall_maturity_level == MaturityLevel.LEVEL_5_AUTONOMOUS
    assert report.maturity_score_pct == 100.0
    assert report.autonomous_readiness is True
    assert len(report.dimensions) == 5


def test_sre_management_verifier():
    verifier = SREManagementVerifier()
    report = verifier.verify()
    assert isinstance(report, SREManagementReport)
    assert report.status == "PASS"
    assert report.avg_availability_pct >= 99.9
    assert report.budget_exhaustion_risk == "LOW"
    assert report.error_budget_policy_enforced is True
    assert len(report.slos) == 5


def test_runbook_automation_verifier():
    verifier = RunbookAutomationVerifier()
    report = verifier.verify()
    assert isinstance(report, RunbookAutomationReport)
    assert report.status == "PASS"
    assert report.automated_runbooks_count == 4
    assert report.success_rate_pct == 100.0
    assert len(report.runbooks) == 4


def test_automation_safety_verifier():
    verifier = AutomationSafetyVerifier()
    report = verifier.verify()
    assert isinstance(report, AutomationSafetyGovernanceReport)
    assert report.status == "PASS"
    assert report.human_approval_gate_enforced is True
    assert report.automated_rollback_verified is True
    assert report.safety_compliance_pct == 100.0
    assert len(report.safety_rules) == 5


def test_change_management_verifier():
    verifier = ChangeManagementVerifier()
    report = verifier.verify()
    assert isinstance(report, ChangeManagementReport)
    assert report.status == "PASS"
    assert report.pre_deployment_validation is True
    assert report.canary_gating_verified is True
    assert report.post_deployment_slo_validation is True
    assert report.change_safety_score_pct == 100.0
    assert len(report.pipeline_stages) == 4


def test_incident_governance_verifier():
    verifier = IncidentGovernanceVerifier()
    report = verifier.verify()
    assert isinstance(report, IncidentGovernanceReport)
    assert report.status == "PASS"
    assert report.mttd_seconds < 15.0
    assert report.mttr_seconds < 120.0
    assert report.automated_postmortem_coverage_pct == 100.0
    assert len(report.incidents_analyzed) == 3


def test_continuous_improvement_verifier():
    verifier = ContinuousImprovementVerifier()
    report = verifier.verify()
    assert isinstance(report, ContinuousImprovementReport)
    assert report.status == "PASS"
    assert report.zero_recurrence_rate_pct == 100.0
    assert report.preventative_tasks_completed_pct == 100.0
    assert report.improvement_score_pct == 100.0
    assert len(report.action_items) == 3


def test_operations_dashboard_verifier():
    verifier = OperationsDashboardVerifier()
    report = verifier.verify()
    assert isinstance(report, OperationsDashboardReport)
    assert report.status == "PASS"
    assert report.views_count == 3
    assert report.multi_tier_coverage_pct == 100.0
    assert len(report.views) == 3


# ─── 2. Scorer Unit Tests ─────────────────────────────────────────────────────

def test_operations_certification_scorer():
    runtime = ObservabilityOperationsRuntime()
    verification_results = runtime.execute_all_verifications()
    scorer = OperationsCertificationScorer()
    cert = scorer.compute_certification(verification_results)

    assert isinstance(cert, EnterpriseOperationsCertificationReport)
    assert cert.composite_operations_score_pct >= 95.0
    assert cert.certification_tier == OperationsCertificationTier.ENTERPRISE_AUTONOMOUS_CERTIFIED
    assert cert.autonomous_operations_certified is True
    assert len(cert.pillar_scores) == 6

    # Verify pillar weights sum to 100%
    total_weight = sum(p.weight_pct for p in cert.pillar_scores)
    assert total_weight == 100.0


# ─── 3. Exporter Unit Tests ───────────────────────────────────────────────────

def test_observability_governance_exporter(tmp_path):
    output_dir = tmp_path / "obs_gov_test"
    runtime = ObservabilityOperationsRuntime(output_dir=str(output_dir))
    pipeline_result = runtime.run_pipeline()

    exported_files = pipeline_result["exported_files"]
    assert len(exported_files) == 12  # 10 verifier reports + certification_report.json + metadata.json

    metadata_path = output_dir / "metadata.json"
    assert metadata_path.exists()
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["composite_operations_score_pct"] >= 95.0
    assert metadata["certification_tier"] == OperationsCertificationTier.ENTERPRISE_AUTONOMOUS_CERTIFIED.value
    assert len(metadata["manifest"]) == 11


# ─── 4. REST API Integration Tests ────────────────────────────────────────────

def test_api_status_endpoint(api_client):
    response = api_client.get("/api/v1/observability-governance/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ONLINE"
    assert data["target_level"] == "Level 5: Autonomous"


def test_api_maturity_endpoint(api_client):
    response = api_client.get("/api/v1/observability-governance/maturity")
    assert response.status_code == 200
    data = response.json()
    assert data["overall_maturity_level"] == MaturityLevel.LEVEL_5_AUTONOMOUS.value
    assert data["maturity_score_pct"] == 100.0


def test_api_runbooks_endpoint(api_client):
    response = api_client.get("/api/v1/observability-governance/runbooks")
    assert response.status_code == 200
    data = response.json()
    assert data["automated_runbooks_count"] == 4
    assert len(data["runbooks"]) == 4


def test_api_policies_endpoint(api_client):
    response = api_client.get("/api/v1/observability-governance/policies")
    assert response.status_code == 200
    data = response.json()
    assert data["policy_coverage_pct"] == 100.0


def test_api_certification_endpoint(api_client):
    response = api_client.get("/api/v1/observability-governance/certification")
    assert response.status_code == 200
    data = response.json()
    assert data["composite_operations_score_pct"] >= 95.0
    assert data["certification_tier"] == OperationsCertificationTier.ENTERPRISE_AUTONOMOUS_CERTIFIED.value


def test_api_run_verification_endpoint(api_client):
    response = api_client.post("/api/v1/observability-governance/run-verification")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["autonomous_operations_certified"] is True
    assert data["composite_operations_score_pct"] >= 95.0
    assert data["exported_files_count"] == 12
