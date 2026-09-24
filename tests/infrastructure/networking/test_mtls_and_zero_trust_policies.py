"""Tests for mTLS Validation and Zero-Trust Policy Engine."""

from app.infrastructure.networking.security import (
    CertificateAuthorityManager,
    MTLSEngine,
    ZeroTrustPolicyEngine,
    ZeroTrustRule,
)
from app.infrastructure.networking.control_plane import ZeroTrustAction


def test_mtls_engine_validation() -> None:
    ca_mgr = CertificateAuthorityManager()
    mtls = MTLSEngine(ca_mgr)

    client_cert = ca_mgr.issue_workload_certificate("agent-service", namespace="default")
    server_cert = ca_mgr.issue_workload_certificate("workflow-service", namespace="default")

    # Valid connection
    res = mtls.validate_connection(
        client_cert=client_cert,
        server_cert=server_cert,
        expected_destination_spiffe=server_cert.san_spiffe_ids[0],
    )
    assert res.is_valid is True
    assert res.caller_spiffe_id == client_cert.san_spiffe_ids[0]

    # Invalid cipher suite
    res_bad_cipher = mtls.validate_connection(
        client_cert=client_cert,
        server_cert=server_cert,
        cipher_suite="DES-CBC3-SHA",
    )
    assert res_bad_cipher.is_valid is False
    assert "Disallowed cipher" in res_bad_cipher.error_message

    # Destination mismatch
    res_mismatch = mtls.validate_connection(
        client_cert=client_cert,
        server_cert=server_cert,
        expected_destination_spiffe="spiffe://docutask.internal/ns/default/sa/wrong-service",
    )
    assert res_mismatch.is_valid is False
    assert "mismatch" in res_mismatch.error_message


def test_zero_trust_policy_engine_default_deny_and_matching() -> None:
    zt = ZeroTrustPolicyEngine()

    caller = "spiffe://docutask.internal/ns/default/sa/frontend"
    target = "spiffe://docutask.internal/ns/default/sa/backend"

    # Default deny
    res_deny = zt.evaluate(caller, target, method="GET", path="/api/v1/documents")
    assert res_deny.action == ZeroTrustAction.DENY
    assert res_deny.is_allowed is False

    # Add specific allow rule
    zt.add_rule(ZeroTrustRule(
        rule_id="r1",
        name="Allow Frontend to Backend",
        action=ZeroTrustAction.ALLOW,
        source_spiffe_pattern=caller,
        target_spiffe_pattern=target,
        allowed_methods=["GET", "POST"],
        allowed_paths=["/api/v1/documents/*"],
        tenant_scope=["tenant-01"],
    ))

    # Test allowed call matching tenant
    res_allow = zt.evaluate(caller, target, method="GET", path="/api/v1/documents/123", tenant_id="tenant-01")
    assert res_allow.action == ZeroTrustAction.ALLOW
    assert res_allow.is_allowed is True

    # Test disallowed tenant
    res_wrong_tenant = zt.evaluate(caller, target, method="GET", path="/api/v1/documents/123", tenant_id="tenant-02")
    assert res_wrong_tenant.action == ZeroTrustAction.DENY

    # Test disallowed HTTP method
    res_wrong_method = zt.evaluate(caller, target, method="DELETE", path="/api/v1/documents/123", tenant_id="tenant-01")
    assert res_wrong_method.action == ZeroTrustAction.DENY
