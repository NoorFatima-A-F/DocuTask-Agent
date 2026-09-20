"""Egress Policy Manager for restricting outbound platform calls."""

from typing import List, Optional
import threading

from .network_policy import NetworkPolicy, NetworkPolicyRule, NetworkPolicyEngine, NetworkPolicyType
from ..control_plane.registry import ZeroTrustAction


class EgressPolicyManager:
    """Restricts outbound calls to approved external APIs, AI providers, and storage."""

    def __init__(self, engine: NetworkPolicyEngine) -> None:
        self.engine = engine
        self._approved_domains: List[str] = [
            "api.openai.com",
            "generativelanguage.googleapis.com",
            "anthropic.com",
            "s3.amazonaws.com",
            "storage.googleapis.com",
        ]
        self._lock = threading.RLock()

    def allow_domain(self, domain: str) -> None:
        """Add domain to allowed egress destinations."""
        with self._lock:
            if domain not in self._approved_domains:
                self._approved_domains.append(domain)

    def is_domain_allowed(self, domain: str) -> bool:
        """Check if outbound destination domain is permitted."""
        with self._lock:
            for approved in self._approved_domains:
                if domain == approved or domain.endswith(f".{approved}"):
                    return True
            return False

    def create_strict_egress_policy(self, namespace: str = "default") -> NetworkPolicy:
        """Create egress restriction policy."""
        policy = NetworkPolicy(
            policy_id=f"policy-strict-egress-{namespace}",
            name=f"Strict Egress Restriction: {namespace}",
            target_service="*",
            namespace=namespace,
            policy_types=[NetworkPolicyType.EGRESS],
            egress_rules=[
                NetworkPolicyRule(
                    rule_id=f"rule-egress-{namespace}",
                    direction=NetworkPolicyType.EGRESS,
                    allowed_namespaces=[namespace, "system-egress", "kube-system"],
                    allowed_ports=[443, 8443],
                    allowed_protocols=["https", "grpc"],
                    action=ZeroTrustAction.ALLOW,
                    description="Allow outbound traffic only to approved secure ports",
                )
            ],
        )
        self.engine.add_policy(policy)
        return policy
