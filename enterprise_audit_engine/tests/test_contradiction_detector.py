"""Tests for Certification Contradiction Detector."""

from enterprise_audit_engine.contradiction_detector.contradiction_detector import (
    ContradictionDetector,
    ContradictionReport,
)


def test_no_contradiction_clean():
    evidence = [
        {"id": "EV-1", "classification": "VERIFIED_BY_EXECUTION", "category": "Runtime"}
    ]
    claims = [
        {"claim": "System has basic runtime verification", "evidence_ids": ["EV-1"]}
    ]
    rep = ContradictionDetector.analyze_contradictions(evidence, claims)
    assert isinstance(rep, ContradictionReport)
    assert rep.has_contradictions is False
    assert rep.status == "NO_CONTRADICTIONS"
    assert rep.final_verdict == "CERTIFICATION_PERMITTED"


def test_detects_config_masquerading_as_runtime():
    evidence = [
        {"id": "EV-CFG-1", "classification": "CONFIGURATION_PRESENT", "category": "Config"}
    ]
    claims = [
        {"claim": "Database connection is runtime verified under load", "evidence_ids": ["EV-CFG-1"]}
    ]
    rep = ContradictionDetector.analyze_contradictions(evidence, claims)
    assert rep.has_contradictions is True
    assert rep.status == "CERTIFICATION_CONTRADICTION_FOUND"
    assert rep.final_verdict == "CERTIFICATION_REJECTED"
    assert rep.contradiction_count >= 1


def test_detects_insufficient_evidence_production_claim():
    evidence = [
        {"id": "EV-INSUF-1", "classification": "EVIDENCE_INSUFFICIENT", "category": "Security"}
    ]
    claims = [
        {"claim": "Application is production ready for high-security environments", "evidence_ids": ["EV-INSUF-1"]}
    ]
    rep = ContradictionDetector.analyze_contradictions(evidence, claims)
    assert rep.has_contradictions is True
    assert rep.final_verdict == "CERTIFICATION_REJECTED"


def test_detects_reality_check_failure():
    reality_failures = {
        "api": {"contradictions": ["/api/upload allows unauthenticated POST 200 OK"]},
        "db": {"contradictions": []},
        "security": {"vulnerabilities": ["SQL Injection escaped"]},
    }
    rep = ContradictionDetector.analyze_contradictions([], [], reality_failures)
    assert rep.has_contradictions is True
    assert rep.contradiction_count == 2
    assert rep.final_verdict == "CERTIFICATION_REJECTED"
