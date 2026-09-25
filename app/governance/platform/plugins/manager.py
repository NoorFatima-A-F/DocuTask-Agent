"""Enterprise Plugin Manager orchestrating registration, lifecycle, and sandboxed execution."""

from typing import Any, Dict, List, Optional, Set

from .lifecycle import PluginLifecycleStateMachine, PluginState
from .registry import PluginMetadata, PluginRegistry
from .sandbox import GovernancePlugin, PluginSandbox, SandboxExecutionResult


class PluginManager:
    """Central orchestrator for the governance plugin ecosystem."""

    def __init__(self, registry: Optional[PluginRegistry] = None) -> None:
        self.registry = registry or PluginRegistry()

    def register(
        self,
        plugin: GovernancePlugin,
        owner: str,
        tenant_id: str,
        capabilities: Optional[List[str]] = None,
        permissions: Optional[Set[str]] = None,
    ) -> PluginMetadata:
        """Register a new plugin."""
        return self.registry.register_plugin(
            plugin_instance=plugin,
            owner=owner,
            tenant_id=tenant_id,
            capabilities=capabilities,
            permissions=permissions,
        )

    def validate(self, plugin_id: str) -> PluginMetadata:
        """Run validation on registered plugin and transition state to VALIDATED."""
        meta = self.registry.get_plugin_metadata(plugin_id)
        inst = self.registry.get_plugin_instance(plugin_id)
        if not meta or not inst:
            raise ValueError(f"Plugin {plugin_id} not found.")

        # Run instance self-validation
        is_valid = inst.validate()
        if not is_valid:
            raise ValueError(f"Plugin {plugin_id} failed self-validation check.")

        new_state = PluginLifecycleStateMachine.transition(meta.state, PluginState.VALIDATED)
        updated = self.registry.update_state(plugin_id, new_state)
        return updated or meta

    def approve(self, plugin_id: str) -> PluginMetadata:
        """Approve validated plugin for tenant activation."""
        meta = self.registry.get_plugin_metadata(plugin_id)
        if not meta:
            raise ValueError(f"Plugin {plugin_id} not found.")

        new_state = PluginLifecycleStateMachine.transition(meta.state, PluginState.APPROVED)
        updated = self.registry.update_state(plugin_id, new_state)
        return updated or meta

    def activate(self, plugin_id: str, config: Optional[Dict[str, Any]] = None) -> PluginMetadata:
        """Initialize and activate approved plugin."""
        meta = self.registry.get_plugin_metadata(plugin_id)
        inst = self.registry.get_plugin_instance(plugin_id)
        if not meta or not inst:
            raise ValueError(f"Plugin {plugin_id} not found.")

        # Initialize instance
        inst.initialize(config or {})
        inst.initialized = True

        new_state = PluginLifecycleStateMachine.transition(meta.state, PluginState.ACTIVE)
        updated = self.registry.update_state(plugin_id, new_state)
        return updated or meta

    def disable(self, plugin_id: str) -> PluginMetadata:
        """Disable active plugin."""
        meta = self.registry.get_plugin_metadata(plugin_id)
        if not meta:
            raise ValueError(f"Plugin {plugin_id} not found.")

        new_state = PluginLifecycleStateMachine.transition(meta.state, PluginState.DISABLED)
        updated = self.registry.update_state(plugin_id, new_state)
        return updated or meta

    def remove(self, plugin_id: str) -> bool:
        """Shutdown and remove plugin."""
        meta = self.registry.get_plugin_metadata(plugin_id)
        inst = self.registry.get_plugin_instance(plugin_id)
        if not meta:
            return False

        if inst:
            inst.shutdown()

        self.registry.update_state(plugin_id, PluginState.REMOVED)
        return self.registry.unregister(plugin_id)

    def dispatch_hook(
        self,
        hook_name: str,
        payload: Dict[str, Any],
        tenant_id: Optional[str] = None,
    ) -> List[SandboxExecutionResult]:
        """Dispatch governance hook to all active, approved plugins for tenant."""
        active_plugins = self.registry.list_plugins(tenant_id=tenant_id, state=PluginState.ACTIVE)
        results: List[SandboxExecutionResult] = []

        for meta in active_plugins:
            inst = self.registry.get_plugin_instance(meta.plugin_id)
            if not inst:
                continue

            sandbox = PluginSandbox(allowed_permissions=meta.permissions)
            res = sandbox.run_sandboxed(
                plugin=inst,
                hook_name=hook_name,
                payload=payload,
            )
            results.append(res)

        return results
