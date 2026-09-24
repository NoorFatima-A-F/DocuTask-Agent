"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Agent Policy Engine.
Governs agent actions before execution, enforcing tool access boundaries,
model restrictions, data privacy, and compliance policies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import logging

from app.agents.domain.agent_entity import Agent

logger = logging.getLogger(__name__)


@dataclass
class PolicyEvaluationResult:
    """Verdict of a pre-action policy check."""
    is_allowed: bool = True
    action: str = ""
    resource: str = ""
    violations: List[str] = field(default_factory=list)
    applied_policies: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_allowed": self.is_allowed,
            "action": self.action,
            "resource": self.resource,
            "violations": self.violations,
            "applied_policies": self.applied_policies,
            "timestamp": self.timestamp.isoformat(),
        }


class AgentPolicyEngine:
    """
    Evaluates actions attempted by autonomous agents against organizational
    policy rules (budget, tool authorization, memory access, privacy).
    """

    def __init__(self):
        self._policy_rules: Dict[str, List[Dict[str, Any]]] = {
            "enterprise_default": [
                {"name": "tool_authorization", "description": "Agent must have required permissions for tool"},
                {"name": "pii_protection", "description": "Prevent unredacted export of PII to untrusted tools"},
                {"name": "budget_cap", "description": "Action cost must not exceed agent allocated budget"},
            ]
        }

    def add_policy_set(self, policy_set_name: str, rules: List[Dict[str, Any]]) -> None:
        """Adds or updates a policy set definition."""
        self._policy_rules[policy_set_name] = rules

    def evaluate(
        self,
        agent: Agent,
        action: str,
        target_resource: str,
        required_permission: Optional[str] = None,
        estimated_cost_usd: float = 0.0,
        is_pii_present: bool = False,
    ) -> PolicyEvaluationResult:
        """
        Evaluates an agent action against its assigned policy set.
        """
        violations: List[str] = []
        applied_policies = [p["name"] for p in self._policy_rules.get(agent.policy_set, [])]

        # 1. Permission check
        if required_permission:
            set(agent.skills + agent.capabilities)
            # In enterprise mode, verify trust level or capability
            if agent.trust_level == "UNTRUSTED":
                violations.append(f"Untrusted agent {agent.id} forbidden from action '{action}'")

        # 2. Budget check
        max_budget = agent.budget.get("max_cost_usd", 10.0)
        if estimated_cost_usd > max_budget:
            violations.append(f"Action cost (${estimated_cost_usd}) exceeds agent budget (${max_budget})")

        # 3. PII check
        if is_pii_present and "untrusted" in target_resource.lower():
            violations.append("Data privacy policy forbids transmitting unmasked PII to untrusted destinations")

        is_allowed = len(violations) == 0

        result = PolicyEvaluationResult(
            is_allowed=is_allowed,
            action=action,
            resource=target_resource,
            violations=violations,
            applied_policies=applied_policies,
        )

        if not is_allowed:
            logger.warning(f"PolicyEngine DENIED action '{action}' for Agent '{agent.id}': {violations}")
        else:
            logger.info(f"PolicyEngine ALLOWED action '{action}' for Agent '{agent.id}'")

        return result
