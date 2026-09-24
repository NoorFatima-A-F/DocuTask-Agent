"""Environment Models and Tier Specifications (Req 30, 31)."""
from dataclasses import dataclass, field
from enum import Enum
from typing import List


class DeploymentEnvironmentType(str, Enum):
    """Supported deployment target environments (Req 30)."""
    LOCAL = "LOCAL"
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    QA = "QA"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
    DR = "DR"
    PRIVATE_CLOUD = "PRIVATE_CLOUD"
    CUSTOMER_MANAGED = "CUSTOMER_MANAGED"
    AIR_GAPPED = "AIR_GAPPED"


@dataclass
class EnvironmentConfiguration:
    """Security, capacity, and governance constraints for an environment tier (Req 31)."""
    environment_type: DeploymentEnvironmentType
    allowed_regions: List[str] = field(default_factory=lambda: ["us-east-1", "us-west-2"])
    requires_approval: bool = False
    required_approver_roles: List[str] = field(default_factory=list)
    min_soak_time_seconds: int = 0
    allowed_strategies: List[str] = field(default_factory=lambda: ["ROLLING", "CANARY", "BLUE_GREEN", "SHADOW"])
    max_replicas: int = 50
    strict_supply_chain: bool = False
    allowed_sources: List[str] = field(default_factory=list)
