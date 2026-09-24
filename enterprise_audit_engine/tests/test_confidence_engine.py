"""Unit tests for Deterministic Confidence & Maturity Engine."""

from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from enterprise_audit_engine.analyzers.confidence_engine import ConfidenceEngine


def test_confidence_calculation_runtime():
    record = EvidenceRecord.create(
        category="Runtime",
        collector="RuntimeCollector",
        source_type=EvidenceSourceType.RUNTIME_EXECUTION,
        summary="Container healthcheck 200 OK",
        confidence=EvidenceConfidence.VERY_HIGH,
        classification=EvidenceClassification.VERIFIED_BY_EXECUTION,
    )
    confidence = ConfidenceEngine.calculate_confidence([record])
    assert confidence == EvidenceConfidence.VERY_HIGH


def test_confidence_calculation_static_plus_tests():
    r1 = EvidenceRecord.create(
        category="API",
        collector="SourceAnalyzer",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        summary="FastAPI routes valid",
        confidence=EvidenceConfidence.MEDIUM,
        classification=EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS,
    )
    r2 = EvidenceRecord.create(
        category="API",
        collector="TestingCollector",
        source_type=EvidenceSourceType.AUTOMATED_TEST_EXECUTION,
        summary="TestClient passed",
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED,
    )
    confidence = ConfidenceEngine.calculate_confidence([r1, r2])
    assert confidence == EvidenceConfidence.HIGH


def test_subsystem_classification_with_critical_finding():
    r1 = EvidenceRecord.create(
        category="Security",
        collector="SecurityCollector",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        summary="Exposed live API key",
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.CRITICAL_FINDING,
    )
    classification = ConfidenceEngine.classify_subsystem([r1])
    assert classification == EvidenceClassification.CRITICAL_FINDING
