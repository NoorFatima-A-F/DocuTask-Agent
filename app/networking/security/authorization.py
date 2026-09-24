"""Zero-Trust Authorization and Contextual Evaluation."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Set

from .policies import NetworkPolicyEngine, PolicyAction
from ..identity.service_identity import SPIFFEIdentity


@dataclass
class ZeroTrustSubject:
    spiffe_uri: str
    tenant_id: str = "system"
    roles: Set[str] = field(default_factory=lambda: {"service"})
    client_ip: str = "127.0.0.1"
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ZeroTrustResource:
    service_name: str
    namespace: str = "default"
    path: str = "/"
    action: str = "POST"
    resource_type: str = "service_endpoint"


@dataclass
class ZeroTrustDecision:
    allowed: bool
    reason: str
    risk_score: float = 0.0  # 0.0 (safest) to 1.0 (high risk)
    policy_action: PolicyAction = PolicyAction.DENY
    evaluated_at: float = field(default_factory=time.time)
    audit_id: str = field(default_factory=lambda: f"zt-eval-{uuid.uuid4().hex[:8]}")


class ZeroTrustEvaluator:
    """Evaluates requests against Zero-Trust RBAC/ABAC models and contextual risk."""

    def __init__(
        self,
        policy_engine: Optional[NetworkPolicyEngine] = None,
        max_allowed_risk_score: float = 0.7,
    ):
        self.policy_engine = policy_engine or NetworkPolicyEngine()
        self.max_allowed_risk_score = max_allowed_risk_score
        self._rbac_rules: Dict[str, Set[str]] = {}  # role -> allowed actions
        self._ip_blocklist: Set[str] = set()

    def block_ip(self, ip_address: str) -> None:
        self._ip_blocklist.add(ip_address)

    def allow_role_action(self, role: str, action: str) -> None:
        if role not in self._rbac_rules:
            self._rbac_rules[role] = set()
        self._rbac_rules[role].add(action)

    def calculate_risk_score(self, subject: ZeroTrustSubject, resource: ZeroTrustResource) -> float:
        """Calculate dynamic contextual risk score."""
        score = 0.0
        if subject.client_ip in self._ip_blocklist:
            return 1.0

        if subject.tenant_id == "anonymous":
            score += 0.4

        if "admin" in resource.path.lower() and "admin" not in subject.roles:
            score += 0.5

        if not subject.spiffe_uri.startswith("spiffe://"):
            score += 0.3

        return min(1.0, score)

    def evaluate(self, subject: ZeroTrustSubject, resource: ZeroTrustResource) -> ZeroTrustDecision:
        """Perform full zero-trust policy, RBAC, and risk evaluation."""
        # 1. Contextual Risk Check
        risk_score = self.calculate_risk_score(subject, resource)
        if risk_score > self.max_allowed_risk_score:
            return ZeroTrustDecision(
                allowed=False,
                reason=f"Contextual risk score ({risk_score:.2f}) exceeded threshold ({self.max_allowed_risk_score})",
                risk_score=risk_score,
                policy_action=PolicyAction.DENY,
            )

        # 2. Extract source identity
        try:
            spiffe = SPIFFEIdentity.parse(subject.spiffe_uri)
            src_service = spiffe.service_name
            src_ns = spiffe.namespace
        except Exception:
            src_service = "unknown"
            src_ns = "unknown"

        # 3. Network Policy Evaluation
        policy_action = self.policy_engine.evaluate(
            source_service=src_service,
            source_namespace=src_ns,
            target_service=resource.service_name,
            target_namespace=resource.namespace,
            method=resource.action,
            path=resource.path,
        )

        if policy_action == PolicyAction.DENY:
            return ZeroTrustDecision(
                allowed=False,
                reason="Denied by network communication policy",
                risk_score=risk_score,
                policy_action=PolicyAction.DENY,
            )

        # 4. RBAC Evaluation
        if self._rbac_rules:
            user_actions: Set[str] = set()
            for r in subject.roles:
                user_actions.update(self._rbac_rules.get(r, set()))
            if "*" not in user_actions and resource.action not in user_actions:
                return ZeroTrustDecision(
                    allowed=False,
                    reason=f"Role permission denied for action {resource.action}",
                    risk_score=risk_score,
                    policy_action=PolicyAction.DENY,
                )

        return ZeroTrustDecision(
            allowed=True,
            reason="Authorized by zero-trust policies",
            risk_score=risk_score,
            policy_action=policy_action,
        )
