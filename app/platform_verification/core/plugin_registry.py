"""
Plugin Registry & Dynamic Discovery Engine
"""
from typing import Dict, List, Optional
from app.platform_verification.domain.interfaces import VerificationPlugin
from app.platform_verification.domain.exceptions import PluginNotFoundException

class PluginRegistry:
    def __init__(self):
        self._plugins: Dict[str, VerificationPlugin] = {}

    def register_plugin(self, plugin: VerificationPlugin) -> None:
        self._plugins[plugin.plugin_name] = plugin

    def get_plugin(self, plugin_name: str) -> VerificationPlugin:
        if plugin_name not in self._plugins:
            raise PluginNotFoundException(f"Plugin '{plugin_name}' is not registered in verification platform.")
        return self._plugins[plugin_name]

    def list_plugins(self) -> List[Dict[str, str]]:
        return [
            {"plugin_name": p.plugin_name, "target_domain": p.target_domain}
            for p in self._plugins.values()
        ]

plugin_registry = PluginRegistry()
