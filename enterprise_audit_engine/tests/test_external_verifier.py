"""Tests for Standalone Zero-Dependency External Verifier."""

import pytest
import json
from enterprise_audit_engine.certification_authority.domain.models import CertificationRecord
from enterprise_audit_engine.certification_authority.signing.signer import CertificateSigner
from enterprise_audit_engine.external_verifier.standalone_verifier import StandaloneExternalVerifier


@pytest.fixture
def cert_files(tmp_path):
    cert = CertificationRecord.create_pending(
        certificate_id="CERT-EXT-001",
        system_name="DocuTask Agent",
        release_version="1.0.0",
        audit_engine_version="2.1.0",
        audit_execution_id="RUN-EXT-001",
        merkle_root="merkle_root_valid_hash_12345",
        evidence_root_hash="evidence_root_valid_hash_12345",
        eqi_score=95.0,
    )
    signed_cert, pub_key_pem = CertificateSigner.sign_certificate(cert)

    cert_path = tmp_path / "verification_certificate.json"
    pub_path = tmp_path / "public_key.pem"
    merkle_path = tmp_path / "audit_merkle_root.json"

    with open(cert_path, "w", encoding="utf-8") as fp:
        json.dump(signed_cert.model_dump(), fp, indent=2)

    pub_path.write_text(pub_key_pem, encoding="utf-8")

    with open(merkle_path, "w", encoding="utf-8") as fp:
        json.dump({"merkle_root": "merkle_root_valid_hash_12345"}, fp, indent=2)

    return cert_path, pub_path, merkle_path, signed_cert


def test_standalone_verifier_valid(cert_files):
    cert_path, pub_path, merkle_path, _ = cert_files
    res = StandaloneExternalVerifier.verify_standalone(
        certificate_path=cert_path,
        public_key_path=pub_path,
        merkle_path=merkle_path,
    )

    assert res["is_trusted"] is True
    assert res["status"] == "TRUSTED"
    assert res["signature_valid"] is True
    assert res["merkle_valid"] is True
    assert res["is_expired"] is False
    assert res["issues_count"] == 0


def test_standalone_verifier_tampered_payload(cert_files):
    cert_path, pub_path, merkle_path, signed_cert = cert_files

    # Modify eqi_score in certificate json file
    with open(cert_path, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    data["eqi_score"] = 99.9
    with open(cert_path, "w", encoding="utf-8") as fp:
        json.dump(data, fp)

    res = StandaloneExternalVerifier.verify_standalone(
        certificate_path=cert_path,
        public_key_path=pub_path,
        merkle_path=merkle_path,
    )

    assert res["is_trusted"] is False
    assert res["status"] == "REJECTED"
    assert res["signature_valid"] is False


def test_standalone_verifier_mismatched_merkle(cert_files):
    cert_path, pub_path, merkle_path, _ = cert_files

    # Tamper merkle manifest
    with open(merkle_path, "w", encoding="utf-8") as fp:
        json.dump({"merkle_root": "mismatched_merkle_root"}, fp)

    res = StandaloneExternalVerifier.verify_standalone(
        certificate_path=cert_path,
        public_key_path=pub_path,
        merkle_path=merkle_path,
    )

    assert res["is_trusted"] is False
    assert res["merkle_valid"] is False


def test_standalone_verifier_expired_certificate(cert_files):
    cert_path, pub_path, merkle_path, _ = cert_files

    with open(cert_path, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    data["expiry_timestamp"] = "2020-01-01T00:00:00+00:00"
    with open(cert_path, "w", encoding="utf-8") as fp:
        json.dump(data, fp)

    res = StandaloneExternalVerifier.verify_standalone(
        certificate_path=cert_path,
        public_key_path=pub_path,
        merkle_path=merkle_path,
    )

    assert res["is_trusted"] is False
    assert res["is_expired"] is True


def test_standalone_verifier_missing_file(tmp_path):
    res = StandaloneExternalVerifier.verify_standalone(tmp_path / "non_existent.json")
    assert res["is_trusted"] is False
    assert res["status"] == "FILE_NOT_FOUND"
