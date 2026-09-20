"""Zero-Trust Policy Engine, Identity Verification, and Runtime Authorization."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
import threading

from ..control_plane.registry import ZeroTrustAction


@dataclass
class ZeroTrustRule:
    """A granular Zero-Trust authorization rule."""
    rule_id: str
    name: str
    action: ZeroTrustAction = ZeroTrustAction.ALLOW
    source_spiffe_pattern: str = "*"  # e.g. "spiffe://docutask.internal/ns/default/sa/*"
    target_spiffe_pattern: str = "*"  # e.g. "spiffe://docutask.internal/ns/default/sa/document-processor"
    allowed_methods: List[str] = field(default_factory=lambda: ["*"])
    allowed_paths: List[str] = field(default_factory=lambda: ["/*"])
    tenant_scope: List[str] = field(default_factory=lambda: ["*"])
    priority: int = 100
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ZeroTrustEvaluationResult:
    """Decision output of Zero-Trust evaluation."""
    action: ZeroTrustAction
    matched_rule_id: Optional[str] = None
    reason: str = "default_deny"
    caller_spiffe: str = ""
    target_spiffe: str = ""
    tenant_id: Optional[str] = None
    evaluated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def is_allowed(self) -> bool:
        """True if action is ALLOW."""
        return self.action == ZeroTrustAction.ALLOW


class ZeroTrustPolicyEngine:
    """Enforces default-deny Zero-Trust authorization across all service calls."""

    def __init__(self) -> None:
        self._rules: Dict[str, ZeroTrustRule] = {}
        self._lock = threading.RLock()

    def add_rule(self, rule: ZeroTrustRule) -> None:
        """Register or update a Zero-Trust rule."""
        with self._lock:
            self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule by ID."""
        with self._lock:
            return self._rules.pop(rule_id, None) is not None

    def list_rules(self) -> List[ZeroTrustRule]:
        """List active rules sorted by priority (lowest number = highest priority)."""
        with self._lock:
            return sorted(self._rules.values(), key=lambda r: r.priority)

    def evaluate(
        self,
        caller_spiffe: str,
        target_spiffe: str,
        method: str = "GET",
        path: str = "/",
        tenant_id: Optional[str] = None,
    ) -> ZeroTrustEvaluationResult:
        """Evaluate request context against Zero-Trust policies with default DENY."""
        with self._lock:
            rules = self.list_rules()

        for rule in rules:
            if not rule.is_active:
                continue

            # Match source SPIFFE
            if not self._pattern_match(rule.source_spiffe_pattern, caller_spiffe):
                continue

            # Match target SPIFFE
            if not self._pattern_match(rule.target_spiffe_pattern, target_spiffe):
                continue

            # Match HTTP Method
            if "*" not in rule.allowed_methods and method.upper() not in [m.upper() for m in rule.allowed_methods]:
                continue

            # Match Path prefix
            if not self._path_match(rule.allowed_paths, path):
                continue

            # Match Tenant scope
            if tenant_id and "*" not in rule.tenant_scope and tenant_id not in rule.tenant_scope:
                continue

            # Match found! Return rule decision
            return ZeroTrustEvaluationResult(
                action=rule.action,
                matched_rule_id=rule.rule_id,
                reason=f"Matched rule: {rule.name}",
                caller_spiffe=caller_spiffe,
                target_spiffe=target_spiffe,
                tenant_id=tenant_id,
            )

        # Default Deny
        return ZeroTrustEvaluationResult(
            action=ZeroTrustAction.DENY,
            reason="No matching Zero-Trust rule found (Default Deny)",
            caller_spiffe=caller_spiffe,
            target_spiffe=target_spiffe,
            tenant_id=tenant_id,
        )

    def _pattern_match(self, pattern: str, value: str) -> bool:
        """Wildcard string pattern matching."""
        if pattern == "*" or pattern == value:
            return True
        if pattern.endswith("*"):
            prefix = pattern[:-1]
            return value.startswith(prefix)
        return False

    def _path_match(self, allowed_paths: List[str], path: str) -> bool:
        """Match request path against allowed path prefixes."""
        if "/*" in allowed_paths or "*" in allowed_paths:
            return True
        for ap in allowed_paths:
            if ap.endswith("/*") and path.startswith(ap[:-2]):
                return True
            if ap == path or path.startswith(ap):
                return True
        return False
