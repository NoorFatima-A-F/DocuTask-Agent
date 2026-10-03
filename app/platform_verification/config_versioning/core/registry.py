"""
Configuration Registry with SemVer Indexing and Retrieval.
"""
from typing import Dict, List, Optional
from app.platform_verification.config_versioning.domain.models import ConfigurationSnapshot
from app.platform_verification.config_versioning.domain.interfaces import ConfigurationRegistryInterface

class ConfigurationRegistry(ConfigurationRegistryInterface):
    def __init__(self):
        self._snapshots: Dict[str, ConfigurationSnapshot] = {}

    def store_snapshot(self, snapshot: ConfigurationSnapshot) -> ConfigurationSnapshot:
        self._snapshots[snapshot.snapshot_id] = snapshot
        return snapshot

    def get_snapshot(self, snapshot_id: str) -> Optional[ConfigurationSnapshot]:
        return self._snapshots.get(snapshot_id)

    def list_snapshots(self, tenant_id: str = "default-tenant") -> List[ConfigurationSnapshot]:
        return [s for s in self._snapshots.values() if s.tenant_id == tenant_id]

configuration_registry = ConfigurationRegistry()
