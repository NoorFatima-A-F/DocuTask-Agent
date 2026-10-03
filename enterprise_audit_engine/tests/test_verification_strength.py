"""Unit tests for Verification Strength Model."""

from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from enterprise_audit_engine.analyzers.verification_strength_model import VerificationStrengthModel


def test_verification_strength_insufficient():
    card = VerificationStrengthModel.evaluate_subsystem("AI", [])
    assert card.classification == EvidenceClassification.EVIDENCE_INSUFFICIENT
    assert card.total_score == 0.0
    assert card.confidence == EvidenceConfidence.NONE


def test_verification_strength_static_only():
    record = EvidenceRecord.create(
        category="AI",
        collector="AIPipelineCollector",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        summary="Static code exists",
        confidence=EvidenceConfidence.MEDIUM,
        classification=EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS,
    )

    card = VerificationStrengthModel.evaluate_subsystem("AI", [record])
    assert card.source_inspection_score == 20.0
    assert card.automated_tests_score == 0.0
    assert card.runtime_execution_score == 0.0
    assert card.classification == EvidenceClassification.EVIDENCE_INSUFFICIENT or card.classification == EvidenceClassification.PARTIALLY_VERIFIED


def test_verification_strength_full_stack():
    r1 = EvidenceRecord.create(
        category="API",
        collector="APICollector",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        summary="OpenAPI schema parsed",
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS,
    )
    r2 = EvidenceRecord.create(
        category="API",
        collector="TestingCollector",
        source_type=EvidenceSourceType.AUTOMATED_TEST_EXECUTION,
        summary="Integration tests passed with 0 exit code",
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED,
    )
    r3 = EvidenceRecord.create(
        category="API",
        collector="RuntimeCollector",
        source_type=EvidenceSourceType.RUNTIME_EXECUTION,
        summary="Uvicorn runtime verified live with health checks",
        confidence=EvidenceConfidence.VERY_HIGH,
        classification=EvidenceClassification.VERIFIED_BY_EXECUTION,
    )
    r4 = EvidenceRecord.create(
        category="SecurityAndCompliance",
        collector="SecurityCollector",
        source_type=EvidenceSourceType.RUNTIME_EXECUTION,
        summary="Zero secrets found in git history",
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED,
    )
    r5 = EvidenceRecord.create(
        category="API",
        collector="TestingCollector",
        source_type=EvidenceSourceType.CONFIGURATION_FILE,
        summary="Latency benchmark p95 < 200ms",
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED,
    )

    card = VerificationStrengthModel.evaluate_subsystem("API", [r1, r2, r3, r4, r5])
    assert card.total_score >= 90.0
    assert card.classification == EvidenceClassification.VERIFIED_BY_EXECUTION
    assert card.confidence == EvidenceConfidence.VERY_HIGH
