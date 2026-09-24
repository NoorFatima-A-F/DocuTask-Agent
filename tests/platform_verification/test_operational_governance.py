"""
Phase 3H.8: Comprehensive Test Suite for Enterprise Operational Governance & Safe Operations Verification
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.operational_governance.domain.models import (
    RiskLevel,
    DeploymentStrategyType,
    GovernanceCertificationTier,
)
from app.platform_verification.operational_governance.verifiers import (
    ChangeGovernanceVerifier,
    ConfigurationChangeVerifier,
    DeploymentSafetyVerifier,
    DatabaseChangeVerifier,
    AIModelChangeVerifier,
    ApprovalWorkflowVerifier,
    RollbackVerificationVerifier,
    AuditTrailVerifier,
    ContinuousVerificationVerifier,
    GovernanceDashboardVerifier,
)
from app.platform_verification.operational_governance.scoring import OperationalGovernanceScorer
from app.platform_verification.operational_governance.runtime import OperationalGovernanceRuntime
from app.platform_verification.operational_governance.api import router


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_change_governance_verification():
    verifier = ChangeGovernanceVerifier()
    report = verifier.verify_change_governance()

    assert report.total_changes_evaluated == 4
    assert report.lifecycle_governance_enforced is True

    risk_levels = [c.risk_level for c in report.changes]
    assert RiskLevel.LOW in risk_levels
    assert RiskLevel.MODERATE in risk_levels
    assert RiskLevel.HIGH in risk_levels
    assert RiskLevel.EMERGENCY in risk_levels

    for change in report.changes:
        assert change.change_id.startswith("CHG-")
        assert len(change.rollback_strategy) > 0
        assert len(change.verification_plan) > 0
        assert change.is_compliant is True


def test_configuration_change_verification():
    verifier = ConfigurationChangeVerifier()
    report = verifier.verify_configuration_changes()

    assert report.total_configs_audited == 5
    assert report.immutable_configuration_enforced is True
    assert report.zero_unvalidated_overrides is True

    for config in report.configurations:
        assert config.schema_validated is True
        assert config.secret_separated is True
        assert config.immutable_version_recorded is True
        assert config.drift_detected is False


def test_deployment_safety_verification():
    verifier = DeploymentSafetyVerifier()
    report = verifier.verify_deployment_safety()

    assert report.total_deployments_audited == 4
    assert report.progressive_delivery_enforced is True

    strategies = [d.strategy for d in report.deployments]
    assert DeploymentStrategyType.CANARY in strategies
    assert DeploymentStrategyType.BLUE_GREEN in strategies
    assert DeploymentStrategyType.ROLLING in strategies
    assert DeploymentStrategyType.FEATURE_FLAG in strategies

    for dep in report.deployments:
        assert dep.health_validation_gates_passed is True
        assert dep.automatic_promotion_enabled is True
        assert dep.rollback_trigger_configured is True


def test_database_change_governance():
    verifier = DatabaseChangeVerifier()
    report = verifier.verify_database_changes()

    assert report.total_migrations_audited == 4
    assert report.schema_evolution_safe is True

    for mig in report.migrations:
        assert mig.is_backward_compatible is True
        assert mig.is_forward_compatible is True
        assert mig.zero_downtime_verified is True
        assert mig.rollback_script_verified is True
        assert mig.transaction_integrity_guaranteed is True


def test_ai_model_change_verification():
    verifier = AIModelChangeVerifier()
    report = verifier.verify_ai_model_changes()

    assert report.total_ai_changes_audited == 3
    assert report.zero_regression_verified is True

    for bm in report.benchmarks:
        assert bm.schema_compatibility_pct == 100.0
        assert bm.extraction_accuracy_pct >= 99.0
        assert bm.regression_tests_passed is True
        assert bm.instant_rollback_capable is True


def test_approval_workflow_verification():
    verifier = ApprovalWorkflowVerifier()
    report = verifier.verify_approval_workflows()

    assert report.total_workflows_evaluated == 4
    assert report.policy_compliance_pct == 100.0

    for wf in report.workflows:
        assert wf.status == "APPROVED"
        assert len(wf.approvals_obtained) >= 1
        if wf.risk_level == RiskLevel.EMERGENCY:
            assert wf.post_incident_review_required is True


def test_automated_rollback_verification():
    verifier = RollbackVerificationVerifier()
    report = verifier.verify_automated_rollbacks()

    assert report.total_triggers_evaluated == 5
    assert report.automated_rollback_operational is True

    trigger_types = [t.trigger_type for t in report.triggers]
    assert "SLO_VIOLATION" in trigger_types
    assert "ERROR_RATE_SPIKE" in trigger_types
    assert "HEALTH_FAILURE" in trigger_types
    assert "AI_PROMPT_DRIFT" in trigger_types

    for trig in report.triggers:
        assert trig.state_restoration_verified is True
        assert trig.data_loss_prevented is True
        assert trig.rollback_latency_seconds < 5.0


def test_audit_trail_verification():
    verifier = AuditTrailVerifier()
    report = verifier.verify_audit_trails()

    assert report.total_audit_records == 5
    assert report.tamper_evident_integrity_verified is True

    for rec in report.records:
        assert rec.outcome == "SUCCESS"
        assert rec.evidence_reference_sha256.startswith("sha256:")
        assert len(rec.affected_resources) > 0


def test_continuous_verification():
    verifier = ContinuousVerificationVerifier()
    report = verifier.verify_continuous_operations()

    assert report.checks_total == 5
    assert report.checks_passed == 5
    assert report.production_stability_confirmed is True

    for chk in report.checks:
        assert chk.passed is True
        assert chk.audit_signoff is True


def test_governance_dashboard_generation():
    verifier = GovernanceDashboardVerifier()
    report = verifier.generate_governance_dashboard()

    assert report.active_deployments_count == 0
    assert report.deployment_success_rate_pct == 100.0
    assert report.operational_risk_index <= 0.05
    assert len(report.metrics) == 6


def test_operational_governance_scorer():
    change = ChangeGovernanceVerifier().verify_change_governance()
    config = ConfigurationChangeVerifier().verify_configuration_changes()
    deploy = DeploymentSafetyVerifier().verify_deployment_safety()
    db = DatabaseChangeVerifier().verify_database_changes()
    ai = AIModelChangeVerifier().verify_ai_model_changes()
    approval = ApprovalWorkflowVerifier().verify_approval_workflows()
    rollback = RollbackVerificationVerifier().verify_automated_rollbacks()
    audit = AuditTrailVerifier().verify_audit_trails()
    continuous = ContinuousVerificationVerifier().verify_continuous_operations()
    dashboard = GovernanceDashboardVerifier().generate_governance_dashboard()

    scorer = OperationalGovernanceScorer()
    scorecard = scorer.calculate_scorecard(
        change_report=change,
        config_report=config,
        deploy_report=deploy,
        db_report=db,
        ai_report=ai,
        approval_report=approval,
        rollback_report=rollback,
        audit_report=audit,
        continuous_report=continuous,
        dashboard_report=dashboard,
    )

    assert scorecard.overall_governance_score >= 98.0
    assert scorecard.certification_tier == GovernanceCertificationTier.ENTERPRISE_OPERATIONAL_GOVERNANCE_CERTIFIED
    assert scorecard.passed is True
    assert len(scorecard.pillar_scores) == 8
    assert scorecard.change_auditability_guaranteed is True
    assert scorecard.rollback_readiness_guaranteed is True


def test_evidence_exporter_and_signatures(tmp_path):
    runtime = OperationalGovernanceRuntime(output_dir=tmp_path)
    result = runtime.run_full_verification(export_evidence=True)
    meta = result["export_metadata"]

    assert meta is not None
    assert meta["total_reports_exported"] == 11
    assert meta["overall_governance_score"] >= 98.0
    assert meta["status"] == "PASSED"

    expected_files = [
        "change_governance_report.json",
        "configuration_change_report.json",
        "deployment_safety_report.json",
        "database_change_report.json",
        "ai_model_change_report.json",
        "approval_workflow_report.json",
        "rollback_verification_report.json",
        "audit_trail_report.json",
        "continuous_verification_report.json",
        "governance_dashboard_report.json",
        "operational_governance_certification_report.json",
        "metadata.json",
    ]

    for f in expected_files:
        p = tmp_path / f
        assert p.exists()
        assert p.stat().st_size > 0


def test_fastapi_endpoints(api_client):
    # GET /health
    resp = api_client.get("/api/v1/platform-verification/operational-governance/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "HEALTHY"

    # GET /changes
    resp = api_client.get("/api/v1/platform-verification/operational-governance/changes")
    assert resp.status_code == 200
    assert resp.json()["total_changes_evaluated"] == 4

    # GET /deployments
    resp = api_client.get("/api/v1/platform-verification/operational-governance/deployments")
    assert resp.status_code == 200
    assert resp.json()["total_deployments_audited"] == 4

    # GET /audit-trail
    resp = api_client.get("/api/v1/platform-verification/operational-governance/audit-trail")
    assert resp.status_code == 200
    assert resp.json()["total_audit_records"] == 5

    # GET /dashboard
    resp = api_client.get("/api/v1/platform-verification/operational-governance/dashboard")
    assert resp.status_code == 200
    assert resp.json()["deployment_success_rate_pct"] == 100.0

    # GET /scorecard
    resp = api_client.get("/api/v1/platform-verification/operational-governance/scorecard")
    assert resp.status_code == 200
    assert resp.json()["scorecard"]["overall_governance_score"] >= 98.0

    # POST /verify
    resp = api_client.post("/api/v1/platform-verification/operational-governance/verify?export_evidence=false")
    assert resp.status_code == 200
    assert resp.json()["status"] == "SUCCESS"
    assert resp.json()["summary"]["overall_score"] >= 98.0
