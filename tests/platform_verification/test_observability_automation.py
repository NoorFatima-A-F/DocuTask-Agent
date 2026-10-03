"""
Test Suite: Phase 3I.8 Observability Automation, Self-Healing Operations & Autonomous Reliability
"""
import os
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.observability_automation.domain.models import (
    AutonomousCertificationTier,
    AutomationActionType,
    AutonomousArchitectureReport,
    AnomalyDetectionReport,
    EventCorrelationReport,
    RootCauseAnalysisReport,
    RemediationExecutionReport,
    AutomationSafetyReport,
    SelfHealingValidationReport,
    IncidentAutomationReport,
    ReliabilityLearningReport,
    AutonomousTestingReport,
    HumanControlPolicyReport,
    AutonomousDashboardReport,
    AutonomousCertificationReport,
)

from app.platform_verification.observability_automation.verifiers.architecture_verifier import (
    ArchitectureVerifier,
)
from app.platform_verification.observability_automation.verifiers.anomaly_detection_verifier import (
    AnomalyDetectionVerifier,
)
from app.platform_verification.observability_automation.verifiers.event_correlation_verifier import (
    EventCorrelationVerifier,
)
from app.platform_verification.observability_automation.verifiers.root_cause_verifier import (
    RootCauseVerifier,
)
from app.platform_verification.observability_automation.verifiers.remediation_verifier import (
    RemediationVerifier,
)
from app.platform_verification.observability_automation.verifiers.safety_control_verifier import (
    SafetyControlVerifier,
)
from app.platform_verification.observability_automation.verifiers.self_healing_verifier import (
    SelfHealingVerifier,
)
from app.platform_verification.observability_automation.verifiers.incident_automation_verifier import (
    IncidentAutomationVerifier,
)
from app.platform_verification.observability_automation.verifiers.reliability_learning_verifier import (
    ReliabilityLearningVerifier,
)
from app.platform_verification.observability_automation.verifiers.autonomous_testing_verifier import (
    AutonomousTestingVerifier,
)
from app.platform_verification.observability_automation.verifiers.human_control_verifier import (
    HumanControlVerifier,
)
from app.platform_verification.observability_automation.verifiers.autonomous_dashboard_verifier import (
    AutonomousDashboardVerifier,
)
from app.platform_verification.observability_automation.runtime.observability_automation_runtime import (
    ObservabilityAutomationRuntime,
)
from app.platform_verification.observability_automation.api.observability_automation_api import (
    router as automation_router,
)


# ─── 1. Individual Verifier Tests ─────────────────────────────────────────────

def test_architecture_verifier():
    verifier = ArchitectureVerifier()
    report = verifier.verify_architecture()

    assert isinstance(report, AutonomousArchitectureReport)
    assert report.components_count == 8
    assert len(report.components) == 8
    assert report.automation_level == "advanced"
    assert report.human_approval_required is True
    assert report.status == "PASS"


def test_anomaly_detection_verifier():
    verifier = AnomalyDetectionVerifier()
    report = verifier.verify_anomaly_detection()

    assert isinstance(report, AnomalyDetectionReport)
    assert len(report.anomalies) >= 4
    assert report.detection_accuracy_pct >= 95.0
    assert report.status == "PASS"


def test_event_correlation_verifier():
    verifier = EventCorrelationVerifier()
    report = verifier.verify_event_correlation()

    assert isinstance(report, EventCorrelationReport)
    assert len(report.incidents) >= 2
    assert report.correlation_verified is True
    assert "4:1" in report.signal_reduction_ratio


def test_root_cause_verifier():
    verifier = RootCauseVerifier()
    report = verifier.verify_root_cause_analysis()

    assert isinstance(report, RootCauseAnalysisReport)
    assert len(report.hypotheses) >= 2
    assert report.average_confidence >= 0.50
    assert report.status == "PASS"
    assert len(report.primary_root_cause) > 0


def test_remediation_verifier():
    verifier = RemediationVerifier()
    report = verifier.verify_automated_remediation()

    assert isinstance(report, RemediationExecutionReport)
    assert len(report.actions) >= 4
    assert report.all_actions_verified is True
    assert report.automation_success_rate_pct == 100.0

    action_types = {a.action_type for a in report.actions}
    assert AutomationActionType.SERVICE_RESTART in action_types
    assert AutomationActionType.QUEUE_RECOVERY in action_types
    assert AutomationActionType.RESOURCE_SCALING in action_types
    assert AutomationActionType.DEPLOYMENT_ROLLBACK in action_types


def test_safety_control_verifier():
    verifier = SafetyControlVerifier()
    report = verifier.verify_safety_controls()

    assert isinstance(report, AutomationSafetyReport)
    assert len(report.rules) >= 5
    assert report.guardrails_enforced is True
    assert report.zero_unauthorized_high_risk_actions is True


def test_self_healing_verifier():
    verifier = SelfHealingVerifier()
    report = verifier.verify_self_healing_workflows()

    assert isinstance(report, SelfHealingValidationReport)
    assert len(report.loops) >= 3
    assert report.all_healing_loops_verified is True
    assert report.average_mttr_seconds <= 30.0


