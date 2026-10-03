"""Tests for Audit Registry, History Regression Detector, and Revocation Registry."""

from enterprise_audit_engine.certification_authority.domain.models import (
    CertificationRecord,
    RevocationReason,
)
from enterprise_audit_engine.certification_authority.registry.audit_registry import AuditRegistry
from enterprise_audit_engine.certification_authority.registry.regression_detector import AuditRegressionDetector
from enterprise_audit_engine.certification_authority.registry.revocation_registry import CertificationRevocationRegistry


def _create_cert(cert_id: str, ver: str, eqi: float, crit_findings: list = None) -> CertificationRecord:
    return CertificationRecord.create_pending(
        certificate_id=cert_id,
        system_name="DocuTask Agent",
        release_version=ver,
        audit_engine_version="2.1.0",
        audit_execution_id="RUN-01",
        merkle_root="abc" * 10,
        evidence_root_hash="def" * 10,
        eqi_score=eqi,
        critical_findings=crit_findings or [],
    )


def test_audit_registry_lifecycle(tmp_path):
    registry = AuditRegistry(tmp_path)
    cert1 = _create_cert("CERT-001", "1.0.0", 92.0)
    cert2 = _create_cert("CERT-002", "1.1.0", 95.0)

    registry.register_certificate(cert1)
    registry.register_certificate(cert2)

    versions = registry.list_versions()
    assert "1.0.0" in versions
    assert "1.1.0" in versions

    loaded = registry.get_certificate("1.0.0")
    assert loaded is not None
    assert loaded.certificate_id == "CERT-001"
    assert loaded.eqi_score == 92.0


def test_audit_regression_detector_improvement():
    cert1 = _create_cert("CERT-001", "1.0.0", 90.0, ["Minor critical finding"])
    cert2 = _create_cert("CERT-002", "1.1.0", 96.0, [])  # Resolved critical finding!

    diff = AuditRegressionDetector.compare_certifications(cert1, cert2)
    assert diff["has_regression"] is False
    assert diff["eqi_delta"] == 6.0
    assert diff["critical_findings_delta"] == -1


def test_audit_regression_detector_detects_regression():
    cert1 = _create_cert("CERT-001", "1.0.0", 95.0, [])
    cert2 = _create_cert("CERT-002", "1.1.0", 82.0, ["New critical finding"])

    diff = AuditRegressionDetector.compare_certifications(cert1, cert2)
    assert diff["has_regression"] is True
    assert diff["regressions_count"] >= 2


def test_revocation_registry_lifecycle(tmp_path):
    crl = CertificationRevocationRegistry(tmp_path)
    assert crl.is_revoked("CERT-001") is False

    crl.revoke_certificate(
        certificate_id="CERT-001",
        reason=RevocationReason.EVIDENCE_TAMPERING,
        details="Discovered tampered database record",
    )

    assert crl.is_revoked("CERT-001") is True
    rev = crl.get_revocation("CERT-001")
    assert rev is not None
    assert rev.reason == RevocationReason.EVIDENCE_TAMPERING
