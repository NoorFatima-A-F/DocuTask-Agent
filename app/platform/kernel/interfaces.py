"""
Core Platform Kernel Interfaces.
Defines foundational abstractions for components, services, modules, plugins, and capabilities.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable
from .metadata import ComponentMetadata, ModuleMetadata, PluginMetadata, ServiceMetadata
from .health import ComponentHealth
from .diagnostics import DiagnosticReport


@runtime_checkable
class IComponent(Protocol):
    """Universal protocol for all managed components within the platform kernel."""

    @property
    def component_id(self) -> str:
        """Unique identifier of the component."""
        ...

    @property
    def metadata(self) -> ComponentMetadata:
        """Component metadata."""
        ...


@runtime_checkable
class IService(Protocol):
    """Protocol for platform services registered within the ServiceRegistry."""

    @property
    def service_name(self) -> str:
        """Canonical name of the service."""
        ...

    @property
    def version(self) -> str:
        """Service version."""
        ...

    @property
    def metadata(self) -> ServiceMetadata:
        """Service metadata."""
        ...


@runtime_checkable
class ICapability(Protocol):
    """Protocol for an advertised capability within the CapabilityRegistry."""

    @property
    def capability_name(self) -> str:
        """Name of the capability (e.g., 'document.ocr', 'ai.embedding')."""
        ...

    @property
    def provider_name(self) -> str:
        """Provider component/module name advertising this capability."""
        ...

    @property
    def version(self) -> str:
        """Capability version."""
        ...

    @property
    def attributes(self) -> Dict[str, Any]:
        """Additional capability attributes and configuration schema."""
        ...


@runtime_checkable
class IModule(Protocol):
    """Protocol for dynamic modules managed by the ModuleManager."""

    @property
    def module_name(self) -> str:
        """Canonical module name."""
        ...

    @property
    def metadata(self) -> ModuleMetadata:
        """Module metadata."""
        ...

    async def initialize(self, context: Any) -> None:
        """Initialize the module with runtime context."""
        ...

    async def start(self) -> None:
        """Start module operations."""
        ...

    async def stop(self) -> None:
        """Stop module operations."""
        ...


@runtime_checkable
class IPlugin(Protocol):
    """Protocol for dynamic plugins loaded into the PluginRegistry."""

    @property
    def plugin_id(self) -> str:
        """Unique plugin ID."""
        ...

    @property
    def metadata(self) -> PluginMetadata:
        """Plugin manifest metadata."""
        ...

    async def on_load(self, kernel: Any) -> None:
        """Lifecycle hook invoked when plugin is loaded into the kernel."""
        ...

    async def on_unload(self) -> None:
        """Lifecycle hook invoked when plugin is unloaded."""
        ...


class IKernel(ABC):
    """Core Platform Kernel interface."""

    @abstractmethod
    def get_component(self, component_id: str) -> Optional[IComponent]:
        """Retrieve a registered component by its ID."""
        pass

    @abstractmethod
    def list_components(self) -> List[IComponent]:
        """List all active components in the kernel."""
        pass

    @abstractmethod
    async def get_health(self) -> ComponentHealth:
        """Get aggregate kernel health."""
        pass

    @abstractmethod
    async def get_diagnostics(self) -> DiagnosticReport:
        """Get kernel diagnostic report."""
        pass
