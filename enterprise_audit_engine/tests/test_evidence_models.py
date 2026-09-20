"""Unit tests for Evidence Domain Models & Immutability."""

import pytest
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)


def test_evidence_record_creation_and_hashing():
    record = EvidenceRecord.create(
        category="Security",
        collector="TestCollector",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        summary="No secrets found in repository",
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS,
    )

    assert record.id.startswith("EV-")
    assert len(record.content_hash) == 64  # Valid SHA-256
    assert record.category == "Security"
    assert record.confidence == EvidenceConfidence.HIGH
    assert record.classification == EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS


def test_evidence_record_immutability():
    record = EvidenceRecord.create(
        category="Testing",
        collector="TestCollector",
        source_type=EvidenceSourceType.AUTOMATED_TEST_EXECUTION,
        summary="Pytest suite passed",
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED,
    )

    # Pydantic v2 frozen model raises ValidationError on mutation attempt
    with pytest.raises(Exception):
        record.summary = "Tampered summary"
