"""Tests for Declarative Network Policies, Ingress, and Egress Isolation."""

import pytest
from app.infrastructure.networking.policies import (
    NetworkPolicy,
    NetworkPolicyRule,
    NetworkPolicyEngine,
    NetworkPolicyType,
    IngressPolicyManager,
    EgressPolicyManager,
)
from app.infrastructure.networking.control_plane import ZeroTrustAction


def test_network_policy_cidr_and_namespace_filtering() -> None:
    engine = NetworkPolicyEngine()

    policy = NetworkPolicy(
        policy_id="policy-ocr-ingress",
        name="OCR Ingress Policy",
        target_service="ocr-service",
        namespace="workers",
        ingress_rules=[
            NetworkPolicyRule(
                rule_id="r1",
                direction=NetworkPolicyType.INGRESS,
                allowed_namespaces=["ingestion", "system"],
                allowed_cidrs=["10.0.0.0/16"],
                allowed_ports=[8443],
                allowed_protocols=["https"],
                action=ZeroTrustAction.ALLOW,
            )
        ],
    )
    engine.add_policy(policy)

    # Allowed from matching namespace, CIDR, port, protocol
    assert engine.evaluate_traffic(
        direction=NetworkPolicyType.INGRESS,
        source_ip="10.0.1.50",
        dest_service="ocr-service",
        dest_namespace="workers",
        dest_port=8443,
        protocol="https",
        source_namespace="ingestion",
    ) is True

    # Denied due to disallowed source IP CIDR
    assert engine.evaluate_traffic(
        direction=NetworkPolicyType.INGRESS,
        source_ip="192.168.1.100",
        dest_service="ocr-service",
        dest_namespace="workers",
        dest_port=8443,
        protocol="https",
        source_namespace="ingestion",
    ) is False

    # Denied due to disallowed source namespace
    assert engine.evaluate_traffic(
        direction=NetworkPolicyType.INGRESS,
        source_ip="10.0.1.50",
        dest_service="ocr-service",
        dest_namespace="workers",
        dest_port=8443,
        protocol="https",
        source_namespace="untrusted-ns",
    ) is False


def test_egress_policy_manager() -> None:
    engine = NetworkPolicyEngine()
    egress_mgr = EgressPolicyManager(engine)

    assert egress_mgr.is_domain_allowed("api.openai.com") is True
    assert egress_mgr.is_domain_allowed("models.generativelanguage.googleapis.com") is True
    assert egress_mgr.is_domain_allowed("malicious-exfiltration.xyz") is False

    # Add custom allowed domain
    egress_mgr.allow_domain("custom-partner.corp")
    assert egress_mgr.is_domain_allowed("custom-partner.corp") is True
