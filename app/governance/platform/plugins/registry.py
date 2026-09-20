"""Plugin Registry and Metadata Management."""

from datetime import datetime, timezone
import secrets
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from .lifecycle import PluginState
from .sandbox import GovernancePlugin


class PluginMetadata(BaseModel):
    """Metadata record for a registered governance plugin."""

    plugin_id: str
    name: str
    version: str
    owner: str
    tenant_id: str
    description: str = ""
    capabilities: List[str] = Field(default_factory=list)
    permissions: Set[str] = Field(default_factory=set)
    state: PluginState = PluginState.REGISTERED
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PluginRegistry:
    """Multi-tenant plugin repository and index."""

    def __init__(self) -> None:
        self._plugins: Dict[str, PluginMetadata] = {}
        self._instances: Dict[str, GovernancePlugin] = {}

    def register_plugin(
        self,
        plugin_instance: GovernancePlugin,
        owner: str,
        tenant_id: str,
        capabilities: Optional[List[str]] = None,
        permissions: Optional[Set[str]] = None,
    ) -> PluginMetadata:
        """Register a new plugin in REGISTERED state."""
        plugin_id = f"plug_{secrets.token_hex(8)}"
        meta = PluginMetadata(
            plugin_id=plugin_id,
            name=plugin_instance.name,
            version=plugin_instance.version,
            owner=owner,
            tenant_id=tenant_id,
            description=plugin_instance.description,
            capabilities=capabilities or ["policy.rule", "analytics.hook"],
            permissions=permissions or {"governance:plugin:read"},
            state=PluginState.REGISTERED,
        )
        self._plugins[plugin_id] = meta
        self._instances[plugin_id] = plugin_instance
        return meta

    def get_plugin_metadata(self, plugin_id: str) -> Optional[PluginMetadata]:
        return self._plugins.get(plugin_id)

    def get_plugin_instance(self, plugin_id: str) -> Optional[GovernancePlugin]:
        return self._instances.get(plugin_id)

    def list_plugins(
        self,
        tenant_id: Optional[str] = None,
        state: Optional[PluginState] = None,
    ) -> List[PluginMetadata]:
        """List registered plugins."""
        results = list(self._plugins.values())
        if tenant_id:
            results = [p for p in results if p.tenant_id == tenant_id]
        if state:
            results = [p for p in results if p.state == state]
        return results

    def update_state(self, plugin_id: str, target_state: PluginState) -> Optional[PluginMetadata]:
        """Update plugin state."""
        meta = self._plugins.get(plugin_id)
        if meta:
            meta.state = target_state
            meta.updated_at = datetime.now(timezone.utc)
            return meta
        return None

    def unregister(self, plugin_id: str) -> bool:
        """Remove plugin."""
        if plugin_id in self._plugins:
            del self._plugins[plugin_id]
            self._instances.pop(plugin_id, None)
            return True
        return False
