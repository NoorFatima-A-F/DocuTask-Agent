"""
Unit and integration tests for Part 4 - Enterprise Platform Core Services Verification.
"""

import os
import json
import pytest
from app.platform_core_verification import (
    OrchestratorVerifier,
    AgentKernelVerifier,
    WorkflowEngineVerifier,
    SchedulerVerifier,
    QueueVerifier,
    StorageVerifier,
    ApiGatewayVerifier,
    EventBusVerifier,
    ConfigSecretsVerifier,
    CachingVerifier,
    IdentityVerifier,
    ObservabilityVerifier,
    ResilienceVerifier,
    CrossServiceVerifier,
    CoreServicesScorer,
    EvidenceGenerator,
    VerificationStatus,
    SectionId,
)


def test_section_a_orchestrator():
    v = OrchestratorVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_A_ORCHESTRATOR
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_section_b_agent_kernel():
    v = AgentKernelVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_B_AGENT_KERNEL
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_c_workflow_engine():
    v = WorkflowEngineVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_C_WORKFLOW_ENGINE
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_d_scheduler():
    v = SchedulerVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_D_SCHEDULER
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_e_queues():
    v = QueueVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_E_QUEUES
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_f_storage():
    v = StorageVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_F_STORAGE
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_g_api_gateway():
    v = ApiGatewayVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_G_API_GATEWAY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_h_event_bus():
    v = EventBusVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_H_EVENT_BUS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_i_config_secrets():
    v = ConfigSecretsVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_I_CONFIG_SECRETS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_j_caching():
    v = CachingVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_J_CACHING
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_k_identity_auth():
    v = IdentityVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_K_IDENTITY_AUTH
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_l_observability():
    v = ObservabilityVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_L_OBSERVABILITY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_m_resilience():
    v = ResilienceVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_M_RESILIENCE
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_n_cross_service():
    v = CrossServiceVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_N_CROSS_SERVICE
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_core_services_scorer_and_scorecard():
    verifiers = [
        OrchestratorVerifier(),
        AgentKernelVerifier(),
        WorkflowEngineVerifier(),
        SchedulerVerifier(),
        QueueVerifier(),
        StorageVerifier(),
        ApiGatewayVerifier(),
        EventBusVerifier(),
        ConfigSecretsVerifier(),
        CachingVerifier(),
        IdentityVerifier(),
        ObservabilityVerifier(),
        ResilienceVerifier(),
        CrossServiceVerifier(),
    ]
    results = {v.verify_all().section_id.value: v.verify_all() for v in verifiers}
    
    scorer = CoreServicesScorer()
    scorecard = scorer.calculate_scorecard(results)

    assert scorecard.composite_score == 100.0
    assert scorecard.grade == "A+"
    assert scorecard.total_assertions == 56
    assert scorecard.passed_assertions == 56
    assert len(scorecard.sections) == 14


def test_evidence_export_and_manifest(tmp_path):
    output_dir = str(tmp_path / "evidence")
    docs_dir = str(tmp_path / "docs")

    verifiers = [OrchestratorVerifier(), AgentKernelVerifier(), StorageVerifier()]
    results = {v.verify_all().section_id.value: v.verify_all() for v in verifiers}
    
    scorer = CoreServicesScorer()
    scorecard = scorer.calculate_scorecard(results)

    exporter = EvidenceGenerator(output_dir=output_dir, docs_dir=docs_dir)
    summary = exporter.export_all(scorecard)

    assert os.path.exists(summary["manifest_path"])
    assert os.path.exists(summary["report_path"])
    
    with open(summary["manifest_path"], "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest["composite_score"] == 100.0
    assert len(manifest["files"]) > 0
