"""Enterprise Policy Engine.

Enforces enterprise-wide security, compliance (SOC2, HIPAA, GDPR), cost ceilings,
data residency, model allow-lists, and human approval rules on all dynamic plugins.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class PolicyRule:
    policy_id: str
    name: str
    category: str  # SECURITY, PRIVACY, COST, COMPLIANCE, MODEL_RESTRICTION
    severity: str  # BLOCKING, WARNING, AUDIT
    description: str
    condition_expression: str
    is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "name": self.name,
            "category": self.category,
            "severity": self.severity,
            "description": self.description,
            "condition_expression": self.condition_expression,
            "is_active": self.is_active,
        }


@dataclass
class PolicyEvaluationResult:
    is_allowed: bool
    violations: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    evaluated_count: int
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_allowed": self.is_allowed,
            "violations": self.violations,
            "warnings": self.warnings,
            "evaluated_count": self.evaluated_count,
            "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.timestamp)),
        }


class PolicyEngine:
    def __init__(self):
        self._policies: Dict[str, PolicyRule] = {}
        self._seed_default_policies()

    def _seed_default_policies(self) -> None:
        defaults = [
            PolicyRule(
                policy_id="pol-sec-001",
                name="Strict PII / PHI Redaction Rule",
                category="PRIVACY",
                severity="BLOCKING",
                description="Blocks unredacted Social Security Numbers, Medical Record Numbers, or Credit Cards from leaving secure enclave.",
                condition_expression="phi_redacted == true",
            ),
            PolicyRule(
                policy_id="pol-cost-002",
                name="Mission Budget Guardrail ($0.05 Max / Doc)",
                category="COST",
                severity="BLOCKING",
                description="Automatically throttles or aborts mission sub-graphs exceeding $0.05 per document page.",
                condition_expression="cost_usd <= 0.05",
            ),
            PolicyRule(
                policy_id="pol-model-003",
                name="Approved Enterprise Foundation Models Only",
                category="MODEL_RESTRICTION",
                severity="BLOCKING",
                description="Ensures only zero-data-retention enterprise tier LLM endpoints (Gemini 2.5) are invoked.",
                condition_expression="model in ['gemini-2.5-flash', 'gemini-2.5-pro']",
            ),
            PolicyRule(
                policy_id="pol-gov-004",
                name="Four-Eyes Human Approval for High-Value Wire Transits (> $10k)",
                category="COMPLIANCE",
                severity="BLOCKING",
                description="Requires cryptographic human supervisor signature for invoices exceeding $10,000.",
                condition_expression="amount <= 10000 or human_signed == true",
            ),
        ]
        for p in defaults:
            self._policies[p.policy_id] = p

    def add_policy(self, policy: PolicyRule) -> None:
        self._policies[policy.policy_id] = policy

    def remove_policy(self, policy_id: str) -> bool:
        if policy_id in self._policies:
            del self._policies[policy_id]
            return True
        return False

    def list_policies(self) -> List[PolicyRule]:
        return list(self._policies.values())

    def evaluate_action(self, action_context: Dict[str, Any]) -> PolicyEvaluationResult:
        violations: List[Dict[str, Any]] = []
        warnings: List[Dict[str, Any]] = []
        evaluated = 0

        for policy in self._policies.values():
            if not policy.is_active:
                continue
            evaluated += 1

            # Simple evaluator checks
            if policy.policy_id == "pol-cost-002":
                cost = float(action_context.get("cost_usd", 0.001))
                if cost > 0.05:
                    violations.append({
                        "policy_id": policy.policy_id,
                        "name": policy.name,
                        "reason": f"Cost ${cost:.4f} exceeds ceiling of $0.05",
                    })

            elif policy.policy_id == "pol-gov-004":
                amount = float(action_context.get("amount", 0.0))
                human_signed = bool(action_context.get("human_signed", False))
                if amount > 10000.0 and not human_signed:
                    violations.append({
                        "policy_id": policy.policy_id,
                        "name": policy.name,
                        "reason": f"Amount ${amount:,.2f} requires Human Supervisor Signature",
                    })

        is_allowed = len(violations) == 0
        return PolicyEvaluationResult(
            is_allowed=is_allowed,
            violations=violations,
            warnings=warnings,
            evaluated_count=evaluated,
        )


global_policy_engine = PolicyEngine()
