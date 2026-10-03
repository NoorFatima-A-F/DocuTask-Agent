"""Unit tests for Claim Truth Validation."""

import pytest
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
    AuditFinding,
)
from enterprise_audit_engine.governance.claim_validator import ClaimValidator, UnsupportedClaimError


def test_claim_validator_accepts_proven_claim():
    record = EvidenceRecord.create(
        category="Security",
        collector="SecurityCollector",
        source_type=EvidenceSourceType.RUNTIME_EXECUTION,
        summary="Zero secrets found in git history",
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED_BY_EXECUTION,
    )

    finding = AuditFinding(
        subsystem="Security",
        claim="Security subsystem verified through runtime scans",
        evidence_ids=[record.id],
        classification=EvidenceClassification.VERIFIED_BY_EXECUTION,
        confidence=EvidenceConfidence.HIGH,
        analysis="Valid runtime evidence attached.",
    )

    is_valid, msg = ClaimValidator.validate_claim(finding, [record])
    assert is_valid is True
    assert msg == "Valid"


def test_claim_validator_rejects_unprovable_hype():
    record = EvidenceRecord.create(
        category="Security",
        collector="SecurityCollector",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        summary="Static scan passed",
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED,
    )

    finding = AuditFinding(
        subsystem="Security",
        claim="System is 100% secure with no flaws",
        evidence_ids=[record.id],
        classification=EvidenceClassification.VERIFIED,
        confidence=EvidenceConfidence.HIGH,
        analysis="Marketing claim.",
    )

    is_valid, msg = ClaimValidator.validate_claim(finding, [record])
    assert is_valid is False
    assert "unprovable assertion" in msg


def test_claim_validator_blocks_runtime_claim_without_runtime_evidence():
    record = EvidenceRecord.create(
        category="API",
        collector="APICollector",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,  # NOT RUNTIME
        summary="Static endpoints parsed",
        confidence=EvidenceConfidence.MEDIUM,
        classification=EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS,
    )

    finding = AuditFinding(
        subsystem="API",
        claim="API fully verified in production execution",
        evidence_ids=[record.id],
        classification=EvidenceClassification.VERIFIED_BY_EXECUTION,
        confidence=EvidenceConfidence.VERY_HIGH,
        analysis="Claim exceeds evidence strength.",
    )

    is_valid, msg = ClaimValidator.validate_claim(finding, [record])
    assert is_valid is False
    assert "without RUNTIME_EXECUTION evidence" in msg


def test_validate_all_findings_raises_error():
    record = EvidenceRecord.create(
        category="AI",
        collector="AICollector",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        summary="AI routes exist",
        confidence=EvidenceConfidence.LOW,
        classification=EvidenceClassification.CONFIGURATION_PRESENT,
    )

    finding = AuditFinding(
        subsystem="AI",
        claim="System is 100% secure",
        evidence_ids=[record.id],
        classification=EvidenceClassification.VERIFIED,
        confidence=EvidenceConfidence.HIGH,
        analysis="Unsubstantiated.",
    )

    with pytest.raises(UnsupportedClaimError):
        ClaimValidator.validate_all_findings([finding], [record])
