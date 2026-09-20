"""
Unit and Integration tests for Enterprise Reporting, Audit Intelligence & Dashboards (PART 8).
"""
import pytest
from app.platform_verification.reporting_audit import (
    AuditReportRecord,
    ComplianceControlMapping,
    ControlStatus,
    EnterpriseReportingPlatformRuntime,
    NotificationEventType,
    ReportFormat,
    ReportType,
    UserRole,
    VerificationSummary,
)


@pytest.fixture
def runtime():
    return EnterpriseReportingPlatformRuntime()


def test_audit_report_generation_and_cryptographic_integrity(runtime):
    """Test creating and cryptographically validating an audit report."""
    data = {
        "dataset_name": "Invoice Benchmark v4",
        "sample_count": 50000,
        "confidence_level": 0.95,
        "measured_accuracy": 0.952,
        "hallucination_rate": 0.012,
    }

    report = runtime.report_generator.generate_report(
        report_type=ReportType.AI_EVALUATION_REPORT,
        title="AI Evaluation & Grounding Certification Report",
        scope="DocuTask Agent v2.4.0 Production Model",
        data=data,
        evidence_refs=["EVD-EXEC-98231", "EVD-TRACE-5521"],
        generated_by="LeadAIEvaluationArchitect",
        report_format=ReportFormat.JSON,
    )

    assert report.report_id.startswith("RPT-AI_E-")
    assert report.verify_integrity() is True
    assert len(report.sha256_digest) == 64

    # Test tampering detection
    report.content["measured_accuracy"] = 0.999
    assert report.verify_integrity() is False


def test_compliance_mapping_engine(runtime):
    """Test mapping verification results to NIST AI RMF, ISO 42001, and SOC 2 controls."""
    nist_controls = runtime.compliance_engine.evaluate_compliance(framework="NIST_AI_RMF")
    assert len(nist_controls) >= 2
    assert all(c.status == ControlStatus.PASSED for c in nist_controls)

    all_controls = runtime.compliance_engine.evaluate_compliance()
    assert len(all_controls) >= 4


def test_role_based_dashboard_views(runtime):
    """Test generating Executive, Engineering, Security, and AI Governance views."""
    # 1. Executive Dashboard
    exec_view = runtime.dashboard_engine.build_executive_dashboard()
    assert exec_view.production_readiness_pct > 90.0
    assert exec_view.current_certification_level == "LEVEL_7_ENTERPRISE_CERTIFIED"

    # 2. Engineering Dashboard
    eng_view = runtime.dashboard_engine.build_engineering_dashboard()
    assert len(eng_view.recent_runs) >= 1
    assert eng_view.code_coverage_pct >= 85.0

    # 3. Security Dashboard
    sec_view = runtime.dashboard_engine.build_security_dashboard()
    assert sec_view.prompt_injection_resistance_pct >= 98.0
    assert sec_view.vulnerability_counts["critical"] == 0

    # 4. AI Governance Dashboard
    ai_view = runtime.dashboard_engine.build_ai_governance_dashboard()
    assert ai_view.hallucination_rate <= 0.03
    assert len(ai_view.model_comparisons) >= 2


def test_notification_alert_dispatch(runtime):
    """Test dispatching role-targeted alerts."""
    alert = runtime.notification_service.send_alert(
        event_type=NotificationEventType.CERTIFICATION_EXPIRING,
        severity="WARNING",
        title="Certification Expiring in 14 Days",
        message="Level 7 Enterprise Certification for DocuTask Agent requires reverification.",
        roles=[UserRole.EXECUTIVE, UserRole.ENGINEER],
    )

    assert alert.alert_id.startswith("ALT-")
    assert UserRole.EXECUTIVE in alert.recipient_roles

    exec_alerts = runtime.notification_service.list_alerts(UserRole.EXECUTIVE)
    assert len(exec_alerts) >= 1


def test_audit_package_export(runtime):
    """Test packaging complete audit bundle with checksum receipt."""
    rpt = runtime.report_generator.generate_report(
        report_type=ReportType.SOC2_COMPLIANCE_REPORT,
        title="SOC 2 Type II Verification Evidence",
        scope="Enterprise Deployment",
        data={"controls_evaluated": 12, "passed": 12},
        evidence_refs=["EVD-LOG-001"],
        generated_by="GRCLead",
    )

    pkg = runtime.export_manager.export_audit_package(
        system_version="v2.4.0",
        include_reports=[rpt.report_id],
        evidence_manifest=["evidence/cas/sha256/abc12345"],
    )

    assert pkg.package_id.startswith("AUDIT-PKG-")
    assert len(pkg.reports) == 1
    assert len(pkg.package_checksum) == 64
    assert pkg.metrics_snapshot["security_status"] == "PASSED"