def test_incident_automation_verifier():
    verifier = IncidentAutomationVerifier()
    report = verifier.verify_incident_automation()

    assert isinstance(report, IncidentAutomationReport)
    assert len(report.incidents) >= 2
    assert report.lifecycle_automated is True
    assert report.postmortem_automation_verified is True


def test_reliability_learning_verifier():
    verifier = ReliabilityLearningVerifier()
    report = verifier.verify_reliability_learning()

    assert isinstance(report, ReliabilityLearningReport)
    assert len(report.lessons) >= 3
    assert report.knowledge_base_active is True
    assert report.recurrence_prevention_score_pct == 100.0


def test_autonomous_testing_verifier():
    verifier = AutonomousTestingVerifier()
    report = verifier.verify_autonomous_testing()

    assert isinstance(report, AutonomousTestingReport)
    assert len(report.simulations) >= 4
    assert report.all_simulations_passed is True


def test_human_control_verifier():
    verifier = HumanControlVerifier()
    report = verifier.verify_human_control_policies()

    assert isinstance(report, HumanControlPolicyReport)
    assert len(report.policies) == 3
    assert report.human_oversight_enforced is True


def test_autonomous_dashboard_verifier():
    verifier = AutonomousDashboardVerifier()
    report = verifier.verify_autonomous_dashboards()

    assert isinstance(report, AutonomousDashboardReport)
    assert len(report.dashboard_views) == 3
    assert report.dashboards_active is True


# ─── 2. Scorer Tests ──────────────────────────────────────────────────────────

def test_autonomous_reliability_scorer():
    runtime = ObservabilityAutomationRuntime()
    scorer = runtime.scorer

    cert = scorer.calculate_certification_score(
        arch_report=runtime.arch_verifier.verify_architecture(),
        anomaly_report=runtime.anomaly_verifier.verify_anomaly_detection(),
        corr_report=runtime.corr_verifier.verify_event_correlation(),
        rca_report=runtime.rca_verifier.verify_root_cause_analysis(),
        remediation_report=runtime.remediation_verifier.verify_automated_remediation(),
        safety_report=runtime.safety_verifier.verify_safety_controls(),
        healing_report=runtime.healing_verifier.verify_self_healing_workflows(),
        incident_report=runtime.incident_verifier.verify_incident_automation(),
        learning_report=runtime.learning_verifier.verify_reliability_learning(),
        testing_report=runtime.testing_verifier.verify_autonomous_testing(),
        human_report=runtime.human_verifier.verify_human_control_policies(),
        dash_report=runtime.dash_verifier.verify_autonomous_dashboards(),
    )

    assert isinstance(cert, AutonomousCertificationReport)
    assert len(cert.pillar_scores) == 6
    assert cert.overall_score_pct >= 95.0
    assert cert.certification_granted is True
    assert cert.certification_tier == AutonomousCertificationTier.AUTONOMOUS_OPERATIONS_READY

    total_weight = sum(p.weight_pct for p in cert.pillar_scores)
    assert total_weight == 100.0


# ─── 3. Exporter & Artifact Verification ──────────────────────────────────────

def test_observability_automation_evidence_exporter(tmp_path):
    output_dir = str(tmp_path / "automation_test_export")
    runtime = ObservabilityAutomationRuntime(output_dir=output_dir)
    results = runtime.run_full_verification()

    assert results["status"] == "SUCCESS"
    assert os.path.exists(output_dir)

    expected_files = [
        "architecture_report.json",
        "anomaly_report.json",
        "correlation_report.json",
        "root_cause_report.json",
        "remediation_report.json",
        "safety_report.json",
        "self_healing_report.json",
        "incident_report.json",
        "learning_report.json",
        "testing_report.json",
        "human_control_policy_report.json",
        "autonomous_dashboard_report.json",
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
    app.include_router(automation_router)
    return TestClient(app)


def test_api_run_verification(api_client):
    response = api_client.post("/api/v1/observability-automation/run-verification")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["certification_granted"] is True
    assert data["overall_score_pct"] >= 95.0


def test_api_status(api_client):
    response = api_client.get("/api/v1/observability-automation/status")
    assert response.status_code == 200
    data = response.json()
    assert data["certification_granted"] is True
    assert data["overall_score_pct"] >= 95.0
    assert len(data["pillar_scores"]) == 6


def test_api_remediations(api_client):
    response = api_client.get("/api/v1/observability-automation/remediations")
    assert response.status_code == 200
    data = response.json()
    assert "remediations" in data
    assert "safety_guardrails" in data
    assert "self_healing_loops" in data


def test_api_root_cause_analysis(api_client):
    response = api_client.get("/api/v1/observability-automation/root-cause-analysis")
    assert response.status_code == 200
    data = response.json()
    assert "root_cause_analysis" in data
    assert "event_correlation" in data
    assert "reliability_learning" in data
