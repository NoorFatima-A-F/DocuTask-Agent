"""Governance Gate Enforcement Engine (Req 51, 52)."""
from typing import List, Tuple
from .policies import ReleaseFreezeManager
from .risk import ReleaseRiskEvaluator, RiskLevel


class DeploymentGovernanceEnforcer:
    """Combines risk analysis and release freezes to approve or block deployment requests."""

    def __init__(self, freeze_manager: Optional[ReleaseFreezeManager] = None):
        self.freeze_manager = freeze_manager or ReleaseFreezeManager()

    def evaluate_deployment_request(
        self,
        environment: str,
        region: str,
        component: str,
        risk_level: RiskLevel,
        approved_by: Optional[str] = None,
    ) -> Tuple[bool, str]:
        # 1. Check freeze window
        frozen, freeze_reason = self.freeze_manager.is_deployment_frozen(environment, region, component)
        if frozen:
            return False, freeze_reason or "Deployment blocked by active release freeze"

        # 2. Critical/High risk in production requires explicit multi-party sign-off
        if environment.lower() == "production":
            if risk_level in {RiskLevel.HIGH, RiskLevel.CRITICAL} and not approved_by:
                return False, f"Production deployment of {risk_level.value} risk change requires explicit executive sign-off"

        return True, "Governance policy check passed"
