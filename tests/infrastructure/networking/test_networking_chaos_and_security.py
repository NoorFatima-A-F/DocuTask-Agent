"""Chaos and Security Tests: Impersonation, Expired Certs, DNS Partitions, Policy Bypasses."""

import pytest
from app.infrastructure.networking.security import (
    SPIFFEIdentity,
    WorkloadIdentityManager,
    CertificateAuthorityManager,
    MTLSEngine,
    ZeroTrustPolicyEngine,
    ZeroTrustRule,
)
from app.infrastructure.networking.control_plane import ZeroTrustAction, CertificateStatus
from app.infrastructure.networking.sdk.network_sdk import NetworkSDK


def test_service_impersonation_rejection() -> None:
    sdk = NetworkSDK()

    # Deny all rule except for verified service account
    sdk.zero_trust_engine.add_rule(ZeroTrustRule(
        rule_id="strict-finance",
        name="Strict Finance Access",
        action=ZeroTrustAction.DENY,
        source_spiffe_pattern="spiffe://docutask.internal/ns/default/sa/untrusted-service",
        target_spiffe_pattern="spiffe://docutask.internal/ns/default/sa/finance-ledger",
        priority=10,
    ))

    res = sdk.secure_call(
        caller_service="untrusted-service",
        target_service="finance-ledger",
    )
    assert res.success is False
    assert res.status_code == 403
    assert "Zero-Trust Policy Denied" in res.error


def test_expired_certificate_rejection() -> None:
    ca_mgr = CertificateAuthorityManager()
    mtls = MTLSEngine(ca_mgr)

    # Issue cert with negative validity days (expired immediately)
    client_cert = ca_mgr.issue_workload_certificate("compromised-service", validity_days=-1)
    server_cert = ca_mgr.issue_workload_certificate("secure-vault", validity_days=30)

    res = mtls.validate_connection(client_cert, server_cert)
    assert res.is_valid is False
    assert "expired" in res.error_message.lower() or "invalid" in res.error_message.lower()


def test_mesh_network_partition_failover() -> None:
    sdk = NetworkSDK()

    # Register primary instance in failing zone
    inst_primary = sdk.register_service("storage-broker", host="10.0.1.10", port=443)
    # Register standby instance in secondary zone
    inst_secondary = sdk.register_service("storage-broker", host="10.0.2.20", port=443)

    # Primary crashes / fails health check
    sdk.discovery_registry.update_instance_health(inst_primary.instance_id, state=sdk.discovery_registry.get_instance(inst_primary.instance_id).health_state.UNHEALTHY)

    # Resolution should automatically bypass unhealthy instance
    resolved = sdk.resolve_service("storage-broker")
    assert resolved is not None
    assert resolved.host == "10.0.2.20"
