"""
Plugin Registry.
Tracks lifecycle state transitions, manifest metadata, and active instances of all installed plugins.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.agents.runtime.plugin_loader import PluginManifest, PluginState


class PluginRegistration(BaseModel):
    """Runtime registration record of an installed plugin."""
    manifest: PluginManifest
    state: PluginState = PluginState.DISCOVERED
    instance: Optional[Any] = None
    installed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def status(self) -> str:
        """Backward compatibility with status string."""
        return "ACTIVE" if self.state in (PluginState.ACTIVATED, PluginState.RUNNING) else "INACTIVE"

    def transition_to(self, new_state: PluginState) -> "PluginRegistration":
        """Advances plugin lifecycle state."""
        return self.model_copy(update={"state": new_state})

    model_config = {"frozen": True}


class PluginRegistry:
    """Registry maintaining lifecycle states and instances of installed plugins."""

    def __init__(self) -> None:
        self._plugins: Dict[str, PluginRegistration] = {}

    def register(self, manifest: PluginManifest, instance: Optional[Any] = None) -> PluginRegistration:
        """Registers a validated plugin in REGISTERED state."""
        reg = PluginRegistration(
            manifest=manifest,
            state=PluginState.REGISTERED,
            instance=instance,
        )
        self._plugins[manifest.plugin_id] = reg
        return reg

    def update_state(self, plugin_id: str, new_state: PluginState) -> Optional[PluginRegistration]:
        """Updates plugin lifecycle state."""
        reg = self._plugins.get(plugin_id)
        if not reg:
            return None
        updated = reg.transition_to(new_state)
        self._plugins[plugin_id] = updated
        return updated

    def get(self, plugin_id: str) -> Optional[PluginRegistration]:
        """Retrieves plugin registration by ID."""
        return self._plugins.get(plugin_id)

    def list_all(self) -> List[PluginRegistration]:
        """Returns all registered plugins."""
        return list(self._plugins.values())

    def list_active(self) -> List[PluginRegistration]:
        """Returns all currently active or running plugins."""
        return [
            p for p in self._plugins.values()
            if p.state in (PluginState.ACTIVATED, PluginState.RUNNING) and p.manifest.enabled
        ]

    def deactivate(self, plugin_id: str) -> bool:
        """Transitions plugin to DISABLED state."""
        if plugin_id in self._plugins:
            self.update_state(plugin_id, PluginState.DISABLED)
            return True
        return False

    def remove(self, plugin_id: str) -> bool:
        """Transitions to UNLOADED and removes from registry."""
        if plugin_id in self._plugins:
            self.update_state(plugin_id, PluginState.UNLOADED)
            self._plugins.pop(plugin_id, None)
            return True
        return False

    def count(self) -> int:
        """Total number of installed plugins."""
        return len(self._plugins)
