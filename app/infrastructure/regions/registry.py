"""Persistent, Thread-Safe Region Registry."""

import json
from pathlib import Path
import threading
from typing import Dict, List, Optional
from app.infrastructure.regions.models import Region, RegionStatus


class RegionRegistry:
    """Enterprise Registry managing all platform regions."""

    def __init__(self, persistence_path: Optional[str] = None):
        self._regions: Dict[str, Region] = {}
        self._lock = threading.RLock()
        self._persistence_path = Path(persistence_path) if persistence_path else None

        if self._persistence_path and self._persistence_path.exists():
            self._load_from_disk()

    def register_region(self, region: Region) -> Region:
        """Register a new region or update existing."""
        with self._lock:
            self._regions[region.region_id] = region
            self._save_to_disk()
            return region

    def get_region(self, region_id: str) -> Optional[Region]:
        """Retrieve region by region_id."""
        with self._lock:
            return self._regions.get(region_id)

    def list_regions(
        self,
        status: Optional[RegionStatus] = None,
        jurisdiction: Optional[str] = None,
        provider: Optional[str] = None,
    ) -> List[Region]:
        """List regions with optional filtering."""
        with self._lock:
            results = list(self._regions.values())
            if status:
                results = [r for r in results if r.status == status]
            if jurisdiction:
                results = [
                    r for r in results
                    if r.data_residency_jurisdiction.upper() == jurisdiction.upper()
                    or r.geography.jurisdiction.upper() == jurisdiction.upper()
                ]
            if provider:
                results = [r for r in results if r.provider.lower() == provider.lower()]
            return results

    def update_region_status(self, region_id: str, status: RegionStatus) -> Optional[Region]:
        """Update lifecycle status of a region."""
        with self._lock:
            region = self._regions.get(region_id)
            if not region:
                return None
            region.status = status
            self._save_to_disk()
            return region

    def assign_cluster_to_region(self, region_id: str, cluster_id: str) -> bool:
        """Associate a cluster with a region."""
        with self._lock:
            region = self._regions.get(region_id)
            if not region:
                return False
            if cluster_id not in region.active_cluster_ids:
                region.active_cluster_ids.append(cluster_id)
                self._save_to_disk()
            return True

    def remove_cluster_from_region(self, region_id: str, cluster_id: str) -> bool:
        """Disassociate a cluster from a region."""
        with self._lock:
            region = self._regions.get(region_id)
            if not region:
                return False
            if cluster_id in region.active_cluster_ids:
                region.active_cluster_ids.remove(cluster_id)
                self._save_to_disk()
            return True

    def get_failover_region(self, region_id: str) -> Optional[Region]:
        """Retrieve designated failover region for a given region."""
        with self._lock:
            region = self._regions.get(region_id)
            if not region or not region.failover_region_id:
                return None
            return self._regions.get(region.failover_region_id)

    def delete_region(self, region_id: str) -> bool:
        """Remove a region from the registry."""
        with self._lock:
            if region_id in self._regions:
                del self._regions[region_id]
                self._save_to_disk()
                return True
            return False

    def clear(self) -> None:
        """Clear all in-memory regions (useful for testing)."""
        with self._lock:
            self._regions.clear()
            self._save_to_disk()

    def _save_to_disk(self) -> None:
        if not self._persistence_path:
            return
        try:
            self._persistence_path.parent.mkdir(parents=True, exist_ok=True)
            data = {r_id: reg.model_dump(mode="json") for r_id, reg in self._regions.items()}
            with open(self._persistence_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def _load_from_disk(self) -> None:
        try:
            with open(self._persistence_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                for r_id, r_data in raw_data.items():
                    self._regions[r_id] = Region.model_validate(r_data)
        except Exception:
            pass
