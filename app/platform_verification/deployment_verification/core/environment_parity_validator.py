"""
Environment Parity and Drift Analyzer.
"""
from typing import Dict, List, Any
from app.platform_verification.deployment_verification.domain.models import EnvironmentDriftReport
from app.platform_verification.deployment_verification.domain.interfaces import IEnvironmentParityValidator


class EnvironmentParityValidator(IEnvironmentParityValidator):
    """Compares environment configurations to detect configuration drift and missing variables."""

    REQUIRED_VARS = {"DATABASE_URL", "REDIS_URL", "STORAGE_BUCKET", "ENVIRONMENT", "SECRET_KEY"}

    def validate_parity(self, env_configs: Dict[str, Dict[str, Any]]) -> EnvironmentDriftReport:
        drift_items: List[str] = []
        missing: List[str] = []
        stages = list(env_configs.keys())

        for stage, config in env_configs.items():
            for req in self.REQUIRED_VARS:
                if req not in config:
                    missing.append(f"Stage '{stage}' missing required env var '{req}'")

        # Compare settings consistency
        if "STAGING" in env_configs and "PRODUCTION" in env_configs:
            staging_keys = set(env_configs["STAGING"].keys())
            prod_keys = set(env_configs["PRODUCTION"].keys())
            diff = staging_keys.symmetric_difference(prod_keys)
            for d in diff:
                drift_items.append(f"Configuration key mismatch between Staging and Prod: '{d}'")

        score = 100.0 - (len(missing) * 15.0) - (len(drift_items) * 10.0)
        score = max(0.0, min(100.0, score))
        status = "PASS" if len(missing) == 0 and len(drift_items) == 0 else "FAIL"

        return EnvironmentDriftReport(
            compared_environments=stages,
            drift_items=drift_items,
            missing_variables=missing,
            parity_score=score,
            status=status,
        )
