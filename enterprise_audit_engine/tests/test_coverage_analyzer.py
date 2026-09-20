"""Tests for Evidence Completeness & Coverage Verification."""

import pytest
from enterprise_audit_engine.certification.coverage_analyzer import (
    EvidenceCoverageAnalyzer,
    IncompleteEvidenceCoverageError,
)
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    AuditFinding,
    EvidenceClassification,
    EvidenceSourceType,
    EvidenceConfidence,
)


def _create_record(eid: str) -> EvidenceRecord:
    rec = EvidenceRecord(
        id=eid,
        collector="test_col",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        category="SecurityAndCompliance",
        summary="Test evidence",
        raw_payload={"status": "ok"},
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED,
    )
    rec = rec.model_copy(update={"content_hash": rec.calculate_hash()})
    return rec


def test_coverage_analyzer_complete_success():
    records = [_create_record("EV-100"), _create_record("EV-101")]
    findings = [
        AuditFinding(
            finding_id="FND-001",
            subsystem="Database",
            claim="Database encryption configured",
            classification=EvidenceClassification.VERIFIED,
            evidence_ids=["EV-100"],
            confidence=EvidenceConfidence.HIGH,
            analysis="Analysis details",
        ),
        AuditFinding(
            finding_id="FND-002",
            subsystem="Security",
            claim="RBAC security model enforced",
            classification=EvidenceClassification.VERIFIED,
            evidence_ids=["EV-101"],
            confidence=EvidenceConfidence.HIGH,
            analysis="Analysis details",
        ),
    ]

    result = EvidenceCoverageAnalyzer.verify_coverage(findings, records)
    assert result["is_complete"] is True
    assert result["coverage_pct"] == 100.0


def test_coverage_analyzer_missing_evidence_failure():
    records = [_create_record("EV-100")]
    findings = [
        AuditFinding(
            finding_id="FND-001",
            subsystem="Security",
            claim="Unbacked claim",
            classification=EvidenceClassification.VERIFIED,
            evidence_ids=["EV-999"],  # Non-existent ID
            confidence=EvidenceConfidence.HIGH,
            analysis="Analysis details",
        ),
    ]

    with pytest.raises(IncompleteEvidenceCoverageError):
        EvidenceCoverageAnalyzer.verify_coverage(findings, records)


def test_coverage_analyzer_tampered_hash_failure():
    rec = _create_record("EV-100")
    rec = rec.model_copy(update={"content_hash": "invalid_hash"})
    records = [rec]
    findings = [
        AuditFinding(
            finding_id="FND-001",
            subsystem="Security",
            claim="Tampered claim",
            classification=EvidenceClassification.VERIFIED,
            evidence_ids=["EV-100"],
            confidence=EvidenceConfidence.HIGH,
            analysis="Analysis details",
        ),
    ]

    with pytest.raises(IncompleteEvidenceCoverageError):
        EvidenceCoverageAnalyzer.verify_coverage(findings, records)
