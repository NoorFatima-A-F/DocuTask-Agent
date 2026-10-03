"""Unit and Integration Tests for Phase 5: Enterprise Autonomous Workflow Validation Framework."""

import json
import os
import shutil
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.enterprise_autonomous_workflow_validation.domain.models import (
    CertificationTier,
    VerificationStatus,
)
from app.platform_verification.enterprise_autonomous_workflow_validation.verifiers import (
    AuditTrailValidationVerifier,
    AutonomousRecoveryVerifier,
    BusinessKPIVerifier,
    BusinessRuleEnforcementVerifier,
    BusinessValueVerifier,
    CompleteWorkflowExecutionVerifier,
    ComplianceValidationVerifier,
    CostValidationVerifier,
    DecisionQualityVerifier,
    EnterpriseDatasetVerifier,
    ExceptionWorkflowVerifier,
    ExecutiveReadinessVerifier,
    ExplainabilityValidationVerifier,
    HumanInTheLoopVerifier,
    LongRunningWorkflowVerifier,
    MultiAgentBusinessCollaborationVerifier,
    OrganizationalWorkflowVerifier,
    ScenarioLibraryVerifier,
    WorkflowOptimizationVerifier,
    WorkflowScalabilityVerifier,
)
from app.platform_verification.enterprise_autonomous_workflow_validation.scoring.workflow_quality_scorer import (
    AutonomousWorkflowQualityScorer,
)
from app.platform_verification.enterprise_autonomous_workflow_validation.runtime.workflow_verification_runtime import (
    AutonomousWorkflowVerificationRuntime,
)
from app.platform_verification.enterprise_autonomous_workflow_validation.api.workflow_verification_api import router


@pytest.fixture
def tmp_output_dir(tmp_path):
    output_dir = str(tmp_path / "test_workflow_evidence")
    yield output_dir
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


# --- 1. Verifier Unit Tests (Parts A to T) ---

def test_part_a_scenario_library():
    verifier = ScenarioLibraryVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5A-SCENARIO-LIBRARY"
    assert report.status == VerificationStatus.PASSED
    assert report.score == 100.0
    assert report.total_domains == 10
    assert len(report.scenarios) == 10
    assert len(report.checks) == 4


def test_part_b_complete_execution():
    verifier = CompleteWorkflowExecutionVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5B-COMPLETE-EXECUTION"
    assert report.status == VerificationStatus.PASSED
    assert report.total_stages == 18
    assert report.all_stages_passed is True
    assert report.e2e_duration_ms < 1000.0


def test_part_c_human_in_the_loop():
    verifier = HumanInTheLoopVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5C-HITL-VALIDATION"
    assert report.status == VerificationStatus.PASSED
    assert report.timeout_handling_verified is True
    assert len(report.interactions) == 5


def test_part_d_multi_agent_collaboration():
    verifier = MultiAgentBusinessCollaborationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5D-MULTI-AGENT-COLLAB"
    assert report.status == VerificationStatus.PASSED
    assert report.total_agents_engaged == 9
    assert report.collaboration_efficiency_pct == 100.0


def test_part_e_decision_quality():
    verifier = DecisionQualityVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5E-DECISION-QUALITY"
    assert report.status == VerificationStatus.PASSED
    assert report.confidence_calibration_error < 0.05
    assert report.overall_decision_accuracy_pct >= 99.0


def test_part_f_business_rule_enforcement():
    verifier = BusinessRuleEnforcementVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5F-BUSINESS-RULES"
    assert report.status == VerificationStatus.PASSED
    assert report.enforcement_success_rate_pct == 100.0
    assert len(report.rules) == 5


def test_part_g_exception_workflow():
    verifier = ExceptionWorkflowVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5G-EXCEPTION-WORKFLOW"
    assert report.status == VerificationStatus.PASSED
    assert report.unhandled_crashes_count == 0
    assert len(report.simulations) == 5


def test_part_h_business_kpi():
    verifier = BusinessKPIVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5H-BUSINESS-KPI"
    assert report.status == VerificationStatus.PASSED
    assert report.automation_rate_pct > 90.0
    assert report.speedup_multiplier > 10.0
    assert len(report.kpis) == 5


def test_part_i_autonomous_recovery():
    verifier = AutonomousRecoveryVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5I-AUTONOMOUS-RECOVERY"
    assert report.status == VerificationStatus.PASSED
    assert report.data_loss_detected is False
    assert len(report.events) == 5


def test_part_j_organizational_workflow():
    verifier = OrganizationalWorkflowVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5J-ORGANIZATIONAL-WORKFLOW"
    assert report.status == VerificationStatus.PASSED
    assert report.total_departments_orchestrated == 6
    assert len(report.transitions) == 6


def test_part_k_long_running_workflow():
    verifier = LongRunningWorkflowVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5K-LONG-RUNNING"
    assert report.status == VerificationStatus.PASSED
    assert report.checkpoint_integrity_pct == 100.0
    assert len(report.checkpoints) == 4


def test_part_l_explainability_validation():
    verifier = ExplainabilityValidationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5L-EXPLAINABILITY"
    assert report.status == VerificationStatus.PASSED
    assert report.explainability_coverage_pct == 100.0
    assert len(report.items) == 5


def test_part_m_audit_trail_validation():
    verifier = AuditTrailValidationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5M-AUDIT-TRAIL"
    assert report.status == VerificationStatus.PASSED
    assert report.tamper_detection_verified is True
    assert len(report.audit_entries) == 5


