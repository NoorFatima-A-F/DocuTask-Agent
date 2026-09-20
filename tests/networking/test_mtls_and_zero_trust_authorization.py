"""Tests for mTLS 1.3 Handshake and Zero-Trust Authorization Engine."""

import pytest
from app.networking.identity.certificates import CertificateManager
from app.networking.security.authorization import (
    ZeroTrustDecision,
    ZeroTrustEvaluator,
    ZeroTrustResource,
    ZeroTrustSubject,
)
from app.networking.security.mtls import (
    MTLSManager,
    MTLSMode,
    TLSVersion,
)
from app.networking.security.policies import (
    NetworkPolicy,
    NetworkPolicyEngine,
    NetworkPolicyRule,
    PolicyAction,
)


def test_mtls_handshake_strict_and_permissive():
    cert_mgr = CertificateManager()
    mtls_mgr = MTLSManager(cert_manager=cert_mgr)

    client_cert = cert_mgr.issue_certificate("CN=client", ["spiffe://docutask.internal/ns/default/sa/client"])
    server_cert = cert_mgr.issue_certificate("CN=server", ["spiffe://docutask.internal/ns/default/sa/server"])

    # Strict handshake success
    res_ok = mtls_mgr.perform_handshake(
        client_cert_serial=client_cert.serial_number,
        server_cert_serial=server_cert.serial_number,
        mode=MTLSMode.STRICT,
    )
    assert res_ok.success is True
    assert res_ok.session is not None
    assert res_ok.session.cipher_suite == "TLS_AES_256_GCM_SHA384"

    # Strict handshake failure with invalid client cert
    res_fail = mtls_mgr.perform_handshake(
        client_cert_serial="invalid-serial",
        server_cert_serial=server_cert.serial_number,
        mode=MTLSMode.STRICT,
    )
    assert res_fail.success is False

    # Permissive handshake success with invalid client cert
    res_perm = mtls_mgr.perform_handshake(
        client_cert_serial="invalid-serial",
        server_cert_serial=server_cert.serial_number,
        mode=MTLSMode.PERMISSIVE,
    )
    assert res_perm.success is True


def test_zero_trust_policy_and_risk_evaluation():
    policy_engine = NetworkPolicyEngine(default_action=PolicyAction.DENY)
    evaluator = ZeroTrustEvaluator(policy_engine=policy_engine)

    # 1. Without policies, default action is DENY
    subject = ZeroTrustSubject(
        spiffe_uri="spiffe://docutask.internal/ns/frontend/sa/web-client",
        roles={"user"},
    )
    resource = ZeroTrustResource(
        service_name="payment-service",
        namespace="banking",
        path="/charge",
        action="POST",
    )
    decision = evaluator.evaluate(subject, resource)
    assert decision.allowed is False
    assert decision.policy_action == PolicyAction.DENY

    # 2. Add an ALLOW rule
    rule = NetworkPolicyRule(
        rule_id="allow-frontend-to-payment",
        source_service="web-client",
        source_namespace="frontend",
        target_service="payment-service",
        target_namespace="banking",
        allowed_methods=["POST"],
        allowed_paths=["/charge"],
        action=PolicyAction.ALLOW,
    )
    policy = NetworkPolicy(
        policy_id="policy-payment",
        name="payment-ingress",
        namespace="banking",
        rules=[rule],
    )
    policy_engine.add_policy(policy)

    decision2 = evaluator.evaluate(subject, resource)
    assert decision2.allowed is True
    assert decision2.policy_action == PolicyAction.ALLOW

    # 3. Test blocked IP triggering risk denial
    evaluator.block_ip("192.168.1.100")
    bad_subject = ZeroTrustSubject(
        spiffe_uri="spiffe://docutask.internal/ns/frontend/sa/web-client",
        client_ip="192.168.1.100",
    )
    bad_decision = evaluator.evaluate(bad_subject, resource)
    assert bad_decision.allowed is False
    assert bad_decision.risk_score == 1.0
