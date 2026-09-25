"""Model Policy Enforcement Engine (Phase 8C)."""

from __future__ import annotations

from typing import Dict, List
from app.model_governance.registry.models import Model, ModelLifecycleState
from app.model_governance.policies.rules import ModelGovernancePolicyRule


class ModelPolicyEnforcer:
    """Validates model invocation requests against organization governance policies."""

    def __init__(self):
        # org_id -> List[ModelGovernancePolicyRule]
        self._policies: Dict[str, List[ModelGovernancePolicyRule]] = {}

    def add_rule(self, rule: ModelGovernancePolicyRule) -> None:
        """Add a governance policy rule."""
        if rule.organization_id not in self._policies:
            self._policies[rule.organization_id] = []
        self._policies[rule.organization_id].append(rule)

    def set_policy(self, organization_id: str, policy: ModelGovernancePolicyRule) -> None:
        """Assign or update model governance policy."""
        self._policies[organization_id] = [policy]

    def get_policies(self, organization_id: str) -> List[ModelGovernancePolicyRule]:
        """Retrieve policies for organization."""
        return self._policies.get(
            organization_id,
            [ModelGovernancePolicyRule(policy_id="default_policy", organization_id=organization_id)],
        )

    def validate_execution(
        self,
        model: Model,
        organization_id: str,
        target_region: str = "us-east-1",
    ) -> bool:
        """Validate if model invocation is compliant with active policies."""
        policies = self.get_policies(organization_id)

        for policy in policies:
            # 1. Active status check
            current_state = model.lifecycle_state or model.status
            if policy.block_unapproved_models and current_state != ModelLifecycleState.ACTIVE:
                raise ValueError(f"Model '{model.model_id}' is not in ACTIVE state ('{current_state.value}')")

            # 2. Provider check
            prov_name = model.provider.value if hasattr(model.provider, "value") else str(model.provider)
            if prov_name not in policy.allowed_providers:
                raise ValueError(f"Model provider '{prov_name}' is not allowed by policy")

            # 3. Cost check
            if model.input_token_cost_per_1k > policy.max_input_cost_per_1k:
                raise ValueError(
                    f"Model input cost (${model.input_token_cost_per_1k:.5f}) exceeds allowed limit (${policy.max_input_cost_per_1k:.5f})"
                )

            # 4. Region check
            if target_region not in policy.allowed_regions:
                raise ValueError(f"Model '{model.model_id}' is not approved for execution in region '{target_region}'")

        return True
