"""
Enterprise Agent Platform Runtime & Kernel.
Central control plane governing agent lifecycle, dependency graphs, service registry,
module discovery, dynamic plugin loading, Erlang OTP supervision, and multi-tenancy.
"""

from app.agents.runtime.bootstrap import PlatformBootstrapper
from app.agents.runtime.builders import (
    ModuleDescriptorBuilder,
    PlatformConfigBuilder,
    PluginManifestBuilder,
    TenantBuilder,
)
from app.agents.runtime.configuration import PlatformRuntimeConfig
from app.agents.runtime.dependency_container import DependencyContainer, Lifetime
from app.agents.runtime.dependency_graph import DependencyGraph
from app.agents.runtime.dependency_manager import DependencyManager
from app.agents.runtime.environment import EnvironmentPolicy, EnvironmentType
from app.agents.runtime.events import (
    HealthDegradedEvent,
    ModuleDiscoveredEvent,
    PluginLoadedEvent,
    RuntimeBootCompletedEvent,
    RuntimeBootStartedEvent,
    RuntimeTerminatedEvent,
    ShutdownInitiatedEvent,
    SubsystemRegisteredEvent,
    SupervisorRestartTriggeredEvent,
)
from app.agents.runtime.exceptions import (
    ConfigurationValidationError,
    CyclicDependencyError,
    DuplicateServiceRegistrationError,
    FeatureFlagEvaluationError,
    InvalidRuntimeStateTransitionError,
    ModuleLoadError,
    PluginValidationError,
    RuntimeKernelException,
    ServiceNotFoundError,
    SubsystemCrashError,
    TenantIsolationViolationError,
)
from app.agents.runtime.factory import RuntimeFactory
from app.agents.runtime.feature_flags import RuntimeFeatureFlags
from app.agents.runtime.initializer import SubsystemInitializer
from app.agents.runtime.interfaces import (
    IHealthMonitor,
    IKernel,
    IModuleLoader,
    IPluginManager,
    IRuntimeLifecycle,
    IRuntimePlatform,
    IRuntimeSupervisor,
    IServiceLocator,
    IServiceRegistry,
)
from app.agents.runtime.kernel import RuntimeKernel
from app.agents.runtime.module_loader import ModuleLoader
from app.agents.runtime.module_registry import ModuleDescriptor, ModuleRegistry
from app.agents.runtime.platform import Platform
from app.agents.runtime.plugin_loader import PluginLoader, PluginManifest
from app.agents.runtime.plugin_manager import PluginManager
from app.agents.runtime.plugin_registry import PluginRegistration, PluginRegistry
from app.agents.runtime.runtime import PlatformRuntime
from app.agents.runtime.runtime_cache import RuntimeCache
from app.agents.runtime.runtime_context import RuntimeContext
from app.agents.runtime.runtime_health import (
    PlatformHealthReport,
    SubsystemHealthReport,
    SubsystemHealthStatus,
)
from app.agents.runtime.runtime_lifecycle import (
    RuntimeLifecycleState,
    RuntimeLifecycleStateMachine,
)
from app.agents.runtime.runtime_metrics import (
    RuntimeMetricsCollector,
    RuntimeMetricsSnapshot,
)
from app.agents.runtime.runtime_monitor import RuntimeMonitor
from app.agents.runtime.runtime_repository import (
    IRuntimeRepository,
    InMemoryRuntimeRepository,
)
from app.agents.runtime.runtime_serialization import RuntimeSerializer
from app.agents.runtime.runtime_session import RuntimeSession
from app.agents.runtime.runtime_state import RuntimeState
from app.agents.runtime.runtime_supervisor import RuntimeSupervisor
from app.agents.runtime.runtime_validation import (
    RuntimeValidationReport,
    RuntimeValidator,
)
from app.agents.runtime.service_locator import ServiceLocator
from app.agents.runtime.service_registry import ServiceRegistry
from app.agents.runtime.shutdown import ShutdownPipeline
from app.agents.runtime.startup import StartupPipeline
from app.agents.runtime.tenant import Tenant, TenantTier
from app.agents.runtime.tenant_manager import TenantManager
from app.agents.runtime.workspace import WorkspaceManager

__all__ = [
    # Interfaces
    "IKernel",
    "IRuntimePlatform",
    "IServiceRegistry",
    "IServiceLocator",
    "IModuleLoader",
    "IPluginManager",
    "IRuntimeSupervisor",
    "IHealthMonitor",
    # Core Kernel & Platform
    "RuntimeKernel",
    "Platform",
    "PlatformRuntime",
    "RuntimeFactory",
    # Lifecycle & Context
    "RuntimeLifecycleState",
    "RuntimeLifecycleStateMachine",
    "RuntimeState",
    "RuntimeContext",
    "RuntimeSession",
    # Dependency & IoC
    "DependencyGraph",
    "DependencyManager",
    "DependencyContainer",
    "Lifetime",
    # Registry & Locator
    "ServiceRegistry",
    "ServiceLocator",
    # Modules & Plugins
    "ModuleDescriptor",
    "ModuleRegistry",
    "ModuleLoader",
    "PluginManifest",
    "PluginLoader",
    "PluginRegistration",
    "PluginRegistry",
    "PluginManager",
    # Supervision & Health
    "RuntimeSupervisor",
    "SubsystemHealthStatus",
    "SubsystemHealthReport",
    "PlatformHealthReport",
    "RuntimeMonitor",
    "RuntimeMetricsCollector",
    "RuntimeMetricsSnapshot",
    # Tenancy, Workspace & Environment
    "Tenant",
    "TenantTier",
    "TenantManager",
    "WorkspaceManager",
    "EnvironmentType",
    "EnvironmentPolicy",
    "PlatformRuntimeConfig",
    "RuntimeFeatureFlags",
    # Pipelines & Bootstrapping
    "PlatformBootstrapper",
    "SubsystemInitializer",
    "StartupPipeline",
    "ShutdownPipeline",
    # Storage, Serialization, Caching, Validation
    "RuntimeCache",
    "IRuntimeRepository",
    "InMemoryRuntimeRepository",
    "RuntimeSerializer",
    "RuntimeValidator",
    "RuntimeValidationReport",
    # Builders
    "PlatformConfigBuilder",
    "TenantBuilder",
    "PluginManifestBuilder",
    "ModuleDescriptorBuilder",
    # Exceptions
    "RuntimeKernelException",
    "ServiceNotFoundError",
    "DuplicateServiceRegistrationError",
    "CyclicDependencyError",
    "ModuleLoadError",
    "PluginValidationError",
    "InvalidRuntimeStateTransitionError",
    "SubsystemCrashError",
    "TenantIsolationViolationError",
    "FeatureFlagEvaluationError",
    "ConfigurationValidationError",
    # Events
    "RuntimeBootStartedEvent",
    "RuntimeBootCompletedEvent",
    "SubsystemRegisteredEvent",
    "ModuleDiscoveredEvent",
    "PluginLoadedEvent",
    "HealthDegradedEvent",
    "SupervisorRestartTriggeredEvent",
    "ShutdownInitiatedEvent",
    "RuntimeTerminatedEvent",
]
