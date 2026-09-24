"""
Plugin Executor Engine.
Coordinates permission checking, resource bounds enforcement, and sandbox provider invocation.
"""

from typing import Any, Callable, Coroutine, List, Optional
from pydantic import BaseModel
from app.agents.runtime.plugin_runtime.isolation_policy import PluginIsolationPolicy
from app.agents.runtime.plugin_runtime.permission_manager import PluginPermissionManager
from app.agents.runtime.plugin_runtime.resource_limiter import PluginResourceLimiter
from app.agents.runtime.plugin_runtime.sandbox_provider import LocalRestrictedSandbox, SandboxProvider


class PluginExecutionResult(BaseModel):
    """Result of sandboxed plugin execution."""
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0


class PluginExecutor:
    """Orchestrates secure sandboxed execution for runtime plugins."""

    def __init__(
        self,
        permission_manager: Optional[PluginPermissionManager] = None,
        resource_limiter: Optional[PluginResourceLimiter] = None,
        sandbox: Optional[SandboxProvider] = None,
        policy: Optional[PluginIsolationPolicy] = None,
    ) -> None:
        self.permission_manager = permission_manager or PluginPermissionManager()
        self.resource_limiter = resource_limiter or PluginResourceLimiter()
        self.sandbox = sandbox or LocalRestrictedSandbox()
        self.policy = policy or PluginIsolationPolicy()

    async def execute(
        self,
        plugin_id: str,
        action: Callable[[], Coroutine[Any, Any, Any]],
        declared_permissions: Optional[List[str]] = None,
    ) -> Any:
        """Enforces permissions, bounds resources, and executes inside sandbox."""
        # 1. Logical Permission Check
        if declared_permissions:
            self.permission_manager.verify_permissions(declared_permissions)

        # 2. Resource & Sandbox Execution
        async def _sandboxed_action():
            return await self.sandbox.execute_plugin(action, self.policy)

        return await self.resource_limiter.execute_bounded(_sandboxed_action)
