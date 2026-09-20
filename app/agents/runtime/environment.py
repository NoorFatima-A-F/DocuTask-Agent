"""
Runtime Environment Isolation.
Defines execution environment types and enforces security constraints for production deployments.
"""

from enum import Enum


class EnvironmentType(str, Enum):
    """Runtime execution environment tier."""
    DEV = "DEV"
    STAGING = "STAGING"
    PROD = "PROD"
    TEST = "TEST"


class EnvironmentPolicy:
    """Enforces deployment tier constraints."""

    @staticmethod
    def is_production(env: str) -> bool:
        """Returns True if environment is PROD."""
        return env.upper() == EnvironmentType.PROD.value

    @staticmethod
    def allows_experimental_features(env: str) -> bool:
        """Restricts experimental engines to non-production environments."""
        return not EnvironmentPolicy.is_production(env)
