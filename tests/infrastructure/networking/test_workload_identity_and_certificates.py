"""Tests for Workload Identity (SPIFFE/SVID) and Certificate Authority Lifecycle."""

import pytest
from app.infrastructure.networking.security import (
    SPIFFEIdentity,
    WorkloadIdentityManager,
    CertificateAuthorityManager,
)
from app.infrastructure.networking.control_plane import CertificateStatus


def test_spiffe_identity_parsing_and_svid_lifecycle() -> None:
    id_mgr = WorkloadIdentityManager(trust_domain="docutask.internal")

    ident = id_mgr.create_identity(namespace="prod-ai", service_account="llm-orchestrator")
    assert ident.raw_spiffe_id == "spiffe://docutask.internal/ns/prod-ai/sa/llm-orchestrator"

    # Issue SVID
    svid = id_mgr.issue_svid(ident, ttl_seconds=3600)
    assert svid.token is not None
    assert svid.is_expired is False

    # Verify valid SVID
    verified = id_mgr.verify_svid(svid.token)
    assert verified is not None
    assert verified.spiffe_id.service_account == "llm-orchestrator"
    assert verified.spiffe_id.namespace == "prod-ai"

    # Verify corrupted token
    corrupted_token = svid.token[:-5] + "12345"
    assert id_mgr.verify_svid(corrupted_token) is None


def test_ca_manager_issuance_rotation_and_revocation() -> None:
    ca_mgr = CertificateAuthorityManager(trust_domain="docutask.internal")
    assert ca_mgr.root_ca.status == CertificateStatus.ACTIVE

    # Issue workload cert
    cert = ca_mgr.issue_workload_certificate("doc-parser", namespace="default", validity_days=30)
    assert cert.subject_cn == "doc-parser.default"
    assert cert.serial_number is not None
    assert ca_mgr.is_certificate_valid(cert.serial_number) is True

    # Rotate cert
    rotated_cert = ca_mgr.rotate_certificate(cert.serial_number)
    assert rotated_cert is not None
    assert rotated_cert.serial_number != cert.serial_number
    # Old cert should now be revoked
    assert ca_mgr.is_certificate_valid(cert.serial_number) is False
    assert ca_mgr.is_certificate_valid(rotated_cert.serial_number) is True

    # Explicit revocation
    ca_mgr.revoke_certificate(rotated_cert.serial_number)
    assert ca_mgr.is_certificate_valid(rotated_cert.serial_number) is False

    # Trust bundle check
    bundle = ca_mgr.get_trust_bundle()
    assert bundle["trust_domain"] == "docutask.internal"
    assert bundle["revoked_serials_count"] == 2
