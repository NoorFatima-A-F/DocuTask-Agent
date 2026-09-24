"""
Unit and Integration tests for Enterprise Verification Quality Gate & Certification Engine (PART 6).
"""
import pytest
from app.platform_verification.certification_engine import (
    CertificationLevel,
    CertificationStatus,
    ChangeType,
    EnterpriseCertificationPlatformRuntime,
    ExceptionRequest,
    GateComparisonOperator,
    QualityGateCondition,
    ReleaseDecisionType,
    RiskLevel,
)


@pytest.fixture
def runtime():
    return EnterpriseCertificationPlatformRuntime()


def test_quality_gate_condition_evaluations():
    """Verify operators and tolerances in quality gate conditions."""
    cond_gt = QualityGateCondition(
        metric_name="accuracy",
        operator=GateComparisonOperator.GREATER_THAN,
        threshold=0.95,
    )
    assert cond_gt.evaluate(0.96) is True
    assert cond_gt.evaluate(0.94) is False
    assert cond_gt.evaluate(None) is False

    cond_between = QualityGateCondition(
        metric_name="latency",
        operator=GateComparisonOperator.BETWEEN,
        threshold=[100, 500],
    )
    assert cond_between.evaluate(250) is True
    assert cond_between.evaluate(50) is False
    assert cond_between.evaluate(600) is False


def test_decision_engine_approved_flow(runtime):
    """Test standard release decision when all gates pass."""
    metrics = {
        "extraction_accuracy": 0.96,
        "workflow_completion_rate": 0.99,
        "p95_latency_ms": 420.0,
        "throughput_docs_per_sec": 12.0,
        "hallucination_rate": 0.015,
        "grounding_score": 0.97,
        "critical_vulnerabilities": 0,
        "prompt_injection_resistance": 0.99,
        "failure_rate": 0.002,
        "recovery_success_rate": 0.99,
        "availability_rate": 0.999,
        "overall_score": 96.8,
    }

    gate_ids = [
        "GATE_FUNCTIONAL_ACCURACY",
        "GATE_PERFORMANCE_SLA",
        "GATE_AI_QUALITY",
        "GATE_SECURITY_COMPLIANCE",
        "GATE_RELIABILITY",
    ]

    decision = runtime.decision_engine.make_release_decision(
        system_id="SYS_DOCUTASK_01",
        system_version="v2.4.0",
        model_version="gemini-1.5-pro",
        target_level=CertificationLevel.LEVEL_5_PRODUCTION_CERTIFIED,
        metrics=metrics,
        gate_ids=gate_ids,
        policy_ids=["PRODUCTION_RELEASE_POLICY"],
    )

    assert decision.decision == ReleaseDecisionType.APPROVED
    assert decision.requires_human_approval is False
    assert decision.risk_assessment.risk_level == RiskLevel.LOW
    assert len(decision.explainable_reasons) > 0


def test_decision_engine_critical_security_rejection(runtime):
    """Test automated rejection when critical security vulnerability is detected."""
    metrics = {
        "extraction_accuracy": 0.95,
        "workflow_completion_rate": 0.98,
        "critical_vulnerabilities": 2,  # VIOLATION
        "prompt_injection_resistance": 0.85,
        "hallucination_rate": 0.01,
        "grounding_score": 0.95,
        "overall_score": 78.0,
    }

    gate_ids = ["GATE_FUNCTIONAL_ACCURACY", "GATE_SECURITY_COMPLIANCE"]

    decision = runtime.decision_engine.make_release_decision(
        system_id="SYS_DOCUTASK_01",
        system_version="v2.4.0",
        model_version="gemini-1.5-pro",
        target_level=CertificationLevel.LEVEL_5_PRODUCTION_CERTIFIED,
        metrics=metrics,
        gate_ids=gate_ids,
        policy_ids=["PRODUCTION_RELEASE_POLICY"],
    )

    assert decision.decision == ReleaseDecisionType.REJECTED
    assert decision.risk_assessment.risk_level == RiskLevel.CRITICAL
    assert any("critical security vulnerabilities" in r.lower() for r in decision.risk_assessment.identified_risks)


