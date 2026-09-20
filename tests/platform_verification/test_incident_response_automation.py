"""Comprehensive Test Suite for Phase 3H.3.6: Incident Response Automation & Self-Healing.

Validates all 13 core subsystems, domain models, declarative runbooks, self-healing execution,
safety guardrails, cross-signal correlation, postmortem generation, security, and evidence manifests.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.platform_verification.incident_response_automation.architecture.incident_arch_verifier import (
    IncidentArchVerifier,
)
from app.platform_verification.incident_response_automation.cicd.cicd_incident_verifier import (
    CICDIncidentVerifier,
)
from app.platform_verification.incident_response_automation.classifier.incident_classifier import (
    IncidentClassifier,
)
from app.platform_verification.incident_response_automation.correlation.incident_correlation_engine import (
    IncidentCorrelationEngine,
)
from app.platform_verification.incident_response_automation.detector.incident_detector import (
    IncidentDetector,
)
from app.platform_verification.incident_response_automation.domain.models import (
    ActionRiskLevel,
    CICDPipelineReport,
    IncidentArchitectureReport,
    IncidentAutomationTier,
    IncidentCategory,
    IncidentClassificationReport,
    IncidentCorrelationReport,
    IncidentDetectionReport,
    IncidentKnowledgeReport,
    IncidentQualityScorecard,
    IncidentSecurityReport,
    IncidentSeverity,
    PostmortemReport,
    RecoveryPolicyReport,
    RunbookExecutionReport,
    SelfHealingReport,
)
from app.platform_verification.incident_response_automation.exporter.incident_evidence_exporter import (
    IncidentEvidenceExporter,
)
from app.platform_verification.incident_response_automation.healing.self_healing_engine import (
    SelfHealingEngine,
)
from app.platform_verification.incident_response_automation.knowledge.incident_knowledge_base import (
    IncidentKnowledgeBase,
)
from app.platform_verification.incident_response_automation.postmortem.postmortem_generator import (
    PostmortemGenerator,
)
from app.platform_verification.incident_response_automation.runbooks.runbook_engine import (
    RunbookEngine,
)
from app.platform_verification.incident_response_automation.runtime.incident_automation_runtime import (
    IncidentAutomationRuntime,
)
from app.platform_verification.incident_response_automation.safety.recovery_policy_engine import (
    RecoveryPolicyEngine,
)
from app.platform_verification.incident_response_automation.scoring.incident_quality_scorer import (
    IncidentQualityScorer,
)
from app.platform_verification.incident_response_automation.security.incident_security_auditor import (
    IncidentSecurityAuditor,
)


# ============================================================================
# Part 1: Incident Architecture Verification Tests
# ============================================================================
def test_incident_architecture() -> None:
    verifier = IncidentArchVerifier()
    report: IncidentArchitectureReport = verifier.verify_architecture()

    assert report.incident_engine_active is True
    assert report.detection_layer_isolated is True
    assert report.automation_enabled is True
    assert report.rollback_supported is True
    assert report.audit_logging_active is True
    assert len(report.subsystems) == 7
    assert report.passed is True


# ============================================================================
# Part 2: Incident Detection Tests
# ============================================================================
def test_incident_detection() -> None:
    detector = IncidentDetector()
    report: IncidentDetectionReport = detector.detect_incidents()

    assert report.total_signals_detected >= 4
    assert report.avg_detection_latency_seconds <= 10.0
    assert report.precision_pct >= 95.0
    assert report.recall_pct >= 95.0
    assert report.false_positive_rate_pct <= 5.0
    assert report.false_negative_rate_pct <= 5.0
    assert report.passed is True


# ============================================================================
# Part 3: Incident Classification Tests
# ============================================================================
def test_incident_classification() -> None:
    classifier = IncidentClassifier()
    report: IncidentClassificationReport = classifier.classify_incidents()

    assert report.total_classified_incidents >= 6
    assert report.classification_accuracy_pct >= 95.0
    assert report.severity_breakdown["SEV-1"] >= 1
    assert report.severity_breakdown["SEV-2"] >= 1
    assert report.passed is True

    categories = {i.category for i in report.classified_items}
    assert IncidentCategory.APPLICATION_FAILURE in categories
    assert IncidentCategory.DATABASE_FAILURE in categories
    assert IncidentCategory.QUEUE_FAILURE in categories
    assert IncidentCategory.AI_PROVIDER_FAILURE in categories


# ============================================================================
# Part 4: Runbook Execution Tests
# ============================================================================
def test_runbook_execution() -> None:
    engine = RunbookEngine()
    report: RunbookExecutionReport = engine.execute_runbook("restart_worker.yaml")

    assert report.total_steps >= 4
    assert report.successful_steps == report.total_steps
    assert report.post_checks_passed is True
    assert report.execution_time_seconds <= 10.0
    assert report.passed is True


# ============================================================================
# Part 5: Self-Healing Execution Tests
# ============================================================================
def test_self_healing_execution() -> None:
    healing = SelfHealingEngine()
    report: SelfHealingReport = healing.execute_self_healing_tests()

    assert report.total_self_healing_tests >= 3
    assert report.successful_recoveries == report.total_self_healing_tests
    assert report.zero_task_loss_verified is True
    assert report.avg_mttr_seconds <= 15.0
    assert report.passed is True


# ============================================================================
# Part 6: Recovery Safety Policy Tests
# ============================================================================
def test_recovery_safety_policies() -> None:
    policy = RecoveryPolicyEngine()
    report: RecoveryPolicyReport = policy.evaluate_recovery_policies()

    assert report.total_policy_rules >= 6
    assert report.auto_executable_actions >= 3
    assert report.approval_gated_actions >= 2
    assert report.blocked_dangerous_actions >= 2
    assert report.passed is True

    blocked_rules = [r for r in report.rules if r.blocked]
    assert any("drop_database" in r.action_name for r in blocked_rules)
    assert any("delete_storage" in r.action_name for r in blocked_rules)


# ============================================================================
# Part 7: Incident Correlation Tests
# ============================================================================
def test_incident_correlation() -> None:
    correlation = IncidentCorrelationEngine()
    report: IncidentCorrelationReport = correlation.correlate_incident("INC-2026-003")

    assert len(report.causal_chain) >= 4
    assert report.metric_correlation_active is True
    assert report.trace_correlation_active is True
    assert report.log_correlation_active is True
    assert "Gemini" in report.root_cause_identified or "upload" in report.root_cause_identified
    assert report.passed is True


# ============================================================================
# Part 8: Incident Knowledge Base Tests
# ============================================================================
def test_incident_knowledge_base() -> None:
    kb = IncidentKnowledgeBase()
    report: IncidentKnowledgeReport = kb.get_knowledge_report()

    assert report.total_knowledge_entries >= 4
    assert report.knowledge_base_active is True
    assert report.query_retrieval_tested is True
    assert report.passed is True

    for entry in report.entries:
        assert entry.pattern_signature
        assert entry.recommended_solution
        assert entry.preventive_guardrail
        assert entry.success_rate_pct >= 90.0


# ============================================================================
# Part 9: Postmortem Generation Tests
# ============================================================================
def test_postmortem_generator() -> None:
    pm = PostmortemGenerator()
    report: PostmortemReport = pm.generate_postmortem("INC-2026-002")

    assert len(report.timeline) >= 6
    assert report.mttd_seconds > 0.0
    assert report.mttr_seconds > 0.0
    assert report.mttf_hours > 0.0
    assert len(report.remediation_steps_taken) >= 2
    assert len(report.preventive_action_items) >= 2
    assert report.passed is True


# ============================================================================
# Part 10: Security Audit Tests
# ============================================================================
def test_incident_security() -> None:
    security = IncidentSecurityAuditor()
    report: IncidentSecurityReport = security.audit_security()

    assert report.total_security_audits >= 5
    assert report.unauthorized_execution_blocked is True
    assert report.rbac_enforced is True
    assert report.audit_trails_immutable is True
    assert report.passed is True


# ============================================================================
# Part 11: CI/CD Pipeline Verification Tests
# ============================================================================
def test_cicd_pipeline_verification() -> None:
    cicd = CICDIncidentVerifier()
    report: CICDPipelineReport = cicd.verify_pipeline()

    assert len(report.stages_executed) == 8
    assert report.automated_recovery_verified is True
    assert report.certification_generated is True
    assert report.passed is True


# ============================================================================
# Part 12: Evidence Exporter Tests
# ============================================================================
def test_incident_evidence_exporter(tmp_path: Path) -> None:
    exporter = IncidentEvidenceExporter(output_dir=tmp_path)
    runtime = IncidentAutomationRuntime(export_dir=tmp_path)
    results = runtime.run_full_verification()

    manifests = exporter.export_all(
        arch_report=results["arch_report"],
        detect_report=results["detect_report"],
        class_report=results["class_report"],
        runbook_report=results["runbook_report"],
        healing_report=results["healing_report"],
        policy_report=results["policy_report"],
        correlation_report=results["correlation_report"],
        knowledge_report=results["knowledge_report"],
        postmortem_report=results["postmortem_report"],
        security_report=results["security_report"],
        cicd_report=results["cicd_report"],
        scorecard=results["scorecard"],
    )

    assert len(manifests) == 10
    for name, path in manifests.items():
        assert path.exists()
        assert path.stat().st_size > 0
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert isinstance(data, dict)


# ============================================================================
# Part 13: Quality Scorecard & Certification Tests
# ============================================================================
def test_incident_quality_scorecard() -> None:
    runtime = IncidentAutomationRuntime()
    results = runtime.run_full_verification()
    scorecard: IncidentQualityScorecard = results["scorecard"]

    assert scorecard.overall_score >= 95.00
    assert scorecard.certification_tier == IncidentAutomationTier.AUTONOMOUS_INCIDENT_RESPONSE_READY
    assert scorecard.certification_verdict == "CERTIFIED"
    assert scorecard.passed is True

    assert scorecard.detection_accuracy_score == 100.0
    assert scorecard.recovery_automation_score == 100.0
    assert scorecard.safety_controls_score == 100.0
    assert scorecard.incident_diagnosis_score == 100.0
    assert scorecard.operational_learning_score == 100.0
    assert scorecard.security_score == 100.0
