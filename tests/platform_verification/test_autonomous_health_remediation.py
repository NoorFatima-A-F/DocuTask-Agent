"""Test Suite for Phase 3H.4.3 - Autonomous Health Remediation & Recovery Action Framework.

Tests all 14 sub-parts of Phase 3H.4.3:
1. Remediation Architecture
2. Remediation Policy Engine
3. Action Classification (Levels 0 - 3)
4. Recovery Decision Engine (Action Planning)
5. Safety Guard System (Preconditions, Rate Limits, Blast Radius)
6. Remediation Executor (Controlled operations)
7. Recovery Verification Engine (Post-recovery health validation)
8. Rollback Mechanism (State reversion & human escalation)
9. Self-Healing Chaos Scenarios (5 Production scenarios)
10. Remediation Intelligence Metrics (MTTR, MTTD, Automation Success Rate)
11. Security Audit (RBAC, Whitelisting, Zero secret leaks)
12. Observability & Telemetry (Logs, Metrics, Traces)
13. Evidence Generation (8 JSON manifests)
14. Certification Scoring (Weighted 6-dimension scorecard)
Plus FastAPI HTTP router endpoints.
"""

import os
import json
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.autonomous_remediation.policies.remediation_policy_engine import (
    RemediationPolicyEngine,
)
from app.platform_verification.autonomous_remediation.classifier.action_classifier import (
    ActionClassifier,
)
from app.platform_verification.autonomous_remediation.planner.recovery_decision_engine import (
    RecoveryDecisionEngine,
)
from app.platform_verification.autonomous_remediation.safety.safety_guard import (
    SafetyGuard,
)
from app.platform_verification.autonomous_remediation.executor.remediation_executor import (
    RemediationExecutor,
)
from app.platform_verification.autonomous_remediation.validators.recovery_validator import (
    RecoveryValidator,
)
from app.platform_verification.autonomous_remediation.rollback.rollback_manager import (
    RollbackManager,
)
from app.platform_verification.autonomous_remediation.scenarios.self_healing_scenarios_verifier import (
    SelfHealingScenariosVerifier,
)
from app.platform_verification.autonomous_remediation.metrics.remediation_metrics_collector import (
    RemediationMetricsCollector,
)
from app.platform_verification.autonomous_remediation.security.remediation_permissions import (
    RemediationPermissionsAuditor,
)
from app.platform_verification.autonomous_remediation.observability.remediation_telemetry_emitter import (
    RemediationTelemetryEmitter,
)
from app.platform_verification.autonomous_remediation.scoring.remediation_quality_scorer import (
    AutonomousRemediationScorer,
)
from app.platform_verification.autonomous_remediation.exporter.remediation_evidence_exporter import (
    RemediationEvidenceExporter,
)
from app.platform_verification.autonomous_remediation.runtime.autonomous_remediation_runtime import (
    AutonomousRemediationRuntime,
)
from app.platform_verification.autonomous_remediation.api.autonomous_remediation_api import (
    router as remediation_router,
)
from app.platform_verification.autonomous_remediation.domain.models import (
    ActionLevel,
    RemediationRisk,
    ExecutionApproval,
    RemediationStatus,
    SelfHealingTier,
    FailureContext,
)


def test_part_3h_4_3_1_remediation_architecture():
    runtime = AutonomousRemediationRuntime()
    assert runtime.policy_engine is not None
    assert runtime.classifier is not None
    assert runtime.decision_engine is not None
    assert runtime.safety_guard is not None
    assert runtime.executor is not None
    assert runtime.validator is not None
    assert runtime.rollback_mgr is not None


def test_part_3h_4_3_2_remediation_policy_engine():
    engine = RemediationPolicyEngine()
    report = engine.get_policy_report()
    assert report.status == "PASS"
    assert report.total_policies >= 6
    assert report.level_0_count >= 1
    assert report.level_1_count >= 3
    assert report.level_2_count >= 2
    assert report.level_3_count >= 1

    policy = engine.find_policy_for_condition("database_connection_exhausted")
    assert policy is not None
    assert policy.action == "restart_connection_pool"
    assert policy.action_level == ActionLevel.LEVEL_1
    assert policy.risk == RemediationRisk.LOW


def test_part_3h_4_3_3_action_classifier_levels_0_to_3():
    classifier = ActionClassifier()

    c0 = classifier.classify_action("log_latency_telemetry_only")
    assert c0["level"] == ActionLevel.LEVEL_0

    c1 = classifier.classify_action("restart_connection_pool")
    assert c1["level"] == ActionLevel.LEVEL_1
    assert c1["approval"] == ExecutionApproval.AUTOMATIC

    c2 = classifier.classify_action("restart_worker_container")
    assert c2["level"] == ActionLevel.LEVEL_2
    assert c2["risk"] == RemediationRisk.MEDIUM

    c3 = classifier.classify_action("restore_database_from_backup")
    assert c3["level"] == ActionLevel.LEVEL_3
    assert c3["approval"] == ExecutionApproval.PENDING_HUMAN


