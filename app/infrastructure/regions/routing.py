"""Multi-Region Routing and Region Selection Utilities."""

from typing import Dict, List, Optional
from app.infrastructure.regions.models import LatencyClass, Region, RegionStatus
from app.infrastructure.regions.affinity import TenantAffinityManager


class MultiRegionRouter:
    """Calculates optimal region routing paths considering health, priority, latency, and tenant affinity."""

    def __init__(self, affinity_manager: Optional[TenantAffinityManager] = None):
        self.affinity_manager = affinity_manager or TenantAffinityManager()

    def rank_regions(
        self,
        candidate_regions: List[Region],
        tenant_id: Optional[str] = None,
        preferred_jurisdiction: Optional[str] = None,
        estimated_latencies_ms: Optional[Dict[str, float]] = None,
    ) -> List[Region]:
        """Rank regions in descending order of desirability for a request."""
        latencies = estimated_latencies_ms or {}
        eligible: List[Region] = []

        for region in candidate_regions:
            # Must be ACTIVE or STANDBY (STANDBY gets lower rank)
            if region.status not in (RegionStatus.ACTIVE, RegionStatus.STANDBY):
                continue

            # Tenant affinity check
            if tenant_id and not self.affinity_manager.is_region_allowed_for_tenant(tenant_id, region.region_id):
                continue

            # Preferred jurisdiction filter if specified
            if preferred_jurisdiction and preferred_jurisdiction.upper() != "GLOBAL":
                if (
                    region.data_residency_jurisdiction.upper() != preferred_jurisdiction.upper()
                    and region.geography.jurisdiction.upper() != preferred_jurisdiction.upper()
                ):
                    continue

            eligible.append(region)

        # Sorting key:
        # 1. Primary status (True first)
        # 2. Status (ACTIVE before STANDBY)
        # 3. Routing priority (lower number = better)
        # 4. Latency (lower ms = better)
        def score_key(r: Region):
            active_score = 0 if r.status == RegionStatus.ACTIVE else 1
            primary_score = 0 if r.is_primary else 1
            priority = r.routing_priority
            lat = latencies.get(r.region_id, 50.0)
            return (primary_score, active_score, priority, lat)

        return sorted(eligible, key=score_key)
