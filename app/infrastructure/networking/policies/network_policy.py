"""Declarative Network Policies and Policy Evaluation Engine."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import ipaddress
from typing import Dict, List
import threading

from ..control_plane.registry import NetworkPolicyType, ZeroTrustAction


@dataclass
class NetworkPolicyRule:
    """Ingress or Egress rule definition."""
    rule_id: str
    direction: NetworkPolicyType = NetworkPolicyType.INGRESS
    allowed_namespaces: List[str] = field(default_factory=lambda: ["*"])
    allowed_cidrs: List[str] = field(default_factory=list)  # e.g. ["10.0.0.0/8", "192.168.1.0/24"]
    allowed_ports: List[int] = field(default_factory=list)  # e.g. [443, 8080]
    allowed_protocols: List[str] = field(default_factory=lambda: ["https", "grpc"])
    action: ZeroTrustAction = ZeroTrustAction.ALLOW
    description: str = ""


@dataclass
class NetworkPolicy:
    """A scoped Network Policy document."""
    policy_id: str
    name: str
    target_service: str  # or "*"
    namespace: str = "default"
    policy_types: List[NetworkPolicyType] = field(default_factory=lambda: [NetworkPolicyType.INGRESS, NetworkPolicyType.EGRESS])
    ingress_rules: List[NetworkPolicyRule] = field(default_factory=list)
    egress_rules: List[NetworkPolicyRule] = field(default_factory=list)
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class NetworkPolicyEngine:
    """Central engine for evaluating declarative network policies."""

    def __init__(self) -> None:
        self._policies: Dict[str, NetworkPolicy] = {}
        self._lock = threading.RLock()

    def add_policy(self, policy: NetworkPolicy) -> None:
        """Register or update a network policy."""
        with self._lock:
            self._policies[policy.policy_id] = policy

    def remove_policy(self, policy_id: str) -> bool:
        """Remove a policy."""
        with self._lock:
            return self._policies.pop(policy_id, None) is not None

    def list_policies(self) -> List[NetworkPolicy]:
        """List all active policies."""
        with self._lock:
            return list(self._policies.values())

    def evaluate_traffic(
        self,
        direction: NetworkPolicyType,
        source_ip: str,
        dest_service: str,
        dest_namespace: str,
        dest_port: int,
        protocol: str = "https",
        source_namespace: str = "default",
    ) -> bool:
        """Evaluate whether traffic is allowed by network policies."""
        with self._lock:
            applicable = [
                p for p in self._policies.values()
                if p.is_active and (p.target_service in ("*", dest_service)) and p.namespace in ("*", dest_namespace)
            ]

        # If no policies target this service, default allow
        if not applicable:
            return True

        for policy in applicable:
            rules = policy.ingress_rules if direction == NetworkPolicyType.INGRESS else policy.egress_rules
            if not rules:
                continue

            for rule in rules:
                # Namespace check
                if "*" not in rule.allowed_namespaces and source_namespace not in rule.allowed_namespaces:
                    continue

                # Port check
                if rule.allowed_ports and dest_port not in rule.allowed_ports:
                    continue

                # Protocol check
                if rule.allowed_protocols and protocol.lower() not in [p.lower() for p in rule.allowed_protocols]:
                    continue

                # CIDR check
                if rule.allowed_cidrs:
                    if not self._check_cidr(source_ip, rule.allowed_cidrs):
                        continue

                return rule.action == ZeroTrustAction.ALLOW

        # If rules exist but none matched -> deny
        return False

    def _check_cidr(self, ip_str: str, cidrs: List[str]) -> bool:
        """Check if IP address falls within any allowed CIDR block."""
        try:
            ip_obj = ipaddress.ip_address(ip_str)
            for cidr in cidrs:
                if ip_obj in ipaddress.ip_network(cidr, strict=False):
                    return True
        except Exception:
            return False
        return False
