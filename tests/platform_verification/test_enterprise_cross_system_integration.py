"""Unit and Integration Tests for Phase 4: Enterprise Cross-System Integration Framework."""

import json
import os
import shutil
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.enterprise_cross_system_integration.domain.models import (
    CertificationTier,
    VerificationStatus,
)
from app.platform_verification.enterprise_cross_system_integration.verifiers import (
    AgentCollaborationVerifier,
    APIChainVerifier,
    CognitiveIntegrationVerifier,
    CrossSystemPerformanceVerifier,
    DataIntegrityVerifier,
    DependencyMappingVerifier,
    DeploymentIntegrationVerifier,
    EnterpriseWorkflowsVerifier,
    EventBusVerifier,
    EvidenceGenerationVerifier,
    FailurePropagationVerifier,
    IntegrationRegressionVerifier,
    InterfaceContractVerifier,
    KnowledgeFlowVerifier,
    LifecycleIntegrationVerifier,
    MarketplaceValidationVerifier,
    MemoryInteractionVerifier,
    ObservabilityIntegrationVerifier,
    PlanningPipelineVerifier,
    SchedulerVerifier,
    SecurityBoundaryVerifier,
    StatePropagationVerifier,
)
from app.platform_verification.enterprise_cross_system_integration.scoring.integration_quality_scorer import (
    CrossSystemIntegrationQualityScorer,
)
from app.platform_verification.enterprise_cross_system_integration.exporter.integration_quality_exporter import (
    CrossSystemIntegrationQualityExporter,
)
from app.platform_verification.enterprise_cross_system_integration.runtime.integration_verification_runtime import (
    CrossSystemIntegrationVerificationRuntime,
)
from app.platform_verification.enterprise_cross_system_integration.api.integration_verification_api import router


@pytest.fixture
def tmp_output_dir(tmp_path):
    output_dir = str(tmp_path / "test_cross_system_evidence")
    yield output_dir
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir, ignore_errors=True)


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


# --- 1. Verifier Unit Tests (Parts A to V) ---

def test_part_a_dependency_mapping():
    verifier = DependencyMappingVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4A-DEPENDENCY-MAPPING"
    assert report.status == VerificationStatus.PASSED
    assert report.score == 100.0
    assert report.is_dag_valid is True
    assert report.circular_dependencies_detected == 0
    assert len(report.nodes) > 0
    assert len(report.checks) == 4


def test_part_b_interface_contract():
    verifier = InterfaceContractVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4B-INTERFACE-CONTRACT"
    assert report.status == VerificationStatus.PASSED
    assert report.breaking_changes_detected == 0
    assert len(report.contracts) > 0
    assert len(report.checks) == 4


def test_part_c_api_chain():
    verifier = APIChainVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4C-API-CHAIN"
    assert report.status == VerificationStatus.PASSED
    assert report.silent_corruption_detected is False
    assert report.total_steps == 12
    assert report.all_stages_verified is True


def test_part_d_state_propagation():
    verifier = StatePropagationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4D-STATE-PROPAGATION"
    assert report.status == VerificationStatus.PASSED
    assert report.sync_consistency_rate_pct == 100.0
    assert report.distributed_lock_contention_events == 0
    assert len(report.entities) > 0


def test_part_e_knowledge_flow():
    verifier = KnowledgeFlowVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4E-KNOWLEDGE-FLOW"
    assert report.status == VerificationStatus.PASSED
    assert report.data_loss_detected is False
    assert report.unauthorized_leakage_detected is False
    assert report.total_pipeline_stages == 11


def test_part_f_memory_interaction():
    verifier = MemoryInteractionVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4F-MEMORY-INTERACTION"
    assert report.status == VerificationStatus.PASSED
    assert report.memory_tiers_evaluated == 6
    assert report.memory_leak_detected is False
    assert report.tenant_cross_talk_events == 0


def test_part_g_planning_pipeline():
    verifier = PlanningPipelineVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4G-PLANNING-PIPELINE"
    assert report.status == VerificationStatus.PASSED
    assert report.goal_to_task_decomp_rate_pct == 100.0
    assert report.reflection_learning_verified is True
    assert len(report.stages) == 6


