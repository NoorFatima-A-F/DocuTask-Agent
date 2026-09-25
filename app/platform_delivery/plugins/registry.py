"""Plugin Registry Management."""
from typing import Dict, List, Optional
from .contracts import PlatformPlugin
from .lifecycle import PluginLifecycleState
from .sandbox import PluginSandbox


class PluginRegistry:
    """Central manager for plugin discovery, approval, activation, and invocation."""

    def __init__(self, sandbox: Optional[PluginSandbox] = None):
        self.sandbox = sandbox or PluginSandbox()
        self._plugins: Dict[str, PlatformPlugin] = {}
        self._states: Dict[str, PluginLifecycleState] = {}

    def register_plugin(self, plugin: PlatformPlugin) -> None:
        meta = plugin.metadata()
        if not self.sandbox.check_permissions(meta.declared_permissions):
            raise PermissionError(f"Plugin '{meta.name}' requested disallowed sandbox permissions: {meta.declared_permissions}")

        self._plugins[meta.plugin_id] = plugin
        self._states[meta.plugin_id] = PluginLifecycleState.REGISTERED

    def activate_plugin(self, plugin_id: str, context: Optional[Dict] = None) -> None:
        plugin = self._plugins.get(plugin_id)
        if not plugin:
            raise KeyError(f"Plugin '{plugin_id}' not found")
        plugin.initialize(context or {})
        self._states[plugin_id] = PluginLifecycleState.ACTIVE

    def get_plugin(self, plugin_id: str) -> Optional[PlatformPlugin]:
        return self._plugins.get(plugin_id)

    def list_plugins(self) -> List[Dict[str, str]]:
        return [
            {
                "plugin_id": pid,
                "name": p.metadata().name,
                "version": p.metadata().version,
                "state": self._states.get(pid, PluginLifecycleState.DISCOVERED).value,
            }
            for pid, p in self._plugins.items()
        ]