def test_part_3h_4_3_4_recovery_decision_engine():
    engine = RecoveryDecisionEngine()

    # High confidence known failure
    ctx_worker = FailureContext(
        failure_id="FAIL-001",
        root_cause="worker_heartbeat_missing",
        severity="SEV-2",
        confidence=0.96,
        affected_component="celery_worker_01",
        impact_scope="single_instance",
    )
    dec_worker = engine.make_decision(ctx_worker)
    assert dec_worker.selected_action == "restart_worker_container"
    assert dec_worker.action_level == ActionLevel.LEVEL_2
    assert dec_worker.approval == ExecutionApproval.AUTOMATIC
    assert dec_worker.confidence_threshold_met is True

    # Low confidence failure
    ctx_low = FailureContext(
        failure_id="FAIL-002",
        root_cause="worker_heartbeat_missing",
        severity="SEV-2",
        confidence=0.60,
        affected_component="celery_worker_01",
        impact_scope="single_instance",
    )
    dec_low = engine.make_decision(ctx_low)
    assert dec_low.approval == ExecutionApproval.PENDING_HUMAN
    assert dec_low.confidence_threshold_met is False


def test_part_3h_4_3_5_safety_guard_rate_limits_and_blast_radius():
    guard = SafetyGuard(default_cooldown_seconds=60)
    engine = RecoveryDecisionEngine()

    ctx = FailureContext(
        failure_id="FAIL-003",
        root_cause="worker_heartbeat_missing",
        severity="SEV-2",
        confidence=0.95,
        affected_component="celery_worker",
        impact_scope="single_instance",
    )
    dec = engine.make_decision(ctx)
    target = dec.parameters.get("target", "celery_worker")
    max_attempts = dec.parameters.get("max_attempts", 3)

    # Attempts within allowed limit
    for _ in range(max_attempts):
        res = guard.validate_safety(dec)
        assert res.safe_to_execute is True
        guard.register_execution_attempt(target)

    # Exceeding attempt: rate limit triggered
    res_exceeded = guard.validate_safety(dec)
    assert res_exceeded.safe_to_execute is False
    assert res_exceeded.rate_limit_passed is False
    assert res_exceeded.cooldown_remaining_seconds > 0



def test_part_3h_4_3_6_remediation_executor():
    executor = RemediationExecutor()
    engine = RecoveryDecisionEngine()
    ctx = FailureContext(
        failure_id="FAIL-004",
        root_cause="database_connection_exhausted",
        severity="SEV-1",
        confidence=0.98,
        affected_component="postgresql_pool",
        impact_scope="single_instance",
    )
    decision = engine.make_decision(ctx)
    entry = executor.execute_remediation(decision)

    assert entry.action == "restart_connection_pool"
    assert entry.status == RemediationStatus.SUCCESS
    assert entry.before_state == "UNHEALTHY"
    assert entry.after_state == "RECOVERING"
    assert entry.duration_ms > 0

    report = executor.get_execution_report()
    assert report.total_actions_executed >= 1
    assert report.successful_actions >= 1


def test_part_3h_4_3_7_recovery_verification_engine():
    validator = RecoveryValidator()
    executor = RemediationExecutor()
    engine = RecoveryDecisionEngine()

    ctx = FailureContext(
        failure_id="FAIL-005",
        root_cause="gemini_api_503_outage",
        severity="SEV-2",
        confidence=0.95,
        affected_component="ai_provider_router",
        impact_scope="local_service",
    )
    decision = engine.make_decision(ctx)
    entry = executor.execute_remediation(decision)
    rep = validator.validate_recovery(entry)

    assert rep.status == "PASS"
    assert rep.total_validations >= 1
    assert rep.recovery_success_rate_pct == 100.0


def test_part_3h_4_3_8_rollback_mechanism_and_history():
    rollback_mgr = RollbackManager()
    executor = RemediationExecutor()
    engine = RecoveryDecisionEngine()

    ctx = FailureContext(
        failure_id="FAIL-006",
        root_cause="redis_queue_backlog",
        severity="SEV-2",
        confidence=0.92,
        affected_component="queue_fleet",
        impact_scope="local_service",
    )
    decision = engine.make_decision(ctx)
    entry = executor.execute_remediation(decision)
    entry.status = RemediationStatus.FAILED  # simulate failure

    report = rollback_mgr.trigger_rollback(entry)
    assert report.status == "PASS"
    assert report.total_rollbacks_triggered >= 1
    assert report.successful_rollbacks >= 1
    assert report.escalated_incidents_count >= 1


