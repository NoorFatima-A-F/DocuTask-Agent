"""Unit tests for Report Generator."""

from pathlib import Path
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from enterprise_audit_engine.reporters.report_generator import ReportGenerator


def test_report_generation(tmp_path):
    reporter = ReportGenerator(tmp_path)

    record = EvidenceRecord.create(
        category="TestReport",
        collector="ReportCollector",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        summary="Automated report generation verified",
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED,
    )

    reports = reporter.generate_all_reports([record])
    assert "executive_summary" in reports
    assert "technical_due_diligence" in reports
    assert "security_report" in reports
    assert "production_readiness_matrix" in reports

    for name, p in reports.items():
        assert p.exists()
        content = p.read_text(encoding="utf-8")
        assert record.id in content
