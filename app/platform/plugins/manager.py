"""
Platform Plugin Manager.
Orchestrates plugin registration, validation, activation, and deactivation.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from .models import PluginManifest, PluginRecord, PluginStatus, PluginType
from .registry import PluginRegistry
from .validator import PluginValidator
from ..kernel.exceptions import PluginException


class PluginManager:
    """Central manager for plugin loading and lifecycle."""

    def __init__(self, registry: Optional[PluginRegistry] = None):
        self.registry = registry or PluginRegistry()
        self.validator = PluginValidator()

    def register_plugin(
        self,
        manifest: PluginManifest,
        instance: Optional[Any] = None,
        configuration: Optional[Dict[str, Any]] = None,
    ) -> PluginRecord:
        """Register and validate a new plugin."""
        self.validator.validate_manifest(manifest)
        record = PluginRecord(
            manifest=manifest,
            status=PluginStatus.VALIDATED,
            instance=instance,
            loaded_at=datetime.now(timezone.utc),
            configuration=configuration or {},
        )
        self.registry.register(record)
        return record

    async def enable_plugin(self, plugin_id: str, kernel_context: Optional[Any] = None) -> None:
        """Enable and activate a plugin."""
        record = self.registry.get(plugin_id)
        if not record:
            raise PluginException(f"Plugin '{plugin_id}' not registered")

        if record.instance and hasattr(record.instance, "on_load"):
            await record.instance.on_load(kernel_context)

        self.registry.update_status(plugin_id, PluginStatus.ACTIVE)

    async def disable_plugin(self, plugin_id: str) -> None:
        """Disable an active plugin."""
        record = self.registry.get(plugin_id)
        if not record:
            return

        if record.instance and hasattr(record.instance, "on_unload"):
            await record.instance.on_unload()

        self.registry.update_status(plugin_id, PluginStatus.DISABLED)

    async def unload_plugin(self, plugin_id: str) -> None:
        """Unload and unregister plugin."""
        await self.disable_plugin(plugin_id)
        self.registry.unregister(plugin_id)
