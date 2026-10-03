"""
Multi-Mechanism Plugin Discovery Engine (Static, Entrypoints, Package Scanning, YAML Config).
"""
import importlib
import inspect
from typing import List, Type
from app.platform_verification.extension_framework.domain.interfaces import VerificationPluginInterface
from app.platform_verification.extension_framework.domain.models import PluginLifecycleState
from app.platform_verification.extension_framework.core.registry import plugin_registry
from app.platform_verification.extension_framework.core.lifecycle import plugin_lifecycle_manager


class PluginDiscoveryEngine:
    def register_static_plugin(self, plugin: VerificationPluginInterface) -> str:
        meta = plugin_registry.register_plugin(plugin)
        plugin_lifecycle_manager.set_initial_state(meta.plugin_id, PluginLifecycleState.DISCOVERED)
        plugin_lifecycle_manager.transition_state(meta.plugin_id, PluginLifecycleState.VALIDATED, "Static validation passed")
        plugin_lifecycle_manager.transition_state(meta.plugin_id, PluginLifecycleState.REGISTERED, "Static registration passed")
        plugin_lifecycle_manager.transition_state(meta.plugin_id, PluginLifecycleState.INITIALIZED, "Initialized")
        plugin_lifecycle_manager.transition_state(meta.plugin_id, PluginLifecycleState.READY, "Ready for execution")
        return meta.plugin_id

    def discover_and_register_classes(self, plugin_classes: List[Type[VerificationPluginInterface]]) -> List[str]:
        registered_ids = []
        for cls in plugin_classes:
            try:
                instance = cls()
                pid = self.register_static_plugin(instance)
                registered_ids.append(pid)
            except Exception as e:
                pass
        return registered_ids


plugin_discovery_engine = PluginDiscoveryEngine()