def test_part_h_agent_collaboration():
    verifier = AgentCollaborationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4H-AGENT-COLLABORATION"
    assert report.status == VerificationStatus.PASSED
    assert report.deadlock_detected is False
    assert report.consensus_success_rate_pct == 100.0
    assert len(report.interactions) > 0


def test_part_i_cognitive_integration():
    verifier = CognitiveIntegrationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4I-COGNITIVE-INTEGRATION"
    assert report.status == VerificationStatus.PASSED
    assert report.hallucination_prevention_verified is True
    assert report.fact_grounding_score_pct == 100.0
    assert len(report.steps) == 5


def test_part_j_security_boundary():
    verifier = SecurityBoundaryVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4J-SECURITY-BOUNDARY"
    assert report.status == VerificationStatus.PASSED
    assert report.tenant_data_cross_contamination == 0
    assert report.zero_trust_compliance_pct == 100.0
    assert len(report.boundaries) == 6


def test_part_k_lifecycle_integration():
    verifier = LifecycleIntegrationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4K-LIFECYCLE-INTEGRATION"
    assert report.status == VerificationStatus.PASSED
    assert report.invalid_transitions_blocked > 0
    assert report.system_wide_sync_pct == 100.0
    assert len(report.transitions) == 7


def test_part_l_deployment_integration():
    verifier = DeploymentIntegrationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4L-DEPLOYMENT-INTEGRATION"
    assert report.status == VerificationStatus.PASSED
    assert report.blue_green_verified is True
    assert report.canary_verified is True
    assert report.auto_rollback_latency_sec < 5.0
    assert len(report.strategies) == 3


def test_part_m_marketplace_validation():
    verifier = MarketplaceValidationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4M-MARKETPLACE-VALIDATION"
    assert report.status == VerificationStatus.PASSED
    assert report.semver_conflict_detected == 0
    assert report.sandbox_execution_verified is True
    assert len(report.packages) == 4


def test_part_n_event_bus():
    verifier = EventBusVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4N-EVENT-BUS"
    assert report.status == VerificationStatus.PASSED
    assert report.ordering_violations_count == 0
    assert report.idempotency_rate_pct == 100.0
    assert report.total_events_processed > 0


def test_part_o_scheduler():
    verifier = SchedulerVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4O-SCHEDULER"
    assert report.status == VerificationStatus.PASSED
    assert report.duplicate_executions_count == 0
    assert report.leader_election_failover_verified is True
    assert len(report.jobs) == 4


def test_part_p_observability_integration():
    verifier = ObservabilityIntegrationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4P-OBSERVABILITY-INTEGRATION"
    assert report.status == VerificationStatus.PASSED
    assert report.unreconstructable_executions_count == 0
    assert report.trace_propagation_rate_pct == 100.0
    assert len(report.telemetry_links) == 6


def test_part_q_data_integrity():
    verifier = DataIntegrityVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4Q-DATA-INTEGRITY"
    assert report.status == VerificationStatus.PASSED
    assert report.detection_rate_pct == 100.0
    assert report.unrecovered_corruptions_count == 0
    assert len(report.probes) == 5


def test_part_r_failure_propagation():
    verifier = FailurePropagationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4R-FAILURE-PROPAGATION"
    assert report.status == VerificationStatus.PASSED
    assert report.cascading_failure_count == 0
    assert report.blast_radius_containment_pct == 100.0
    assert len(report.drills) == 5


def test_part_s_cross_system_performance():
    verifier = CrossSystemPerformanceVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4S-CROSS-SYSTEM-PERF"
    assert report.status == VerificationStatus.PASSED
    assert report.e2e_p95_latency_ms < 500.0
    assert report.backpressure_threshold_respected is True
    assert len(report.performance_metrics) == 5


def test_part_t_enterprise_workflows():
    verifier = EnterpriseWorkflowsVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4T-ENTERPRISE-WORKFLOWS"
    assert report.status == VerificationStatus.PASSED
    assert report.total_scenarios_executed == 6
    assert report.passed_scenarios_count == 6
    assert report.overall_workflow_accuracy_pct >= 99.0


def test_part_u_integration_regression():
    verifier = IntegrationRegressionVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4U-INTEGRATION-REGRESSION"
    assert report.status == VerificationStatus.PASSED
    assert report.zero_regression_verified is True
    assert report.regression_pass_rate_pct == 100.0
    assert len(report.matrices) == 5


