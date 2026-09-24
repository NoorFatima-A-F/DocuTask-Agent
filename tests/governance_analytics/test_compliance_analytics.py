"""Tests for Compliance Framework Evaluators, Scoring, and Audit Readiness."""

from app.governance.analytics.warehouse.repositories import GovernanceDataWarehouseRepository
from app.governance.analytics.events.normalizers import GovernanceAnalyticsEvent, AnalyticsEventType
from app.governance.analytics.compliance.evaluator import ComplianceEvaluator, ComplianceFramework
from app.governance.analytics.compliance.reports import ComplianceReportingEngine


def test_compliance_framework_evaluator():
    repo = GovernanceDataWarehouseRepository()
    evaluator = ComplianceEvaluator(repo)
    reporting_engine = ComplianceReportingEngine(evaluator)

    # Ingest compliance audit events
    repo.insert_event(
        GovernanceAnalyticsEvent(
            tenant_id="tenant_c",
            event_type=AnalyticsEventType.AUDIT_CREATED,
            metadata={"compliance_framework": "SOC2", "control_id": "CC6.1", "evidence_id": "evd_100"},
            is_success=True,
        )
    )

    soc2_score = evaluator.evaluate_framework(ComplianceFramework.SOC2, "tenant_c")
    assert soc2_score.framework == ComplianceFramework.SOC2
    assert soc2_score.score == 100.0

    all_scores = evaluator.evaluate_all_frameworks("tenant_c")
    assert len(all_scores) == len(ComplianceFramework)

    readiness = reporting_engine.generate_audit_readiness_report("tenant_c")
    assert readiness.overall_readiness_score >= 80.0
    assert readiness.audit_readiness_status in {"AUDIT_READY", "MINOR_GAPS"}
