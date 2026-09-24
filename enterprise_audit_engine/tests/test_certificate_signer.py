"""Tests for Asymmetric Digital Signing and Verification (Ed25519)."""

from enterprise_audit_engine.certification_authority.domain.models import CertificationRecord, CertificationStatus
from enterprise_audit_engine.certification_authority.signing.signer import CertificateSigner
from enterprise_audit_engine.certification_authority.signing.verifier import CertificateSignatureVerifier


def test_ed25519_keypair_generation_and_export():
    private_key, public_key = CertificateSigner.generate_keypair()
    pub_pem = CertificateSigner.export_public_key_pem(public_key)
    priv_pem = CertificateSigner.export_private_key_pem(private_key)

    assert "BEGIN PUBLIC KEY" in pub_pem
    assert "BEGIN PRIVATE KEY" in priv_pem

    reloaded_priv = CertificateSigner.load_private_key_pem(priv_pem)
    assert reloaded_priv is not None


def test_certificate_signing_and_verification_success():
    record = CertificationRecord.create_pending(
        certificate_id="CERT-TEST-001",
        system_name="DocuTask Agent",
        release_version="1.0.0",
        audit_engine_version="2.1.0",
        audit_execution_id="RUN-TEST-01",
        merkle_root="a1b2c3d4e5f6" * 5,
        evidence_root_hash="a1b2c3d4e5f6" * 5,
        eqi_score=94.5,
    )

    signed_record, pub_key_pem = CertificateSigner.sign_certificate(record)
    assert signed_record.status == CertificationStatus.VALID
    assert signed_record.signature != ""
    assert signed_record.public_key_pem == pub_key_pem

    # Verify with embedded public key
    assert CertificateSignatureVerifier.verify_record_signature(signed_record) is True

    # Verify with external public key string
    assert CertificateSignatureVerifier.verify_record_signature(signed_record, pub_key_pem) is True


def test_certificate_signature_tamper_detection():
    record = CertificationRecord.create_pending(
        certificate_id="CERT-TEST-002",
        system_name="DocuTask Agent",
        release_version="1.0.0",
        audit_engine_version="2.1.0",
        audit_execution_id="RUN-TEST-02",
        merkle_root="1234567890abcdef" * 4,
        evidence_root_hash="1234567890abcdef" * 4,
        eqi_score=92.0,
    )

    signed_record, pub_key_pem = CertificateSigner.sign_certificate(record)

    # Tamper with eqi_score
    tampered_record = signed_record.model_copy(update={"eqi_score": 99.9})
    assert CertificateSignatureVerifier.verify_record_signature(tampered_record, pub_key_pem) is False

    # Tamper with merkle_root
    tampered_record2 = signed_record.model_copy(update={"merkle_root": "forged_root"})
    assert CertificateSignatureVerifier.verify_record_signature(tampered_record2, pub_key_pem) is False