def test_part_v_evidence_generation():
    verifier = EvidenceGenerationVerifier()
    report = verifier.verify()
    assert report.verifier_id == "VERIFY-4V-EVIDENCE-GENERATION"
    assert report.status == VerificationStatus.PASSED
    assert report.cryptographic_integrity_verified is True
    assert len(report.evidence_manifest) >= 8


# --- 2. Scoring & Certification Tests ---

def test_integration_quality_scorer():
    runtime = CrossSystemIntegrationVerificationRuntime()
    reports = {k: v.verify() for k, v in runtime.verifiers.items()}
    scorer = CrossSystemIntegrationQualityScorer()
    score = scorer.calculate_score(reports)

    assert score.overall_score == 100.0
    assert score.certification_tier == CertificationTier.ENTERPRISE_INTEGRATION_CERTIFIED
    assert score.verification_status == VerificationStatus.PASSED
    assert len(score.categories) == 7

    # Verify pillar weights sum to 1.0
    total_weights = sum(cat.weight for cat in score.categories)
    assert pytest.approx(total_weights, 0.001) == 1.0


# --- 3. Exporter & SHA-256 Manifest Tests ---

def test_integration_quality_exporter(tmp_output_dir):
    runtime = CrossSystemIntegrationVerificationRuntime()
    report = runtime.execute_all(output_dir=tmp_output_dir)

    assert os.path.exists(tmp_output_dir)
    assert os.path.exists(os.path.join(tmp_output_dir, "manifest.json"))
    assert os.path.exists(os.path.join(tmp_output_dir, "metadata.json"))
    assert os.path.exists(os.path.join(tmp_output_dir, "cross_system_integration_summary_report.md"))
    assert os.path.exists(os.path.join(tmp_output_dir, "cross_system_integration_quality_score.json"))

    # Verify manifest has SHA-256 for all exported files
    with open(os.path.join(tmp_output_dir, "manifest.json"), "r") as f:
        manifest = json.load(f)
    assert len(manifest) >= 24
    for fname, meta in manifest.items():
        assert "sha256" in meta
        assert len(meta["sha256"]) == 64
        assert meta["size_bytes"] > 0


# --- 4. Master Synchronous Runtime Tests ---

def test_runtime_execution(tmp_output_dir):
    runtime = CrossSystemIntegrationVerificationRuntime()
    report = runtime.execute_all(output_dir=tmp_output_dir)

    assert report.status == VerificationStatus.PASSED
    assert report.score.overall_score == 100.0
    assert len(report.reports) == 22
    assert report.score.certification_tier == CertificationTier.ENTERPRISE_INTEGRATION_CERTIFIED


# --- 5. FastAPI REST API Endpoint Tests ---

def test_api_health(api_client):
    res = api_client.get("/api/v1/verification/cross-system-integration/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert data["verifiers_count"] == 22


def test_api_run_verification(api_client, tmp_output_dir):
    res = api_client.post(f"/api/v1/verification/cross-system-integration/run?output_dir={tmp_output_dir}")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "PASSED"
    assert data["score"]["overall_score"] == 100.0
    assert len(data["reports"]) == 22


def test_api_get_score(api_client):
    res = api_client.get("/api/v1/verification/cross-system-integration/score")
    assert res.status_code == 200
    data = res.json()
    assert data["overall_score"] == 100.0
    assert data["certification_tier"] == "Enterprise Integration Certified"


def test_api_get_report(api_client):
    res = api_client.get("/api/v1/verification/cross-system-integration/report")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "PASSED"
    assert len(data["reports"]) == 22


def test_api_get_subsystem_report(api_client):
    res = api_client.get("/api/v1/verification/cross-system-integration/subsystem/api_chain")
    assert res.status_code == 200
    data = res.json()
    assert data["verifier_id"] == "VERIFY-4C-API-CHAIN"
    assert data["total_steps"] == 12


def test_api_get_invalid_subsystem_report(api_client):
    res = api_client.get("/api/v1/verification/cross-system-integration/subsystem/non_existent_subsystem")
    assert res.status_code == 404
