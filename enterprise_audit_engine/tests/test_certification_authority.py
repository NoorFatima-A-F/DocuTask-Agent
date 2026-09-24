"""End-to-End Tests for Certification Authority & Independent Verification."""

from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceSourceType,
    EvidenceClassification,
    EvidenceConfidence,
)
from enterprise_audit_engine.certification_authority.authority import CertificationAuthority
from enterprise_audit_engine.certification_authority.domain.models import CertificationStatus, RevocationReason


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


def test_certification_authority_issue_and_verify(tmp_path):
    authority = CertificationAuthority(repo_root=tmp_path, registry_dir=tmp_path / "registry")
    records = [
        _create_record("EV-01", "Security"),
        _create_record("EV-02", "Runtime"),
        _create_record("EV-03", "Testing"),
    ]

    issue_res = authority.issue_and_sign_certificate(
        audit_execution_id="RUN-20260921-0001",
        records=records,
        merkle_root="merkle_root_sha256_hash_12345678",
        overall_classification="VERIFIED",
        overall_confidence="HIGH",
        critical_findings=[],
        policy_name="enterprise_grade",
        release_version="1.0.0",
    )

    signed_record = issue_res["record"]
    assert signed_record.status == CertificationStatus.VALID
    assert signed_record.signature != ""
    assert signed_record.eqi_score >= 85.0

    # Save to disk
    cert_path = tmp_path / "certificate.json"
    import json
    with open(cert_path, "w", encoding="utf-8") as fp:
        json.dump(signed_record.model_dump(), fp)

    # Verify independently
    ver_res = authority.verify_certificate(certificate_path=cert_path)
    assert ver_res["is_valid"] is True
    assert ver_res["status"] == "CERTIFIED"
    assert ver_res["signature_valid"] is True


def test_certification_authority_revocation_flow(tmp_path):
    authority = CertificationAuthority(repo_root=tmp_path, registry_dir=tmp_path / "registry")
    records = [_create_record("EV-01", "Security")]

    issue_res = authority.issue_and_sign_certificate(
        audit_execution_id="RUN-20260921-0002",
        records=records,
        merkle_root="merkle_root_hash_999",
        overall_classification="VERIFIED",
        overall_confidence="HIGH",
        critical_findings=[],
        release_version="1.0.0",
    )
    signed_record = issue_res["record"]

    cert_path = tmp_path / "certificate.json"
    import json
    with open(cert_path, "w", encoding="utf-8") as fp:
        json.dump(signed_record.model_dump(), fp)

    # Initial verification: VALID
    assert authority.verify_certificate(certificate_path=cert_path)["is_valid"] is True

    # Revoke
    authority.revoke_certificate(
        certificate_id=signed_record.certificate_id,
        reason=RevocationReason.SECURITY_VULNERABILITY,
        details="Critical zero-day reported in dependency",
    )

    # Re-verify: MUST FAIL with REVOKED status
    rev_res = authority.verify_certificate(certificate_path=cert_path)
    assert rev_res["is_valid"] is False
    assert rev_res["status"] == "REVOKED"
    assert rev_res["is_revoked"] is True
