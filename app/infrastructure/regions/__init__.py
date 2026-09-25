"""Region Subsystem for Distributed Multi-Region Governance."""

from app.infrastructure.regions.models import (
    Region,
    RegionStatus,
    Geography,
    LatencyClass,
)
from app.infrastructure.regions.registry import RegionRegistry
from app.infrastructure.regions.policies import RegionPolicyEngine
from app.infrastructure.regions.affinity import (
    TenantAffinityRule,
    TenantAffinityManager,
)
from app.infrastructure.regions.routing import MultiRegionRouter

__all__ = [
    "Region",
    "RegionStatus",
    "Geography",
    "LatencyClass",
    "RegionRegistry",
    "RegionPolicyEngine",
    "TenantAffinityRule",
    "TenantAffinityManager",
    "MultiRegionRouter",
]
