"""Override Validation against Policies and Safety Constraints."""

from typing import Dict, Any, List, Optional, Tuple
from .policies import OverridePolicy
from ..core.context import OversightContext
from ..core.exceptions import InvalidOverrideError


class OverrideValidator:
    """Validates human override proposals against enterprise safety boundaries."""

    def __init__(self, policies: Optional[List[OverridePolicy]] = None):
        self.policies = policies or [OverridePolicy(name="Default Safe Override Policy")]

    def validate_override(
        self,
        reviewer_id: str,
        reviewer_role: str,
        justification: str,
        context: OversightContext,
        policy: Optional[OverridePolicy] = None,
    ) -> Tuple[bool, str]:
        active_policy = policy or self.policies[0]

        # 1. Justification Length Check
        if not justification or len(justification.strip()) < active_policy.min_justification_length:
            return (
                False,
                f"Override justification must be at least {active_policy.min_justification_length} characters",
            )

        # 2. Role Check
        if active_policy.allowed_roles and reviewer_role not in active_policy.allowed_roles:
            return (
                False,
                f"Reviewer role '{reviewer_role}' not authorized to perform overrides. Allowed: {active_policy.allowed_roles}",
            )

        # 3. Prohibited Action Type
        if context.action_type in active_policy.prohibited_action_types:
            return (
                False,
                f"Action type '{context.action_type}' is strictly prohibited from manual override",
            )

        # 4. Critical Safety Threshold
        if context.risk_score > active_policy.max_risk_score_overrideable:
            return (
                False,
                f"Risk score ({context.risk_score:.2f}) exceeds maximum overrideable safety threshold ({active_policy.max_risk_score_overrideable:.2f})",
            )

        return True, "Override validation passed"