def test_part_3h_4_3_9_self_healing_chaos_scenarios():
    verifier = SelfHealingScenariosVerifier()
    report = verifier.verify_scenarios()

    assert report.status == "PASS"
    assert report.total_scenarios == 5
    assert report.passed_scenarios == 5
    scen_ids = [s.scenario_id for s in report.scenarios]
    assert "SCEN-01-WORKER-CRASH" in scen_ids
    assert "SCEN-02-DB-POOL" in scen_ids
    assert "SCEN-03-QUEUE-SURGE" in scen_ids
    assert "SCEN-04-AI-FALLBACK" in scen_ids
    assert "SCEN-05-REMEDIATION-FAIL" in scen_ids


def test_part_3h_4_3_10_remediation_intelligence_metrics():
    collector = RemediationMetricsCollector()
    report = collector.collect_metrics()

    assert report.status == "PASS"
    assert report.total_incidents_detected == 25
    assert report.successful_remediations == 24
    assert report.automation_success_rate_pct >= 95.0
    assert report.mttr_seconds < 5.0
    assert report.mttd_seconds < 2.0


def test_part_3h_4_3_11_security_rbac_and_whitelisting():
    auditor = RemediationPermissionsAuditor()
    report = auditor.audit_security()

    assert report.status == "PASS"
    assert report.secret_leaks_found == 0
    assert report.unauthorized_commands_blocked >= 3
    assert report.rbac_enforced is True


def test_part_3h_4_3_12_observability_and_telemetry():
    emitter = RemediationTelemetryEmitter()

    log = emitter.emit_lifecycle_log(
        event_type="REMEDIATION_STARTED",
        execution_id="EXEC-TEST-01",
        action="restart_worker_container",
        target="celery_worker_01",
        details={"reason": "heartbeat missing"},
    )
    assert log["event"] == "REMEDIATION_STARTED"
    assert log["action"] == "restart_worker_container"

    metrics = emitter.get_prometheus_metrics()
    assert "docutask_remediation_attempts_total" in metrics
    assert "docutask_remediation_success_total" in metrics

    spans = emitter.get_trace_lifecycle_spans("INC-TEST-01")
    assert len(spans) == 6


def test_part_3h_4_3_13_evidence_exporter_and_8_manifests(tmp_path):
    output_dir = str(tmp_path / "test_remediation_manifests")
    runtime = AutonomousRemediationRuntime(export_dir=output_dir)
    res = runtime.run_full_verification()

    assert os.path.exists(output_dir)
    expected_files = [
        "remediation_policy_report.json",
        "action_execution_report.json",
        "recovery_validation_report.json",
        "rollback_report.json",
        "self_healing_test_report.json",
        "security_report.json",
        "certification_report.json",
        "metadata.json",
    ]
    for fname in expected_files:
        fpath = os.path.join(output_dir, fname)
        assert os.path.exists(fpath), f"Missing manifest {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data is not None


def test_part_3h_4_3_14_remediation_scorer_and_enterprise_tier():
    runtime = AutonomousRemediationRuntime()
    res = runtime.run_full_verification()
    scorecard = res["scorecard"]

    assert scorecard.passed is True
    assert scorecard.overall_score >= 95.0
    assert scorecard.certification_tier == SelfHealingTier.ENTERPRISE_SELF_HEALING_READY
    assert scorecard.certification_verdict == "CERTIFIED"
    assert scorecard.recovery_accuracy_score >= 95.0
    assert scorecard.safety_controls_score >= 95.0
    assert scorecard.validation_correctness_score >= 95.0
    assert scorecard.rollback_capability_score >= 95.0


def test_autonomous_remediation_fastapi_endpoints():
    app = FastAPI()
    app.include_router(remediation_router)
    client = TestClient(app)

    endpoints = [
        "/health/remediation/policies",
        "/health/remediation/executions",
        "/health/remediation/validations",
        "/health/remediation/rollbacks",
        "/health/remediation/scenarios",
        "/health/remediation/metrics",
        "/health/remediation/security",
        "/health/remediation/scorecard",
    ]

    for ep in endpoints:
        resp = client.get(ep)
        assert resp.status_code == 200, f"Endpoint {ep} failed with status {resp.status_code}"
        assert resp.json() is not None

    trigger_resp = client.post(
        "/health/remediation/trigger",
        json={
            "failure_id": "FAIL-HTTP-001",
            "root_cause": "worker_heartbeat_missing",
            "severity": "SEV-2",
            "confidence": 0.95,
            "affected_component": "celery_worker_02",
        },
    )
    assert trigger_resp.status_code == 200
    assert trigger_resp.json()["status"] == "COMPLETED"

    post_resp = client.post("/health/remediation/verify")
    assert post_resp.status_code == 200
    data = post_resp.json()
    assert data["scorecard"]["overall_score"] >= 95.0
