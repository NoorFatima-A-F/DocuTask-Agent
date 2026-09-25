"""
Enterprise Plugin Isolation Runtime.
Provides decoupled logical permissions and concrete runtime sandbox isolation engines.
"""

from app.agents.runtime.plugin_runtime.permission_manager import (
    PluginPermission,
    PluginPermissionManager,
)
from app.agents.runtime.plugin_runtime.resource_limiter import (
    PluginResourceLimitExceededError,
    PluginResourceLimiter,
)
from app.agents.runtime.plugin_runtime.isolation_policy import (
    PluginIsolationPolicy,
)
from app.agents.runtime.plugin_runtime.sandbox_provider import (
    DockerSandbox,
    LocalRestrictedSandbox,
    SandboxProvider,
    WasmSandbox,
)
from app.agents.runtime.plugin_runtime.plugin_executor import (
    PluginExecutionResult,
    PluginExecutor,
)

__all__ = [
    "PluginPermission",
    "PluginPermissionManager",
    "PluginResourceLimiter",
    "PluginResourceLimitExceededError",
    "PluginIsolationPolicy",
    "SandboxProvider",
    "LocalRestrictedSandbox",
    "DockerSandbox",
    "WasmSandbox",
    "PluginExecutor",
    "PluginExecutionResult",
]
