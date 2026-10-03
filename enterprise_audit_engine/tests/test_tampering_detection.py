"""Unit tests for Evidence Tampering Detection & Integrity Verification."""

from pathlib import Path
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
    AuditReportManifest,
)
from enterprise_audit_engine.governance.integrity_verifier import EvidenceIntegrityVerifier
from enterprise_audit_engine.storage.evidence_store import EvidenceStore


def test_integrity_verifier_detects_valid_record():
    record = EvidenceRecord.create(
        category="API",
        collector="APICollector",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        summary="All API endpoints verified",
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS,
    )

    is_valid, msg = EvidenceIntegrityVerifier.verify_record_integrity(record)
    assert is_valid is True
    assert msg == "Valid"


def test_integrity_verifier_detects_tampered_record():
    record = EvidenceRecord.create(
        category="AI",
        collector="AIPipelineCollector",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        summary="Original summary",
        confidence=EvidenceConfidence.MEDIUM,
        classification=EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS,
    )

    # Simulate tampered record with mismatching content_hash
    tampered = record.model_copy(update={"summary": "Hacked summary"})
    is_valid, msg = EvidenceIntegrityVerifier.verify_record_integrity(tampered)
    assert is_valid is False
    assert "mismatch" in msg.lower()


def test_store_integrity_audit(tmp_path: Path):
    store = EvidenceStore(tmp_path)
    record1 = EvidenceRecord.create(
        category="Database",
        collector="DatabaseCollector",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        summary="DB models verified",
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED,
    )
    store.save_evidence(record1)

    manifest = AuditReportManifest(
        run_id="RUN-TEST-001",
        total_evidence_collected=1,
        findings_count=1,
        evidence_hashes=[record1.content_hash],
    )

    res = EvidenceIntegrityVerifier.verify_store_integrity(tmp_path, manifest)
    assert res["is_intact"] is True
    assert res["valid_count"] == 1
    assert res["tampered_count"] == 0
