"""
Platform Plugin Registry.
"""

from typing import Dict, List, Optional
from .models import PluginRecord, PluginStatus, PluginType
from ..kernel.exceptions import PluginException


class PluginRegistry:
    """Registry maintaining registered and active plugin records."""

    def __init__(self):
        self._plugins: Dict[str, PluginRecord] = {}

    def register(self, record: PluginRecord) -> None:
        """Register a plugin record."""
        self._plugins[record.manifest.id] = record

    def get(self, plugin_id: str) -> Optional[PluginRecord]:
        """Get plugin record by ID."""
        return self._plugins.get(plugin_id)

    def list_plugins(self, plugin_type: Optional[PluginType] = None) -> List[PluginRecord]:
        """List all plugins, optionally filtered by plugin type."""
        if plugin_type is None:
            return list(self._plugins.values())
        return [p for p in self._plugins.values() if p.manifest.plugin_type == plugin_type]

    def update_status(self, plugin_id: str, status: PluginStatus, error_message: Optional[str] = None) -> None:
        """Update status of a plugin."""
        rec = self._plugins.get(plugin_id)
        if not rec:
            raise PluginException(f"Plugin '{plugin_id}' not found in registry")
        rec.status = status
        if error_message:
            rec.error_message = error_message

    def unregister(self, plugin_id: str) -> None:
        """Unregister a plugin."""
        self._plugins.pop(plugin_id, None)
