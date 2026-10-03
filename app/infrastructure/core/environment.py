"""Environment Management and Isolation Platform."""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EnvironmentType(str, Enum):
    LOCAL = "LOCAL"
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
    DISASTER_RECOVERY = "DISASTER_RECOVERY"


class EnvironmentProfile(BaseModel):
    """Configuration, quota, and security profile for an environment."""

    env_type: EnvironmentType
    name: str
    max_cpu_cores: int
    max_memory_gb: int
    max_replicas_per_service: int
    require_deployment_approval: bool = False
    allow_mock_providers: bool = False
    enforce_strict_security: bool = True
    primary_region: str = "us-east-1"
    allowed_regions: List[str] = Field(default_factory=lambda: ["us-east-1", "eu-west-1"])
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EnvironmentManager:
    """Manages multi-environment isolation, profiles, and quota enforcement."""

    DEFAULT_PROFILES: Dict[EnvironmentType, EnvironmentProfile] = {
        EnvironmentType.LOCAL: EnvironmentProfile(
            env_type=EnvironmentType.LOCAL,
            name="Local Developer Machine",
            max_cpu_cores=8,
            max_memory_gb=16,
            max_replicas_per_service=2,
            require_deployment_approval=False,
            allow_mock_providers=True,
            enforce_strict_security=False,
            primary_region="local",
            allowed_regions=["local"],
        ),
        EnvironmentType.DEVELOPMENT: EnvironmentProfile(
            env_type=EnvironmentType.DEVELOPMENT,
            name="Development Cluster",
            max_cpu_cores=32,
            max_memory_gb=64,
            max_replicas_per_service=4,
            require_deployment_approval=False,
            allow_mock_providers=True,
            enforce_strict_security=False,
            primary_region="us-east-1",
            allowed_regions=["us-east-1"],
        ),
        EnvironmentType.TESTING: EnvironmentProfile(
            env_type=EnvironmentType.TESTING,
            name="Automated Testing & CI/CD",
            max_cpu_cores=16,
            max_memory_gb=32,
            max_replicas_per_service=2,
            require_deployment_approval=False,
            allow_mock_providers=True,
            enforce_strict_security=False,
            primary_region="us-east-1",
            allowed_regions=["us-east-1"],
        ),
        EnvironmentType.STAGING: EnvironmentProfile(
            env_type=EnvironmentType.STAGING,
            name="Pre-Production Staging",
            max_cpu_cores=64,
            max_memory_gb=128,
            max_replicas_per_service=10,
            require_deployment_approval=True,
            allow_mock_providers=False,
            enforce_strict_security=True,
            primary_region="us-east-1",
            allowed_regions=["us-east-1", "eu-west-1"],
        ),
        EnvironmentType.PRODUCTION: EnvironmentProfile(
            env_type=EnvironmentType.PRODUCTION,
            name="Global Production Environment",
            max_cpu_cores=256,
            max_memory_gb=512,
            max_replicas_per_service=50,
            require_deployment_approval=True,
            allow_mock_providers=False,
            enforce_strict_security=True,
            primary_region="us-east-1",
            allowed_regions=["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
        ),
        EnvironmentType.DISASTER_RECOVERY: EnvironmentProfile(
            env_type=EnvironmentType.DISASTER_RECOVERY,
            name="Disaster Recovery Secondary Site",
            max_cpu_cores=256,
            max_memory_gb=512,
            max_replicas_per_service=50,
            require_deployment_approval=True,
            allow_mock_providers=False,
            enforce_strict_security=True,
            primary_region="eu-west-1",
            allowed_regions=["eu-west-1", "us-west-2"],
        ),
    }

    def __init__(self, current_env: EnvironmentType = EnvironmentType.LOCAL) -> None:
        self.current_env = current_env
        self._profiles = dict(self.DEFAULT_PROFILES)

    def get_profile(self, env_type: Optional[EnvironmentType] = None) -> EnvironmentProfile:
        target = env_type or self.current_env
        return self._profiles[target]

    def set_current_environment(self, env_type: EnvironmentType) -> None:
        self.current_env = env_type

    def validate_deployment_allowed(
        self,
        requested_replicas: int,
        requested_cpu: int,
        requested_memory_gb: int,
        target_region: Optional[str] = None,
        env_type: Optional[EnvironmentType] = None,
    ) -> tuple[bool, str]:
        """Check whether a requested workload fits within environment policies."""
        profile = self.get_profile(env_type)

        if requested_replicas > profile.max_replicas_per_service:
            return (
                False,
                f"Requested replicas ({requested_replicas}) exceeds {profile.name} max ({profile.max_replicas_per_service}).",
            )

        if requested_cpu > profile.max_cpu_cores:
            return (
                False,
                f"Requested CPU cores ({requested_cpu}) exceeds {profile.name} quota ({profile.max_cpu_cores}).",
            )

        if requested_memory_gb > profile.max_memory_gb:
            return (
                False,
                f"Requested memory ({requested_memory_gb}GB) exceeds {profile.name} quota ({profile.max_memory_gb}GB).",
            )

        region = target_region or profile.primary_region
        if region not in profile.allowed_regions:
            return (
                False,
                f"Region '{region}' is not allowed in {profile.name}. Allowed: {profile.allowed_regions}",
            )

        return True, "Environment policy satisfied."
