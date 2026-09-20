"""Environment Hierarchy and Promotion Governance Rules (Req 32)."""
from typing import Dict, List, Optional
from .models import DeploymentEnvironmentType, EnvironmentConfiguration


class EnvironmentHierarchyPolicy:
    """Enforces strict promotion flow: DEVELOPMENT -> TESTING -> STAGING -> PRODUCTION."""

    DEFAULT_ENV_CONFIGS: Dict[str, EnvironmentConfiguration] = {
        "development": EnvironmentConfiguration(
            environment_type=DeploymentEnvironmentType.DEVELOPMENT,
            allowed_sources=[],
            min_soak_time_seconds=0,
            requires_approval=False,
            strict_supply_chain=False,
        ),
        "testing": EnvironmentConfiguration(
            environment_type=DeploymentEnvironmentType.TESTING,
            allowed_sources=["development"],
            min_soak_time_seconds=0,
            requires_approval=False,
            strict_supply_chain=False,
        ),
        "staging": EnvironmentConfiguration(
            environment_type=DeploymentEnvironmentType.STAGING,
            allowed_sources=["testing"],
            min_soak_time_seconds=5,
            requires_approval=True,
            required_approver_roles=["qa_lead"],
            strict_supply_chain=True,
        ),
        "production": EnvironmentConfiguration(
            environment_type=DeploymentEnvironmentType.PRODUCTION,
            allowed_sources=["staging"],
            min_soak_time_seconds=10,
            requires_approval=True,
            required_approver_roles=["release_manager", "security_lead"],
            strict_supply_chain=True,
        ),
    }

    def __init__(self, configs: Optional[Dict[str, EnvironmentConfiguration]] = None):
        self.configs = configs or dict(self.DEFAULT_ENV_CONFIGS)

    def get_config(self, env_name: str) -> Optional[EnvironmentConfiguration]:
        return self.configs.get(env_name.lower())

    def validate_promotion_path(self, source_env: Optional[str], target_env: str) -> bool:
        target_cfg = self.get_config(target_env)
        if not target_cfg:
            raise ValueError(f"Unknown target environment: '{target_env}'")

        if target_cfg.allowed_sources and source_env:
            if source_env.lower() not in target_cfg.allowed_sources:
                raise ValueError(
                    f"Illegal promotion path: Cannot promote directly from '{source_env}' to '{target_env}'. "
                    f"Allowed sources: {target_cfg.allowed_sources}"
                )
        return True
