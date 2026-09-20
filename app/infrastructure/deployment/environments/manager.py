"""Environment Management, Topologies, and Configuration Separation."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import threading


class EnvironmentType(str, Enum):
    """Target deployment environment classifications."""
    DEV = "dev"
    TEST = "test"
    STAGING = "staging"
    PROD = "prod"
    CUSTOMER_MANAGED = "customer_managed"
    AIR_GAPPED = "air_gapped"


@dataclass
class EnvironmentConfig:
    """Configuration and topology for a deployment environment."""
    env_id: str
    name: str
    env_type: EnvironmentType
    cluster_ids: List[str] = field(default_factory=list)
    regions: List[str] = field(default_factory=list)
    namespace_prefix: str = "docutask"
    is_production_like: bool = False
    requires_approval: bool = False
    resource_quota_cpu: int = 16
    resource_quota_memory_gb: int = 64
    active_release_id: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)


class EnvironmentManager:
    """Manages runtime environments, topologies, and isolation boundaries."""

    def __init__(self) -> None:
        self._environments: Dict[str, EnvironmentConfig] = {}
        self._lock = threading.RLock()
        self._init_default_environments()

    def _init_default_environments(self) -> None:
        """Initialize standard platform environments."""
        defaults = [
            EnvironmentConfig("dev", "Development", EnvironmentType.DEV, ["cluster-dev"], ["us-east-1"]),
            EnvironmentConfig("test", "Testing / QA", EnvironmentType.TEST, ["cluster-test"], ["us-east-1"]),
            EnvironmentConfig("staging", "Staging", EnvironmentType.STAGING, ["cluster-stage"], ["us-east-1"], is_production_like=True),
            EnvironmentConfig("prod", "Enterprise Production", EnvironmentType.PROD, ["cluster-prod-alpha", "cluster-prod-beta"], ["us-east-1", "us-west-2"], is_production_like=True, requires_approval=True),
            EnvironmentConfig("customer_managed", "Customer VPC Dedicated", EnvironmentType.CUSTOMER_MANAGED, ["cluster-cust-01"], ["eu-west-1"], is_production_like=True, requires_approval=True),
            EnvironmentConfig("air_gapped", "Air-Gapped Sovereign", EnvironmentType.AIR_GAPPED, ["cluster-gov-01"], ["us-gov-west-1"], is_production_like=True, requires_approval=True),
        ]
        for env in defaults:
            self._environments[env.env_id] = env

    def register_environment(self, config: EnvironmentConfig) -> None:
        """Register or update an environment."""
        with self._lock:
            self._environments[config.env_id] = config

    def get_environment(self, env_id: str) -> Optional[EnvironmentConfig]:
        """Fetch environment configuration."""
        with self._lock:
            return self._environments.get(env_id)

    def list_environments(self) -> List[EnvironmentConfig]:
        """List all registered environments."""
        with self._lock:
            return list(self._environments.values())