def test_certification_issuance_and_cryptographic_verification(runtime):
    """Test cryptographic signing, integrity verification, and revocation."""
    metrics = {
        "extraction_accuracy": 0.96,
        "workflow_completion_rate": 0.99,
        "p95_latency_ms": 350.0,
        "throughput_docs_per_sec": 10.0,
        "hallucination_rate": 0.01,
        "grounding_score": 0.98,
        "critical_vulnerabilities": 0,
        "prompt_injection_resistance": 0.99,
        "overall_score": 97.5,
    }

    decision = runtime.decision_engine.make_release_decision(
        system_id="SYS_DOCUTASK_01",
        system_version="v2.4.0",
        model_version="gemini-1.5-pro",
        target_level=CertificationLevel.LEVEL_7_ENTERPRISE_CERTIFIED,
        metrics=metrics,
        gate_ids=["GATE_FUNCTIONAL_ACCURACY", "GATE_PERFORMANCE_SLA", "GATE_AI_QUALITY", "GATE_SECURITY_COMPLIANCE"],
    )

    cert = runtime.cert_engine.issue_certification(
        decision=decision,
        evidence_package_id="EVD-PKG-9941",
        approved_by="LeadReleaseArchitect",
        validity_days=60,
    )

    assert cert.id.startswith("CERT-")
    assert cert.status == CertificationStatus.ACTIVE
    assert cert.verify_integrity(runtime.cert_engine.secret_key) is True

    # Test tampering detection
    tampered_sig = cert.signature + "tamper"
    cert.signature = tampered_sig
    assert cert.verify_integrity(runtime.cert_engine.secret_key) is False

    # Restore and test revocation
    cert.signature = cert.generate_signature(runtime.cert_engine.secret_key)
    revoked = runtime.cert_engine.revoke_certification(
        certification_id=cert.id,
        reason="Security CVE detected in upstream parser",
        revoked_by="SecurityOfficer",
    )
    assert revoked.status == CertificationStatus.REVOKED
    assert runtime.cert_engine.verify_certification_validity(cert.id) is False


def test_exception_management_and_gate_waiver(runtime):
    """Test requesting and approving an exception to waive a non-critical gate failure."""
    exc = ExceptionRequest(
        exception_id="EXC-LATENCY-001",
        system_id="SYS_DOCUTASK_01",
        component="AI Extraction",
        gate_id="GATE_PERFORMANCE_SLA",
        metric_name="p95_latency_ms",
        risk_level=RiskLevel.MEDIUM,
        reason="Temporary upstream model quota degradation",
        owner="mlops-lead@docutask.internal",
        duration_days=14,
    )
    runtime.exception_manager.request_exception(exc)
    runtime.exception_manager.approve_exception("EXC-LATENCY-001", approver="PrincipalArchitect")

    active_exceptions = runtime.exception_manager.get_active_exceptions_for_system("SYS_DOCUTASK_01")
    assert len(active_exceptions) == 1

    # Evaluate with higher latency
    metrics = {
        "p95_latency_ms": 2200.0,  # Fails 1500ms threshold
        "throughput_docs_per_sec": 6.0,
    }

    results = runtime.gate_engine.evaluate_gates(
        gate_ids=["GATE_PERFORMANCE_SLA"],
        metrics=metrics,
        active_exceptions=active_exceptions,
    )

    assert results[0].passed is True  # Waived via exception
    assert "[WAIVED via approved exception" in results[0].condition_results[0].message


def test_change_impact_analysis_and_invalidation(runtime):
    """Test automated change impact analysis and cascading certification invalidation."""
    metrics = {
        "extraction_accuracy": 0.96,
        "workflow_completion_rate": 0.99,
        "p95_latency_ms": 300.0,
        "throughput_docs_per_sec": 10.0,
        "hallucination_rate": 0.01,
        "grounding_score": 0.98,
        "critical_vulnerabilities": 0,
        "prompt_injection_resistance": 0.99,
        "overall_score": 98.0,
    }

    decision = runtime.decision_engine.make_release_decision(
        system_id="SYS_DOCUTASK_01",
        system_version="v2.4.0",
        model_version="gemini-1.5-pro",
        target_level=CertificationLevel.LEVEL_5_PRODUCTION_CERTIFIED,
        metrics=metrics,
        gate_ids=["GATE_FUNCTIONAL_ACCURACY", "GATE_AI_QUALITY", "GATE_SECURITY_COMPLIANCE"],
    )

    cert = runtime.cert_engine.issue_certification(
        decision=decision,
        evidence_package_id="EVD-PKG-100",
        approved_by="GovernanceBoard",
    )

    assert cert.status == CertificationStatus.ACTIVE

    # Trigger Model Change
    report = runtime.change_impact_analyzer.analyze_change(
        change_type=ChangeType.MODEL,
        changed_entity="gemini-1.5-pro -> gemini-2.0-flash",
        version_before="1.5",
        version_after="2.0",
        system_id="SYS_DOCUTASK_01",
    )

    assert cert.id in report.invalidated_certifications
    assert cert.status == CertificationStatus.REVOKED
    assert "FullModelEvaluationSuite" in report.required_reverification_suites
