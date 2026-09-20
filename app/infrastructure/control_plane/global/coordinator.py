"""Global Control Plane Coordinator for Multi-Region Synchronization and Consensus."""

import threading
from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.infrastructure.regions.registry import RegionRegistry
from app.infrastructure.regions.models import Region, RegionStatus


class GlobalCoordinator:
    """Coordinates consensus, epoch bumping, and cross-region synchronization."""

    def __init__(self, region_registry: RegionRegistry):
        self.region_registry = region_registry
        self.epoch = 1
        self._lock = threading.RLock()
        self._last_sync_timestamps: Dict[str, datetime] = {}

    def bump_epoch(self) -> int:
        """Increment control plane configuration epoch."""
        with self._lock:
            self.epoch += 1
            return self.epoch

    def sync_region(self, region_id: str) -> bool:
        """Mark a region as synchronized with global state."""
        with self._lock:
            region = self.region_registry.get_region(region_id)
            if not region:
                return False
            self._last_sync_timestamps[region_id] = datetime.now(timezone.utc)
            return True

    def get_sync_status(self) -> Dict[str, datetime]:
        """Get synchronization timestamps for all regions."""
        with self._lock:
            return dict(self._last_sync_timestamps)

    def check_global_quorum(self, min_regions: int = 2) -> bool:
        """Verify global active regions meet minimum consensus quorum."""
        with self._lock:
            active = self.region_registry.list_regions(status=RegionStatus.ACTIVE)
            return len(active) >= min_regions
