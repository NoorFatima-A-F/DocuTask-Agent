"""
Platform Kernel Foundation for DocuTask Agent.
Provides core contracts, interfaces, lifecycle definitions, and metadata protocols.
"""

from .contracts import Contract, VersionedContract
from .diagnostics import IDiagnosticProvider, DiagnosticReport
from .events import IKernelEvent, KernelEvent, KernelEventType
from .exceptions import (
    PlatformKernelException,
    BootstrapException,
    LifecycleException,
    ConfigurationException,
    DependencyResolutionException,
)
from .health import IHealthCheckable, ComponentHealth, HealthStatus
from .interfaces import (
    IKernel,
    IComponent,
    IService,
    IModule,
    IPlugin,
    ICapability,
)
from .lifecycle import (
    ILifecycle,
    LifecyclePhase,
    LifecycleState,
    LifecycleTransition,
)
from .metadata import (
    ComponentMetadata,
    ModuleMetadata,
    PluginMetadata,
    ServiceMetadata,
)
from .versioning import SemanticVersion, VersionRange

__all__ = [
    "Contract",
    "VersionedContract",
    "IDiagnosticProvider",
    "DiagnosticReport",
    "IKernelEvent",
    "KernelEvent",
    "KernelEventType",
    "PlatformKernelException",
    "BootstrapException",
    "LifecycleException",
    "ConfigurationException",
    "DependencyResolutionException",
    "IHealthCheckable",
    "ComponentHealth",
    "HealthStatus",
    "IKernel",
    "IComponent",
    "IService",
    "IModule",
    "IPlugin",
    "ICapability",
    "ILifecycle",
    "LifecyclePhase",
    "LifecycleState",
    "LifecycleTransition",
    "ComponentMetadata",
    "ModuleMetadata",
    "PluginMetadata",
    "ServiceMetadata",
    "SemanticVersion",
    "VersionRange",
]
