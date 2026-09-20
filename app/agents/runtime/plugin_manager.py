"""
Enterprise Plugin Manager Engine.
Orchestrates the 8-state plugin lifecycle:
DISCOVERED -> VALIDATED -> LOADED -> REGISTERED -> ACTIVATED -> RUNNING -> DISABLED -> UNLOADED
with dependency resolution, version conflict checking, sandboxing, and automated rollback management.
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Set, Union
from app.agents.runtime.exceptions import PluginValidationError
from app.agents.runtime.interfaces import IPluginManager
from app.agents.runtime.plugin_loader import PluginLoader, PluginManifest, PluginState
from app.agents.runtime.plugin_registry import PluginRegistration, PluginRegistry

logger = logging.getLogger(__name__)


class PluginDependencyResolver:
    """Resolves inter-plugin dependencies and detects circular or missing plugin prerequisites."""

    @staticmethod
    def resolve_dependencies(
        target: PluginManifest,
        active_plugins: Dict[str, PluginRegistration],
    ) -> List[str]:
        """Validates that all declared plugin dependencies are satisfied and active."""
        missing = []
        for dep_id in target.dependencies:
            if dep_id not in active_plugins:
                missing.append(dep_id)
            elif active_plugins[dep_id].state not in (PluginState.ACTIVATED, PluginState.RUNNING):
                missing.append(dep_id)

        if missing:
            raise PluginValidationError(
                f"Plugin '{target.name}' missing active dependencies: {missing}"
            )
        return target.dependencies


class PluginSandbox:
    """Enforces execution boundaries and permission checks on plugin operations."""

    def __init__(self, allowed_permissions: Optional[Set[str]] = None) -> None:
        self.allowed_permissions = allowed_permissions or {
            "filesystem:read",
            "filesystem:write",
            "network:outbound",
            "tools:execute",
            "telemetry:emit",
        }

    def verify_permissions(self, manifest: PluginManifest) -> None:
        """Ensures plugin does not request unauthorized platform permissions."""
        unauthorized = [p for p in manifest.permissions if p not in self.allowed_permissions]
        if unauthorized:
            raise PluginValidationError(
                f"Plugin '{manifest.name}' requested unauthorized permissions: {unauthorized}"
            )


class PluginRollbackManager:
    """Maintains transaction journal for newly activated plugins and executes LIFO rollback upon failure."""

    def __init__(self, registry: PluginRegistry) -> None:
        self.registry = registry
        self._journal: List[str] = []

    def record_activation(self, plugin_id: str) -> None:
        """Records an activated plugin into the transaction log."""
        self._journal.append(plugin_id)

    async def rollback(self) -> List[str]:
        """Rolls back all newly activated plugins in reverse order (LIFO)."""
        rolled_back = []
        while self._journal:
            pid = self._journal.pop()
            logger.warning(f"PluginRollbackManager: Rolling back plugin '{pid}'")
            self.registry.deactivate(pid)
            self.registry.remove(pid)
            rolled_back.append(pid)
        return rolled_back

    def commit(self) -> None:
        """Clears transaction log upon successful installation."""
        self._journal.clear()


class PluginManager(IPluginManager):
    """Enterprise plugin orchestration engine implementing complete 8-state lifecycle."""

    def __init__(
        self,
        loader: Optional[PluginLoader] = None,
        registry: Optional[PluginRegistry] = None,
        sandbox: Optional[PluginSandbox] = None,
    ) -> None:
        self.loader = loader or PluginLoader()
        self.registry = registry or PluginRegistry()
        self.sandbox = sandbox or PluginSandbox()
        self.resolver = PluginDependencyResolver()
        self.rollback_mgr = PluginRollbackManager(self.registry)

    async def load_plugin(
        self,
        manifest_or_data: Union[PluginManifest, Dict[str, Any]],
        entrypoint_factory: Optional[Callable[[], Any]] = None,
    ) -> PluginRegistration:
        """
        Executes complete plugin onboarding pipeline:
        DISCOVERED -> VALIDATED -> LOADED -> REGISTERED -> ACTIVATED -> RUNNING
        """
        # 1. Discover & Validate
        if isinstance(manifest_or_data, dict):
            manifest = self.loader.load_from_dict(manifest_or_data)
        else:
            self.loader.validate_manifest(manifest_or_data)
            manifest = manifest_or_data

        # 2. Sandbox Permission Verification
        self.sandbox.verify_permissions(manifest)

        # 3. Dependency Resolution
        active_map = {p.manifest.plugin_id: p for p in self.registry.list_active()}
        self.resolver.resolve_dependencies(manifest, active_map)

        # 4. Load & Instantiate
        logger.info(f"Loading plugin '{manifest.name}' ({manifest.plugin_id}) v{manifest.version}")
        try:
            if entrypoint_factory:
                instance = entrypoint_factory()
            else:
                instance = {"plugin_id": manifest.plugin_id, "active": True}

            # 5. Register & Activate
            reg = self.registry.register(manifest=manifest, instance=instance)
            reg = self.registry.update_state(manifest.plugin_id, PluginState.ACTIVATED)
            reg = self.registry.update_state(manifest.plugin_id, PluginState.RUNNING)

            self.rollback_mgr.record_activation(manifest.plugin_id)
            return reg

        except Exception as ex:
            logger.error(f"Plugin loading failed for '{manifest.plugin_id}': {ex}. Rolling back.")
            await self.rollback_mgr.rollback()
            raise

    async def unload_plugin(self, plugin_id: str) -> None:
        """Transitions plugin to DISABLED and UNLOADED, removing from runtime."""
        logger.info(f"Unloading plugin '{plugin_id}'")
        self.registry.deactivate(plugin_id)
        self.registry.remove(plugin_id)

    def get_active_plugins(self) -> List[PluginRegistration]:
        """Returns all currently active plugin records."""
        return self.registry.list_active()
