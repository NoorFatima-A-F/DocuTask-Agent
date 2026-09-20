"""
Pytest Suite for Enterprise Health Check Architecture Verification (Part 3H.1).
"""
import pytest
import os
import json
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.health_architecture.domain.models import (
    HealthState,
    HealthLayer,
    DependencyPriority,
    HealthVisibilityLevel,
    HealthArchitectureTier,
)
from app.platform_verification.health_architecture.state_machine.health_state_machine import (
    HealthStateMachine,
)
from app.platform_verification.health_architecture.contracts.health_contract_manager import (
    HealthContractManager,
)
from app.platform_verification.health_architecture.dependency_graph.dependency_graph_manager import (
    DependencyGraphManager,
)
from app.platform_verification.health_architecture.policies_and_security.health_failure_policy import (
    HealthFailurePolicyManager,
)
from app.platform_verification.health_architecture.policies_and_security.health_security_auditor import (
    HealthSecurityAuditor,
)
from app.platform_verification.health_architecture.automation.orchestration_automation_verifier import (
    OrchestrationAutomationVerifier,
)
from app.platform_verification.health_architecture.scoring.health_score_engine import (
    HealthScoreEngine,
)
from app.platform_verification.health_architecture.exporter.health_evidence_exporter import (
    HealthEvidenceExporter,
)
from app.platform_verification.health_architecture.runtime.health_runtime import (
    HealthVerificationRuntime,
)
from app.platform_verification.health_architecture.api.health_verification_api import (
    router as health_api_router,
)


@pytest.fixture
def state_machine():
    return HealthStateMachine()


@pytest.fixture
def contract_manager():
    return HealthContractManager()


@pytest.fixture
def dep_manager():
    return DependencyGraphManager()


@pytest.fixture
def failure_policy_manager():
    return HealthFailurePolicyManager()


@pytest.fixture
def security_auditor():
    return HealthSecurityAuditor()


@pytest.fixture
def automation_verifier():
    return OrchestrationAutomationVerifier()


@pytest.fixture
def score_engine():
    return HealthScoreEngine()


@pytest.fixture
def test_app():
    app = FastAPI(title="DocuTask Agent Test")
    app.include_router(health_api_router)
    return app


@pytest.fixture
def test_client(test_app):
    return TestClient(test_app)


# 1. Health State Machine Tests
def test_health_state_machine_transitions(state_machine):
    report = state_machine.verify_state_model()
    assert report.state_machine_valid is True
    assert report.total_states == 7
    assert len(report.layers_evaluated) == 4
    assert report.transition_coverage_pct >= 90.0
    assert report.passed is True

    # Check individual transition validity
    assert state_machine.is_valid_transition(HealthState.INITIALIZING, HealthState.READY) is True
    assert state_machine.is_valid_transition(HealthState.READY, HealthState.DEGRADED) is True
    assert state_machine.is_valid_transition(HealthState.DEGRADED, HealthState.RECOVERING) is True
    assert state_machine.is_valid_transition(HealthState.RECOVERING, HealthState.READY) is True
    assert state_machine.is_valid_transition(HealthState.READY, HealthState.INITIALIZING) is False


# 2. Four-Layer Health Model Tests
def test_four_layer_health_model(state_machine):
    process_layer = state_machine.evaluate_process_layer()
    assert process_layer["status"] == "HEALTHY"
    assert process_layer["memory_rss_mb"] < 500

    dep_layer = state_machine.evaluate_dependency_layer()
    assert dep_layer["critical_dependencies_available"] is True

    cap_layer = state_machine.evaluate_capability_layer()
    assert cap_layer["ocr_extraction_ready"] is True
    assert cap_layer["gemini_inference_ready"] is True

    wf_layer = state_machine.evaluate_workflow_layer()
    assert wf_layer["pipeline_throughput_healthy"] is True


# 3. Universal Health Contracts Tests
def test_universal_health_contracts(contract_manager):
    # Liveness Contract: pure process check
    live_resp = contract_manager.execute_liveness()
    assert live_resp["status"] == "HEALTHY"
    assert live_resp["state"] == "READY"
    assert "database" not in live_resp  # Proves zero dependency query in liveness

    # Readiness Contract: critical dependency check
    ready_resp = contract_manager.execute_readiness()
    assert ready_resp["status"] == "HEALTHY"
    assert ready_resp["traffic_routing"] == "ADMIT"

    # Full Health Contract: diagnostics
    health_resp = contract_manager.execute_full_health(authorization="Bearer admin-secret-token")
    assert health_resp["status"] == "HEALTHY"
    assert "components" in health_resp
    assert "diagnostics" in health_resp

    # Full Contract validation report
    report = contract_manager.validate_contracts()
    assert report.liveness_contract_valid is True
    assert report.liveness_isolated_from_dependencies is True
    assert report.readiness_contract_valid is True
    assert report.readiness_enforces_critical_deps is True
    assert report.passed is True


