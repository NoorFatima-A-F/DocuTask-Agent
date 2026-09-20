"""Tests for Certification Policy Engine and Evidence Quality Index (EQI)."""

import pytest
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceSourceType,
    EvidenceClassification,
    EvidenceConfidence,
)
from enterprise_audit_engine.certification_authority.metrics.eqi_calculator import EvidenceQualityIndexCalculator
from enterprise_audit_engine.certification_authority.policy.policy_engine import CertificationPolicyEngine


def _create_record(eid: str, cat: str) -> EvidenceRecord:
    rec = EvidenceRecord(
        id=eid,
        collector="TestCollector",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        category=cat,
        summary=f"Evidence for {cat}",
        raw_payload={"status": "verified"},
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED,
    )
    return rec.model_copy(update={"content_hash": rec.calculate_hash()})


def test_eqi_calculator_enterprise_grade():
    records = [
        _create_record("EV-01", "Security"),
        _create_record("EV-02", "Database"),
        _create_record("EV-03", "Runtime"),
    ]

    eqi = EvidenceQualityIndexCalculator.calculate_eqi(
        records=records,
        coverage_pct=100.0,
        is_reproducible=True,
    )

    assert eqi.total_eqi >= 90.0
    assert eqi.rating == "ENTERPRISE_GRADE"
    assert eqi.evidence_coverage_score == 25.0
    assert eqi.reproducibility_score == 20.0
    assert eqi.integrity_score == 15.0


def test_certification_policy_engine_pass():
    records = [_create_record("EV-01", "Security"), _create_record("EV-02", "Runtime")]
    eqi = EvidenceQualityIndexCalculator.calculate_eqi(records, 100.0, True)

    eval_res = CertificationPolicyEngine.evaluate_policy(
        policy_name="enterprise_grade",
        overall_confidence="HIGH",
        overall_classification="VERIFIED",
        critical_findings=[],
        eqi=eqi,
        is_reproducible=True,
        active_domains=["runtime", "security", "testing", "reproducibility"],
        unsupported_claims_count=0,
    )

    assert eval_res["passed"] is True
    assert eval_res["violations_count"] == 0


def test_certification_policy_engine_fail_on_critical_finding():
    records = [_create_record("EV-01", "Security")]
    eqi = EvidenceQualityIndexCalculator.calculate_eqi(records, 100.0, True)

    eval_res = CertificationPolicyEngine.evaluate_policy(
        policy_name="enterprise_grade",
        overall_confidence="HIGH",
        overall_classification="CRITICAL_FINDING",
        critical_findings=["Critical finding: Unencrypted secret"],
        eqi=eqi,
        is_reproducible=True,
        active_domains=["runtime", "security", "testing", "reproducibility"],
    )

    assert eval_res["passed"] is False
    assert eval_res["violations_count"] >= 1
