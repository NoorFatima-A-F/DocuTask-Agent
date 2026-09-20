"""
Failover Router & Traffic Shift Control.

Manages dynamic traffic shifting, weighted canary splits, in-flight request draining,
and route table updates during regional and cluster failovers.
"""

from __future__ import annotations

import logging
import random
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("infrastructure.failover.routing")


class RouteTarget(BaseModel):
    """Target destination endpoint or region."""
    target_id: str
    region_id: str
    cluster_id: Optional[str] = None
    weight: float = Field(default=100.0, ge=0.0, le=100.0)
    enabled: bool = True
    draining: bool = False


class ServiceRouteTable(BaseModel):
    """Routing configuration for a specific service or tenant."""
    service_name: str
    active_targets: List[RouteTarget] = Field(default_factory=list)
    fallback_target: Optional[str] = None


class FailoverRouter:
    """
    Directs traffic across regions and clusters with support for zero-downtime traffic shifts.
    """

    def __init__(self) -> None:
        self._route_tables: Dict[str, ServiceRouteTable] = {}  # service_name -> ServiceRouteTable

    def register_service_route(self, service_name: str, targets: List[RouteTarget], fallback_target: Optional[str] = None) -> ServiceRouteTable:
        table = ServiceRouteTable(
            service_name=service_name,
            active_targets=targets,
            fallback_target=fallback_target,
        )
        self._route_tables[service_name] = table
        return table

    def get_route_table(self, service_name: str) -> Optional[ServiceRouteTable]:
        return self._route_tables.get(service_name)

    def route_request(self, service_name: str) -> Optional[RouteTarget]:
        """
        Select destination target using weighted probabilistic selection among non-draining targets.
        """
        table = self._route_tables.get(service_name)
        if not table or not table.active_targets:
            return None

        candidates = [t for t in table.active_targets if t.enabled and not t.draining and t.weight > 0]
        if not candidates:
            # Fallback to any enabled candidate or fallback target
            enabled = [t for t in table.active_targets if t.enabled]
            return enabled[0] if enabled else None

        total_weight = sum(t.weight for t in candidates)
        if total_weight <= 0:
            return candidates[0]

        r = random.uniform(0, total_weight)
        cumulative = 0.0
        for target in candidates:
            cumulative += target.weight
            if r <= cumulative:
                return target

        return candidates[-1]

    def shift_traffic(
        self,
        service_name: str,
        from_region: str,
        to_region: str,
        percentage_to_shift: float = 100.0,
    ) -> bool:
        """
        Shift traffic weight from source region to target region for a service.
        """
        table = self._route_tables.get(service_name)
        if not table:
            return False

        source_targets = [t for t in table.active_targets if t.region_id == from_region]
        target_targets = [t for t in table.active_targets if t.region_id == to_region]

        if not source_targets or not target_targets:
            logger.warning(f"Cannot shift traffic for '{service_name}': missing source or target in route table.")
            return False

        shift_fraction = min(1.0, max(0.0, percentage_to_shift / 100.0))

        for st in source_targets:
            st.weight = max(0.0, st.weight * (1.0 - shift_fraction))
            if st.weight == 0:
                st.draining = True

        for tt in target_targets:
            tt.enabled = True
            tt.draining = False
            tt.weight = min(100.0, tt.weight + (100.0 * shift_fraction))

        logger.info(
            f"Shifted {percentage_to_shift}% traffic for '{service_name}' from '{from_region}' to '{to_region}'"
        )
        return True

    def mark_region_draining(self, region_id: str) -> int:
        """Mark all route targets in a region as draining."""
        count = 0
        for table in self._route_tables.values():
            for target in table.active_targets:
                if target.region_id == region_id:
                    target.draining = True
                    target.weight = 0.0
                    count += 1
        return count
