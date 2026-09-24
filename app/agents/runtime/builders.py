"""
Runtime Fluent Builders.
Provides declarative fluent builders for PlatformRuntimeConfig, Tenants, PluginManifests, and ModuleDescriptors.
"""

from typing import Any, Dict, List
from app.agents.runtime.configuration import PlatformRuntimeConfig
from app.agents.runtime.feature_flags import RuntimeFeatureFlags
from app.agents.runtime.module_registry import ModuleDescriptor
from app.agents.runtime.plugin_loader import PluginManifest
from app.agents.runtime.tenant import Tenant, TenantTier


class PlatformConfigBuilder:
    """Fluent builder for PlatformRuntimeConfig."""

    def __init__(self) -> None:
        self._environment = "DEV"
        self._max_concurrent_sessions = 1000
        self._startup_timeout = 60.0
        self._shutdown_drain = 30.0
        self._enable_supervisor = True
        self._feature_flags = RuntimeFeatureFlags()
        self._extra: Dict[str, Any] = {}

    def with_environment(self, env: str) -> "PlatformConfigBuilder":
        self._environment = env
        return self

    def with_max_concurrent_sessions(self, max_sessions: int) -> "PlatformConfigBuilder":
        self._max_concurrent_sessions = max_sessions
        return self

    def with_feature_flag(self, flag_name: str, value: bool) -> "PlatformConfigBuilder":
        self._feature_flags = self._feature_flags.set_flag(flag_name, value)
        return self

    def with_timeouts(self, startup: float, drain: float) -> "PlatformConfigBuilder":
        self._startup_timeout = startup
        self._shutdown_drain = drain
        return self

    def build(self) -> PlatformRuntimeConfig:
        return PlatformRuntimeConfig(
            environment=self._environment,
            max_concurrent_sessions=self._max_concurrent_sessions,
            startup_timeout_seconds=self._startup_timeout,
            shutdown_drain_seconds=self._shutdown_drain,
            enable_supervisor=self._enable_supervisor,
            feature_flags=self._feature_flags,
            extra_properties=self._extra,
        )


class TenantBuilder:
    """Fluent builder for Tenant."""

    def __init__(self, tenant_id: str, name: str) -> None:
        self._tenant_id = tenant_id
        self._name = name
        self._tier = TenantTier.ENTERPRISE
        self._max_concurrent_workflows = 100
        self._allowed_tools: List[str] = []

    def with_tier(self, tier: TenantTier) -> "TenantBuilder":
        self._tier = tier
        return self

    def with_max_workflows(self, max_wf: int) -> "TenantBuilder":
        self._max_concurrent_workflows = max_wf
        return self

    def with_allowed_tools(self, tools: List[str]) -> "TenantBuilder":
        self._allowed_tools = tools
        return self

    def build(self) -> Tenant:
        return Tenant(
            tenant_id=self._tenant_id,
            name=self._name,
            tier=self._tier,
            max_concurrent_workflows=self._max_concurrent_workflows,
            allowed_tools=self._allowed_tools,
        )


class PluginManifestBuilder:
    """Fluent builder for PluginManifest."""

    def __init__(self, plugin_id: str, name: str, entrypoint: str) -> None:
        self._plugin_id = plugin_id
        self._name = name
        self._entrypoint = entrypoint
        self._version = "1.0.0"
        self._author = "Enterprise Architecture"
        self._capabilities: List[str] = []
        self._config: Dict[str, Any] = {}

    def with_version(self, version: str) -> "PluginManifestBuilder":
        self._version = version
        return self

    def with_author(self, author: str) -> "PluginManifestBuilder":
        self._author = author
        return self

    def with_capability(self, capability: str) -> "PluginManifestBuilder":
        self._capabilities.append(capability)
        return self

    def with_config(self, key: str, value: Any) -> "PluginManifestBuilder":
        self._config[key] = value
        return self

    def build(self) -> PluginManifest:
        return PluginManifest(
            plugin_id=self._plugin_id,
            name=self._name,
            version=self._version,
            author=self._author,
            entrypoint=self._entrypoint,
            capabilities=self._capabilities,
            config=self._config,
        )


class ModuleDescriptorBuilder:
    """Fluent builder for ModuleDescriptor."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._version = "1.0.0"
        self._dependencies: List[str] = []
        self._description = ""

    def with_version(self, version: str) -> "ModuleDescriptorBuilder":
        self._version = version
        return self

    def depends_on(self, dependency: str) -> "ModuleDescriptorBuilder":
        self._dependencies.append(dependency)
        return self

    def with_description(self, description: str) -> "ModuleDescriptorBuilder":
        self._description = description
        return self

    def build(self) -> ModuleDescriptor:
        return ModuleDescriptor(
            name=self._name,
            version=self._version,
            dependencies=self._dependencies,
            description=self._description,
        )
