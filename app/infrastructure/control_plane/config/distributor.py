"""Configuration Distribution and Rollback Management across Multi-Region Clusters."""

from datetime import datetime, timezone
import hashlib
import json
import threading
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ConfigBundle(BaseModel):
    bundle_id: str
    version: str
    checksum: str
    payload: Dict[str, Any]
    target_regions: List[str] = Field(default_factory=list)  # Empty means all
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ConfigurationDistributor:
    """Manages versioned configuration distribution, canary rollout, and rollbacks."""

    def __init__(self):
        self._bundles: Dict[str, ConfigBundle] = {}
        self._applied_cluster_configs: Dict[str, str] = {}  # cluster_id -> bundle_id
        self._applied_region_configs: Dict[str, str] = {}   # region_id -> bundle_id
        self._history: List[Dict[str, Any]] = []
        self._lock = threading.RLock()

    def create_bundle(
        self, version: str, payload: Dict[str, Any], target_regions: Optional[List[str]] = None
    ) -> ConfigBundle:
        """Publish a new immutable versioned configuration bundle."""
        with self._lock:
            payload_str = json.dumps(payload, sort_keys=True)
            checksum = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
            bundle_id = f"cfg_{version}_{checksum[:8]}"

            bundle = ConfigBundle(
                bundle_id=bundle_id,
                version=version,
                checksum=checksum,
                payload=payload,
                target_regions=target_regions or [],
            )
            self._bundles[bundle_id] = bundle
            return bundle

    def distribute_to_cluster(self, bundle_id: str, cluster_id: str) -> bool:
        """Apply a config bundle to a specific cluster."""
        with self._lock:
            bundle = self._bundles.get(bundle_id)
            if not bundle:
                return False

            self._applied_cluster_configs[cluster_id] = bundle_id
            self._history.append({
                "target_type": "CLUSTER",
                "target_id": cluster_id,
                "bundle_id": bundle_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return True

    def distribute_to_region(self, bundle_id: str, region_id: str) -> bool:
        """Apply a config bundle to a specific region."""
        with self._lock:
            bundle = self._bundles.get(bundle_id)
            if not bundle:
                return False

            self._applied_region_configs[region_id] = bundle_id
            self._history.append({
                "target_type": "REGION",
                "target_id": region_id,
                "bundle_id": bundle_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            return True

    def rollback_cluster(self, cluster_id: str, target_bundle_id: str) -> bool:
        """Rollback cluster configuration to a designated prior bundle."""
        return self.distribute_to_cluster(target_bundle_id, cluster_id)

    def get_cluster_config(self, cluster_id: str) -> Optional[ConfigBundle]:
        with self._lock:
            bundle_id = self._applied_cluster_configs.get(cluster_id)
            if not bundle_id:
                return None
            return self._bundles.get(bundle_id)

    def get_region_config(self, region_id: str) -> Optional[ConfigBundle]:
        with self._lock:
            bundle_id = self._applied_region_configs.get(region_id)
            if not bundle_id:
                return None
            return self._bundles.get(bundle_id)
