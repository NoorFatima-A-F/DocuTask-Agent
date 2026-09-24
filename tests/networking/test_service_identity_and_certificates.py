"""Tests for Service Identity, SPIFFE IDs, and Multi-Backend Certificate Management."""

import pytest
from app.networking.identity.certificates import (
    CertificateBackend,
    CertificateManager,
)
from app.networking.identity.service_identity import (
    ServiceIdentityManager,
    SPIFFEIdentity,
)
from app.networking.identity.workload import (
    SVIDType,
    WorkloadAttestationManager,
)


def test_spiffe_identity_formatting_and_parsing():
    spiffe = SPIFFEIdentity(
        trust_domain="docutask.internal",
        namespace="compliance",
        service_name="audit-logger",
    )
    assert spiffe.uri == "spiffe://docutask.internal/ns/compliance/sa/audit-logger"

    parsed = SPIFFEIdentity.parse("spiffe://prod.cluster/ns/ai/sa/llm-worker")
    assert parsed.trust_domain == "prod.cluster"
    assert parsed.namespace == "ai"
    assert parsed.service_name == "llm-worker"

    with pytest.raises(ValueError):
        SPIFFEIdentity.parse("invalid-format")


def test_service_identity_minting_and_revocation():
    mgr = ServiceIdentityManager(default_trust_domain="docutask.internal")
    ident = mgr.mint_identity(
        service_name="billing-service",
        namespace="finance",
        tenant_id="tenant-acme",
        roles={"billing_admin", "service"},
    )
    assert ident.spiffe_id.uri == "spiffe://docutask.internal/ns/finance/sa/billing-service"
    assert ident.is_valid is True

    # Validate
    assert mgr.validate_identity(ident.spiffe_id.uri) is True

    # Revoke
    assert mgr.revoke_identity(ident.spiffe_id.uri) is True
    assert mgr.validate_identity(ident.spiffe_id.uri) is False


def test_certificate_issuance_and_rotation():
    cert_mgr = CertificateManager(backend=CertificateBackend.IN_MEMORY)
    assert cert_mgr.root_ca is not None
    assert cert_mgr.root_ca.is_ca is True

    # Issue leaf certificate
    leaf = cert_mgr.issue_certificate(
        subject="CN=worker.default.svc.docutask.internal",
        san_uris=["spiffe://docutask.internal/ns/default/sa/worker"],
        validity_seconds=3600.0,
    )
    assert leaf.is_active is True
    assert cert_mgr.verify_certificate(leaf.serial_number, expected_san="spiffe://docutask.internal/ns/default/sa/worker") is True

    # Rotate
    rotated = cert_mgr.rotate_certificate(leaf.serial_number)
    assert rotated is not None
    assert rotated.serial_number != leaf.serial_number
    assert leaf.revoked is True
    assert rotated.is_active is True


def test_workload_attestation_and_svid_validation():
    cert_mgr = CertificateManager()
    attest_mgr = WorkloadAttestationManager(cert_manager=cert_mgr)

    # Issue X509 SVID
    svid_x509 = attest_mgr.attest_workload(
        service_name="ocr-pipeline",
        namespace="processing",
        svid_type=SVIDType.X509,
    )
    assert svid_x509.svid_type == SVIDType.X509
    assert attest_mgr.validate_svid(svid_x509.token_or_serial) is True

    # Issue JWT SVID
    svid_jwt = attest_mgr.attest_workload(
        service_name="ocr-pipeline",
        namespace="processing",
        svid_type=SVIDType.JWT,
    )
    assert svid_jwt.svid_type == SVIDType.JWT
    assert attest_mgr.validate_svid(svid_jwt.token_or_serial) is True