def test_part_n_compliance_validation():
    verifier = ComplianceValidationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5N-COMPLIANCE"
    assert report.status == VerificationStatus.PASSED
    assert report.overall_compliance_rate_pct == 100.0
    assert len(report.frameworks) == 5


def test_part_o_cost_validation():
    verifier = CostValidationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5O-COST-VALIDATION"
    assert report.status == VerificationStatus.PASSED
    assert report.cost_per_document_usd < 0.05
    assert len(report.cost_breakdown) == 5


def test_part_p_workflow_optimization():
    verifier = WorkflowOptimizationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5P-OPTIMIZATION"
    assert report.status == VerificationStatus.PASSED
    assert report.overall_efficiency_gain_pct > 50.0
    assert len(report.metrics) == 5


def test_part_q_business_value():
    verifier = BusinessValueVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5Q-BUSINESS-VALUE"
    assert report.status == VerificationStatus.PASSED
    assert report.total_annual_roi_multiple > 3.0
    assert len(report.values) == 5


def test_part_r_enterprise_dataset():
    verifier = EnterpriseDatasetVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5R-ENTERPRISE-DATASET"
    assert report.status == VerificationStatus.PASSED
    assert report.total_samples_evaluated >= 4000
    assert len(report.datasets) == 6


def test_part_s_workflow_scalability():
    verifier = WorkflowScalabilityVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5S-SCALABILITY"
    assert report.status == VerificationStatus.PASSED
    assert report.max_tested_concurrency == 10000
    assert len(report.tiers) == 4


def test_part_t_executive_readiness():
    verifier = ExecutiveReadinessVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-5T-EXECUTIVE-READINESS"
    assert report.status == VerificationStatus.PASSED
    assert report.unattended_operation_certified is True
    assert len(report.pillars) == 5


# --- 2. Scoring & Certification Tests ---

def test_workflow_quality_scorer():
    runtime = AutonomousWorkflowVerificationRuntime()
    reports = {k: v.verify() for k, v in runtime.verifiers.items()}
    scorer = AutonomousWorkflowQualityScorer()
    score = scorer.calculate_score(reports)

    assert score.overall_score == 100.0
    assert score.certification_tier == CertificationTier.ENTERPRISE_AUTONOMOUS_BUSINESS_READY
    assert score.verification_status == VerificationStatus.PASSED
    assert len(score.categories) == 7

    # Verify pillar weights sum to 1.0
    total_weights = sum(cat.weight for cat in score.categories)
    assert pytest.approx(total_weights, 0.001) == 1.0


# --- 3. Exporter & SHA-256 Manifest Tests ---

def test_workflow_quality_exporter(tmp_output_dir):
    runtime = AutonomousWorkflowVerificationRuntime()
    runtime.execute_all(output_dir=tmp_output_dir)

    assert os.path.exists(tmp_output_dir)
    assert os.path.exists(os.path.join(tmp_output_dir, "manifest.json"))
    assert os.path.exists(os.path.join(tmp_output_dir, "metadata.json"))
    assert os.path.exists(os.path.join(tmp_output_dir, "autonomous_workflow_summary_report.md"))
    assert os.path.exists(os.path.join(tmp_output_dir, "autonomous_workflow_quality_score.json"))

    with open(os.path.join(tmp_output_dir, "manifest.json"), "r") as f:
        manifest = json.load(f)
    assert len(manifest) >= 22
    for fname, meta in manifest.items():
        assert "sha256" in meta
        assert len(meta["sha256"]) == 64
        assert meta["size_bytes"] > 0


# --- 4. Master Synchronous Runtime Tests ---

def test_workflow_runtime_execution(tmp_output_dir):
    runtime = AutonomousWorkflowVerificationRuntime()
    report = runtime.execute_all(output_dir=tmp_output_dir)

    assert report.status == VerificationStatus.PASSED
    assert report.score.overall_score == 100.0
    assert len(report.reports) == 20
    assert report.score.certification_tier == CertificationTier.ENTERPRISE_AUTONOMOUS_BUSINESS_READY


# --- 5. FastAPI REST API Endpoint Tests ---

def test_workflow_api_health(api_client):
    res = api_client.get("/api/v1/verification/autonomous-workflows/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert data["verifiers_count"] == 20


def test_workflow_api_run_verification(api_client, tmp_output_dir):
    res = api_client.post(f"/api/v1/verification/autonomous-workflows/run?output_dir={tmp_output_dir}")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "PASSED"
    assert data["score"]["overall_score"] == 100.0
    assert len(data["reports"]) == 20


def test_workflow_api_get_score(api_client):
    res = api_client.get("/api/v1/verification/autonomous-workflows/score")
    assert res.status_code == 200
    data = res.json()
    assert data["overall_score"] == 100.0
    assert data["certification_tier"] == "Enterprise Autonomous Business Ready"


def test_workflow_api_get_report(api_client):
    res = api_client.get("/api/v1/verification/autonomous-workflows/report")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "PASSED"
    assert len(data["reports"]) == 20


def test_workflow_api_get_subsystem_report(api_client):
    res = api_client.get("/api/v1/verification/autonomous-workflows/subsystem/scenario_library")
    assert res.status_code == 200
    data = res.json()
    assert data["verifier_id"] == "VERIFY-5A-SCENARIO-LIBRARY"
    assert data["total_domains"] == 10


def test_workflow_api_get_invalid_subsystem_report(api_client):
    res = api_client.get("/api/v1/verification/autonomous-workflows/subsystem/non_existent_module")
    assert res.status_code == 404
