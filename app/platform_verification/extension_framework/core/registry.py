"""
Centralized Plugin Registry with Dynamic Indexing, SemVer Tracking, and Capability Discovery.
"""
from typing import Dict, List, Optional
from app.platform_verification.extension_framework.domain.models import (
    PluginMetadata, PluginLifecycleState
)
from app.platform_verification.extension_framework.domain.interfaces import (
    VerificationPluginInterface, PluginRegistryInterface
)


class PluginRegistry(PluginRegistryInterface):
    def __init__(self):
        self._plugins: Dict[str, VerificationPluginInterface] = {}
        self._capability_index: Dict[str, List[str]] = {}

    def register_plugin(self, plugin: VerificationPluginInterface) -> PluginMetadata:
        meta = plugin.metadata
        self._plugins[meta.plugin_id] = plugin

        # Index capabilities
        for cap in meta.capabilities:
            if cap not in self._capability_index:
                self._capability_index[cap] = []
            if meta.plugin_id not in self._capability_index[cap]:
                self._capability_index[cap].append(meta.plugin_id)

        return meta

    def get_plugin(self, plugin_id: str) -> Optional[VerificationPluginInterface]:
        return self._plugins.get(plugin_id)

    def list_plugins(self, capability: Optional[str] = None) -> List[PluginMetadata]:
        if capability:
            plugin_ids = self._capability_index.get(capability, [])
            return [self._plugins[pid].metadata for pid in plugin_ids if pid in self._plugins]
        return [p.metadata for p in self._plugins.values()]

    def unregister_plugin(self, plugin_id: str) -> bool:
        if plugin_id in self._plugins:
            plugin = self._plugins.pop(plugin_id)
            for cap in plugin.metadata.capabilities:
                if cap in self._capability_index and plugin_id in self._capability_index[cap]:
                    self._capability_index[cap].remove(plugin_id)
            return True
        return False

    def list_all_capabilities(self) -> List[str]:
        return list(self._capability_index.keys())


plugin_registry = PluginRegistry()
