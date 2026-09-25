"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Connector Policy Engine.
Enforces governance, regional residency, financial budgets, PII rules, and approval controls.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.connectors.core.models import ActionDescriptor, Connector, ConnectorPolicyRule

logger = logging.getLogger(__name__)


class PolicyEvaluationResult(BaseModel):
    """Result of policy engine pre-execution validation."""
    allowed: bool
    requires_human_approval: bool = False
    policy_name: str = "default_policy"
    violations: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)


class ConnectorPolicyEngine:
    """
    Enterprise policy enforcement point governing all external connector invocations.
    """

    def __init__(self, default_policy: Optional[ConnectorPolicyRule] = None):
        self._default_policy = default_policy or ConnectorPolicyRule()
        self._tenant_policies: Dict[str, ConnectorPolicyRule] = {}  # org_id -> policy

    def set_tenant_policy(self, organization_id: str, policy: ConnectorPolicyRule) -> None:
        """Registers custom policy rules for a specific tenant organization."""
        self._tenant_policies[organization_id] = policy

    def get_policy(self, organization_id: str = "org-default") -> ConnectorPolicyRule:
        """Retrieves effective policy rule for a tenant."""
        return self._tenant_policies.get(organization_id, self._default_policy)

    def evaluate(
        self,
        connector: Connector,
        action: ActionDescriptor,
        inputs: Dict[str, Any],
        organization_id: str = "org-default",
        region: str = "us-east-1",
        data_tags: Optional[List[str]] = None,
    ) -> PolicyEvaluationResult:
        """
        Evaluates an intended connector action against tenant security and compliance policies.
        """
        policy = self.get_policy(organization_id)
        violations: List[str] = []
        warnings: List[str] = []
        requires_approval = False
        tags = data_tags or []

        # 1. Allowed / Disallowed connectors
        if connector.id in policy.disallowed_connectors:
            violations.append(f"Connector '{connector.id}' is explicitly disallowed by enterprise policy")

        if policy.allowed_connectors is not None:
            if connector.id not in policy.allowed_connectors:
                violations.append(f"Connector '{connector.id}' is not in the allowed connectors whitelist")

        # 2. Regional data residency
        if policy.allowed_regions is not None:
            if region not in policy.allowed_regions:
                violations.append(f"Execution in region '{region}' violates data residency policy {policy.allowed_regions}")

        # 3. Disallowed data tags (e.g. PCI, HIPAA, SECRET)
        for tag in tags:
            if tag in policy.disallowed_data_tags:
                violations.append(f"Transmission of data tagged '{tag}' to external connectors is prohibited")

        # 4. Financial cost thresholds
        if action.cost_usd > policy.max_cost_per_call_usd:
            violations.append(f"Action cost (${action.cost_usd:.3f}) exceeds maximum allowed per-call limit (${policy.max_cost_per_call_usd:.3f})")

        if action.cost_usd > policy.require_approval_above_cost_usd:
            requires_approval = True
            warnings.append(f"Action cost (${action.cost_usd:.3f}) exceeds approval threshold (${policy.require_approval_above_cost_usd:.3f})")

        allowed = len(violations) == 0
        if not allowed:
            logger.warning(f"Connector policy violation for {connector.id}.{action.name}: {violations}")

        return PolicyEvaluationResult(
            allowed=allowed,
            requires_human_approval=requires_approval,
            policy_name=policy.name,
            violations=violations,
            warnings=warnings,
        )
