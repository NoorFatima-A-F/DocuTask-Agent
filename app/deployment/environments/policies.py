"""Environment Promotion Policies and Governance Rules."""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from ..core.exceptions import PromotionBlockedException


@dataclass
class EnvironmentTierConfig:
    """Policy requirements for promoting into a specific environment tier."""
    tier_name: str
    allowed_source_tiers: List[str]
    min_soak_time_seconds: int = 0
    min_test_pass_rate: float = 1.0
    required_approver_roles: List[str] = field(default_factory=list)
    requires_zero_vulnerabilities: bool = False


class PromotionPolicy:
    """Enforces enterprise promotion governance and environment hierarchy."""

    DEFAULT_TIERS: Dict[str, EnvironmentTierConfig] = {
        "dev": EnvironmentTierConfig(
            tier_name="dev",
            allowed_source_tiers=[],  # Initial entry point
            min_soak_time_seconds=0,
            min_test_pass_rate=0.9,
            required_approver_roles=[],
            requires_zero_vulnerabilities=False,
        ),
        "testing": EnvironmentTierConfig(
            tier_name="testing",
            allowed_source_tiers=["dev"],
            min_soak_time_seconds=0,
            min_test_pass_rate=0.95,
            required_approver_roles=[],
            requires_zero_vulnerabilities=False,
        ),
        "staging": EnvironmentTierConfig(
            tier_name="staging",
            allowed_source_tiers=["testing"],
            min_soak_time_seconds=5,
            min_test_pass_rate=1.0,
            required_approver_roles=["qa_lead"],
            requires_zero_vulnerabilities=True,
        ),
        "prod": EnvironmentTierConfig(
            tier_name="prod",
            allowed_source_tiers=["staging"],
            min_soak_time_seconds=10,
            min_test_pass_rate=1.0,
            required_approver_roles=["release_manager", "security_lead"],
            requires_zero_vulnerabilities=True,
        ),
    }

    def __init__(self, custom_tiers: Optional[Dict[str, EnvironmentTierConfig]] = None):
        self.tiers = custom_tiers or dict(self.DEFAULT_TIERS)

    def get_tier_config(self, tier: str) -> Optional[EnvironmentTierConfig]:
        """Fetches tier configuration."""
        return self.tiers.get(tier.lower())

    def validate_promotion(
        self,
        source_env: Optional[str],
        target_env: str,
        soak_time_seconds: int,
        test_pass_rate: float,
        approvals: List[str],  # list of approved roles
        has_vulnerabilities: bool = False,
    ) -> bool:
        """Validates all governance requirements for promoting between environments."""
        target_cfg = self.get_tier_config(target_env)
        if not target_cfg:
            raise PromotionBlockedException(f"Unknown target environment tier: '{target_env}'")

        # 1. Source tier validation (if source specified)
        if target_cfg.allowed_source_tiers and source_env:
            if source_env.lower() not in target_cfg.allowed_source_tiers:
                raise PromotionBlockedException(
                    f"Direct promotion from '{source_env}' to '{target_env}' is forbidden. "
                    f"Allowed sources: {target_cfg.allowed_source_tiers}"
                )

        # 2. Soak time validation
        if soak_time_seconds < target_cfg.min_soak_time_seconds:
            raise PromotionBlockedException(
                f"Promotion to '{target_env}' requires at least {target_cfg.min_soak_time_seconds}s soak time "
                f"(current soak: {soak_time_seconds}s)"
            )

        # 3. Test pass rate validation
        if test_pass_rate < target_cfg.min_test_pass_rate:
            raise PromotionBlockedException(
                f"Test pass rate {test_pass_rate*100:.1f}% does not meet required {target_cfg.min_test_pass_rate*100:.1f}% for '{target_env}'"
            )

        # 4. Security vulnerability policy
        if target_cfg.requires_zero_vulnerabilities and has_vulnerabilities:
            raise PromotionBlockedException(
                f"Promotion to '{target_env}' blocked: unresolved critical/high security vulnerabilities detected"
            )

        # 5. Required approvals
        for req_role in target_cfg.required_approver_roles:
            if req_role not in approvals:
                raise PromotionBlockedException(
                    f"Missing required approver role '{req_role}' for promotion to '{target_env}'"
                )

        return True
