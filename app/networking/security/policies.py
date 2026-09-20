"""Network Communication Policies & Egress/Ingress Rules."""

from __future__ import annotations

import re
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class PolicyAction(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    AUDIT = "AUDIT"


@dataclass
class NetworkPolicyRule:
    rule_id: str
    source_service: str  # wildcard '*' supported
    source_namespace: str  # wildcard '*' supported
    target_service: str
    target_namespace: str = "default"
    allowed_methods: List[str] = field(default_factory=lambda: ["*"])
    allowed_paths: List[str] = field(default_factory=lambda: ["*"])
    action: PolicyAction = PolicyAction.ALLOW
    priority: int = 100  # Lower number = higher priority
    description: str = ""


@dataclass
class NetworkPolicy:
    policy_id: str
    name: str
    namespace: str = "default"
    default_action: PolicyAction = PolicyAction.DENY
    rules: List[NetworkPolicyRule] = field(default_factory=list)
    enabled: bool = True
    created_at: float = field(default_factory=time.time)


class NetworkPolicyEngine:
    """Evaluates ingress and egress traffic rules against defined mesh policies."""

    def __init__(self, default_action: PolicyAction = PolicyAction.DENY):
        self.default_action = default_action
        self._policies: Dict[str, NetworkPolicy] = {}

    def add_policy(self, policy: NetworkPolicy) -> None:
        self._policies[policy.policy_id] = policy

    def remove_policy(self, policy_id: str) -> bool:
        if policy_id in self._policies:
            del self._policies[policy_id]
            return True
        return False

    def get_policy(self, policy_id: str) -> Optional[NetworkPolicy]:
        return self._policies.get(policy_id)

    def list_policies(self, namespace: Optional[str] = None) -> List[NetworkPolicy]:
        if namespace:
            return [p for p in self._policies.values() if p.namespace == namespace]
        return list(self._policies.values())

    def evaluate(
        self,
        source_service: str,
        source_namespace: str,
        target_service: str,
        target_namespace: str,
        method: str = "POST",
        path: str = "/",
    ) -> PolicyAction:
        """Evaluate traffic against active policies, sorted by rule priority."""
        # Collect applicable active policies for the target namespace
        matching_policies = [
            p for p in self._policies.values()
            if p.enabled and (p.namespace == target_namespace or p.namespace == "*")
        ]

        if not matching_policies:
            return self.default_action

        # Collect all rules from matching policies
        all_rules: List[NetworkPolicyRule] = []
        for policy in matching_policies:
            all_rules.extend(policy.rules)

        # Sort by priority ascending (lower = higher priority)
        all_rules.sort(key=lambda r: r.priority)

        for rule in all_rules:
            if self._rule_matches(rule, source_service, source_namespace, target_service, target_namespace, method, path):
                return rule.action

        return self.default_action

    def _rule_matches(
        self,
        rule: NetworkPolicyRule,
        source_service: str,
        source_namespace: str,
        target_service: str,
        target_namespace: str,
        method: str,
        path: str,
    ) -> bool:
        # Match source
        if rule.source_service != "*" and rule.source_service != source_service:
            return False
        if rule.source_namespace != "*" and rule.source_namespace != source_namespace:
            return False

        # Match target
        if rule.target_service != "*" and rule.target_service != target_service:
            return False
        if rule.target_namespace != "*" and rule.target_namespace != target_namespace:
            return False

        # Match method
        if "*" not in rule.allowed_methods and method.upper() not in [m.upper() for m in rule.allowed_methods]:
            return False

        # Match path (regex/prefix pattern)
        if "*" not in rule.allowed_paths:
            matched_any_path = False
            for p_pattern in rule.allowed_paths:
                if p_pattern.endswith("*"):
                    prefix = p_pattern[:-1]
                    if path.startswith(prefix):
                        matched_any_path = True
                        break
                elif p_pattern == path:
                    matched_any_path = True
                    break
            if not matched_any_path:
                return False

        return True
