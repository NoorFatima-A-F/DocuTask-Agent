"""Global Scheduler for Coarse Regional Placement and Governance Routing."""

from typing import List, Optional
from app.infrastructure.regions.models import Region
from app.infrastructure.regions.registry import RegionRegistry
from app.infrastructure.regions.policies import RegionPolicyEngine
from app.infrastructure.regions.affinity import TenantAffinityManager
from app.infrastructure.topology.selectors import RegionSelector
from app.infrastructure.executions.workload import WorkloadRequest
from app.infrastructure.topology.locality import DataLocalityResolver


class GlobalScheduler:
    """Evaluates multi-region governance, tenant affinity, and data residency to select destination regions."""

    def __init__(
        self,
        region_registry: RegionRegistry,
        affinity_manager: Optional[TenantAffinityManager] = None,
        region_policy_engine: Optional[RegionPolicyEngine] = None,
    ) -> None:
        self.region_registry = region_registry
        self.affinity_manager = affinity_manager or TenantAffinityManager()
        self.region_policy_engine = region_policy_engine or RegionPolicyEngine()
        self.region_selector = RegionSelector(region_registry)

    def select_eligible_regions(self, workload: WorkloadRequest) -> List[Region]:
        """Filter candidate regions based on policy, tenant affinity, and residency."""
        candidates = self.region_selector.select_eligible_regions(workload)

        eligible: List[Region] = []
        for reg in candidates:
            # 1. Tenant Affinity check
            if not self.affinity_manager.is_region_allowed_for_tenant(workload.tenant_id, reg.region_id):
                continue

            # 2. Compliance check
            if workload.compliance_context:
                comp_ok, _ = self.region_policy_engine.validate_compliance(
                    reg, workload.compliance_context
                )
                if not comp_ok:
                    continue

            eligible.append(reg)

        return eligible

    def rank_eligible_regions(
        self, eligible_regions: List[Region], workload: WorkloadRequest
    ) -> List[Region]:
        """Rank eligible regions by data locality, preference, priority, and primary status."""
        loc_region = DataLocalityResolver.resolve_locality_region(workload.data_locality_uri)

        def region_rank_key(r: Region):
            # 1. Data Locality Match (0 if match, 1 otherwise)
            loc_match = 0 if loc_region and r.region_id == loc_region else 1
            # 2. Preference match rank
            pref_rank = (
                workload.region_preferences.index(r.region_id)
                if r.region_id in workload.region_preferences
                else 999
            )
            # 3. Is Primary
            primary_score = 0 if r.is_primary else 1
            # 4. Routing Priority (lower number = higher priority)
            return (loc_match, pref_rank, primary_score, r.routing_priority)

        return sorted(eligible_regions, key=region_rank_key)
