"""Ingress Policy Manager for namespace and tenant boundary enforcement."""

from typing import Dict, List, Optional
import threading

from .network_policy import NetworkPolicy, NetworkPolicyRule, NetworkPolicyEngine, NetworkPolicyType
from ..control_plane.registry import ZeroTrustAction


class IngressPolicyManager:
    """Manages East-West and North-South ingress traffic boundaries."""

    def __init__(self, engine: NetworkPolicyEngine) -> None:
        self.engine = engine
        self._tenant_namespaces: Dict[str, str] = {}  # tenant_id -> namespace
        self._lock = threading.RLock()

    def bind_tenant_namespace(self, tenant_id: str, namespace: str) -> None:
        """Bind a tenant ID to an isolated namespace."""
        with self._lock:
            self._tenant_namespaces[tenant_id] = namespace

    def create_tenant_isolation_policy(self, tenant_id: str, namespace: str) -> NetworkPolicy:
        """Create a strict ingress isolation policy for a tenant namespace."""
        policy = NetworkPolicy(
            policy_id=f"policy-tenant-ingress-{tenant_id}",
            name=f"Tenant Ingress Isolation: {tenant_id}",
            target_service="*",
            namespace=namespace,
            policy_types=[NetworkPolicyType.INGRESS],
            ingress_rules=[
                NetworkPolicyRule(
                    rule_id=f"rule-ingress-ns-{namespace}",
                    direction=NetworkPolicyType.INGRESS,
                    allowed_namespaces=[namespace, "system-ingress", "kube-system"],
                    allowed_ports=[443, 8080, 8443, 9090],
                    allowed_protocols=["https", "grpc"],
                    action=ZeroTrustAction.ALLOW,
                    description=f"Allow traffic only within {namespace} or from gateway",
                )
            ],
        )
        self.engine.add_policy(policy)
        return policy