# 4. Dependency Graph & Criticality Tests
def test_dependency_graph_and_criticality(dep_manager):
    report = dep_manager.generate_dependency_graph()
    assert report.total_services_mapped >= 3
    assert report.critical_dependencies_count >= 5
    assert report.important_dependencies_count >= 4
    assert report.optional_dependencies_count >= 2
    assert report.passed is True

    # Assert timeouts for critical dependencies
    for spec in report.dependency_specs:
        if spec.priority == DependencyPriority.CRITICAL:
            assert spec.timeout_ms <= 3000
            assert spec.failure_state == "UNHEALTHY"


# 5. Failure Classification Policy Tests
def test_failure_classification_policies(failure_policy_manager):
    report = failure_policy_manager.verify_failure_policies()
    assert report.policies_defined_count >= 5
    assert report.detection_mechanisms_verified is True
    assert report.classification_rules_enforced is True
    assert report.response_actions_automated is True
    assert report.recovery_strategies_documented is True
    assert report.passed is True


# 6. Security Audit & Leak Prevention Tests
def test_role_based_health_security_and_leak_prevention(security_auditor):
    report = security_auditor.audit_security()
    assert report.public_endpoint_leak_free is True
    assert report.internal_endpoint_leak_free is True
    assert report.admin_diagnostic_auth_enforced is True
    assert report.credentials_leaked_count == 0
    assert report.urls_leaked_count == 0
    assert report.passed is True


# 7. Orchestration & Automation Tests
def test_orchestration_and_automation(automation_verifier):
    report = automation_verifier.verify_automation_integration()
    assert report.docker_healthcheck_compatible is True
    assert report.kubernetes_liveness_compatible is True
    assert report.kubernetes_readiness_compatible is True
    assert report.kubernetes_startup_compatible is True
    assert report.cicd_predeployment_gating_supported is True
    assert report.passed is True


# 8. Score Engine & Enterprise Certification Tier Tests
def test_health_score_engine_and_certification(
    state_machine,
    contract_manager,
    dep_manager,
    failure_policy_manager,
    security_auditor,
    automation_verifier,
    score_engine,
):
    model_rep = state_machine.verify_state_model()
    contract_rep = contract_manager.validate_contracts()
    dep_rep = dep_manager.generate_dependency_graph()
    policy_rep = failure_policy_manager.verify_failure_policies()
    sec_rep = security_auditor.audit_security()
    auto_rep = automation_verifier.verify_automation_integration()

    scorecard = score_engine.calculate_scorecard(
        model=model_rep,
        contract=contract_rep,
        deps=dep_rep,
        policy=policy_rep,
        sec=sec_rep,
        auto=auto_rep,
    )

    assert scorecard.overall_health_score >= 95.0
    assert scorecard.certification_tier == HealthArchitectureTier.ENTERPRISE_READY
    assert scorecard.certification_verdict == "CERTIFIED"
    assert scorecard.ci_cd_deployment_approved is True
    assert scorecard.passed is True


# 9. Evidence Exporter & Artifacts Tests
def test_health_evidence_exporter(tmp_path):
    output_dir = str(tmp_path / "health_architecture_verification")
    runtime = HealthVerificationRuntime(output_dir=output_dir)
    result = runtime.run_full_verification(export=True)

    assert result["success"] is True
    exported = result["exported_files"]
    assert len(exported) == 8

    for fname in [
        "state_model_report.json",
        "contract_report.json",
        "dependency_graph_report.json",
        "failure_policy_report.json",
        "security_report.json",
        "automation_report.json",
        "certification.json",
        "metadata.json",
    ]:
        assert fname in exported
        fpath = exported[fname]
        assert os.path.exists(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data is not None


# 10. FastAPI Verification Router Tests
def test_fastapi_endpoints(test_client):
    res_verify = test_client.get("/api/v1/health-architecture/verify")
    assert res_verify.status_code == 200
    data_verify = res_verify.json()
    assert data_verify["success"] is True
    assert data_verify["scorecard"]["overall_health_score"] >= 95.0

    res_live = test_client.get("/api/v1/health-architecture/live")
    assert res_live.status_code == 200
    assert res_live.json()["status"] == "HEALTHY"

    res_ready = test_client.get("/api/v1/health-architecture/ready")
    assert res_ready.status_code == 200
    assert res_ready.json()["status"] == "HEALTHY"

    res_health = test_client.get(
        "/api/v1/health-architecture/health",
        headers={"Authorization": "Bearer admin-token"},
    )
    assert res_health.status_code == 200
    assert "diagnostics" in res_health.json()

    res_deps = test_client.get("/api/v1/health-architecture/dependency-graph")
    assert res_deps.status_code == 200
    assert res_deps.json()["total_services_mapped"] >= 3
