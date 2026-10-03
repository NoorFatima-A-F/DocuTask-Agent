"""Tests for ERI Calculator & Composite Trust Score System."""

from enterprise_audit_engine.trust_metrics.eri_calculator import (
    EvidenceReliabilityIndexCalculator,
    EvidenceReliabilityReport,
)
from enterprise_audit_engine.trust_metrics.trust_score import (
    TrustScoreCalculator,
    EvidenceTrustScore,
)


def test_eri_calculator_high_trust():
    evidence = [
        {"id": "EV-1", "category": "RuntimeExecution", "confidence": "HIGH", "raw_payload": {"ok": True}, "content_hash": "abc"},
        {"id": "EV-2", "category": "AutomatedTesting", "confidence": "HIGH", "raw_payload": {"ok": True}, "content_hash": "def"},
    ]
    rep = EvidenceReliabilityIndexCalculator.calculate_eri(
        evidence_items=evidence,
        reality_checks_passed=True,
        reproducibility_passed=True,
        drift_detected=False,
    )

    assert isinstance(rep, EvidenceReliabilityReport)
    assert rep.eri_score >= 80.0
    assert rep.is_acceptable_for_enterprise is True
    assert rep.classification in {"HIGH_TRUST_EVIDENCE", "COMMERCIAL_TRUST_EVIDENCE"}


def test_eri_calculator_untrusted_on_drift_and_failure():
    evidence = [
        {"id": "EV-1", "category": "Config", "confidence": "LOW", "raw_payload": {}, "content_hash": ""}
    ]
    rep = EvidenceReliabilityIndexCalculator.calculate_eri(
        evidence_items=evidence,
        reality_checks_passed=False,
        reproducibility_passed=False,
        drift_detected=True,
    )

    assert rep.is_acceptable_for_enterprise is False
    assert rep.classification == "EVIDENCE_UNTRUSTED"


def test_trust_score_calculation_certified():
    reality_res = {
        "api": {"is_valid": True},
        "db": {"is_valid": True},
    }
    sec_res = {"defense_rate_percentage": 100.0}

    score = TrustScoreCalculator.calculate_trust_score(
        target_system="DocuTask Agent",
        target_version="1.0.0",
        integrity_valid=True,
        reality_result=reality_res,
        security_result=sec_res,
        reproducibility_deterministic=True,
        auditor_consensus_score=94.0,
        has_contradictions=False,
    )

    assert isinstance(score, EvidenceTrustScore)
    assert score.overall_trust_score >= 90.0
    assert score.trust_level == "ENTERPRISE_VERIFIED"
    assert score.is_certified is True


def test_trust_score_rejection_on_contradiction():
    reality_res = {"api": {"is_valid": True}, "db": {"is_valid": True}}
    sec_res = {"defense_rate_percentage": 100.0}

    score = TrustScoreCalculator.calculate_trust_score(
        target_system="DocuTask Agent",
        target_version="1.0.0",
        integrity_valid=True,
        reality_result=reality_res,
        security_result=sec_res,
        reproducibility_deterministic=True,
        auditor_consensus_score=90.0,
        has_contradictions=True,
    )

    assert score.trust_level == "UNVERIFIED_REJECTED"
    assert score.is_certified is False
