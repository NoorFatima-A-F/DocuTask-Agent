"""
Enterprise Agent Platform Runtime & Kernel Interfaces.
Defines the core abstract contracts for the runtime kernel, service registry, module loader,
plugin manager, dependency container, supervisor, and health monitoring.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar
from uuid import UUID

T = TypeVar("T")


class IKernel(ABC):
    """Core runtime kernel contract governing platform boot, module wiring, and lifecycle."""

    @abstractmethod
    async def boot(self) -> None:
        """Executes the deterministic boot sequence across all subsystems."""
        raise NotImplementedError

    @abstractmethod
    async def shutdown(self) -> None:
        """Gracefully drains and halts all running services and workers."""
        raise NotImplementedError

    @abstractmethod
    def is_running(self) -> bool:
        """Returns True if the kernel is in active RUNNING state."""
        raise NotImplementedError


class IServiceRegistry(ABC):
    """Central registry binding abstract interfaces to concrete subsystem instances."""

    @abstractmethod
    def register(self, interface_type: Type[T], instance: T, name: Optional[str] = None) -> None:
        """Registers a service instance under an interface type."""
        raise NotImplementedError

    @abstractmethod
    def resolve(self, interface_type: Type[T], name: Optional[str] = None) -> T:
        """Resolves a service instance by interface type or raises ServiceNotFoundError."""
        raise NotImplementedError

    @abstractmethod
    def has(self, interface_type: Type[T], name: Optional[str] = None) -> bool:
        """Checks if a service is registered."""
        raise NotImplementedError


class IServiceLocator(ABC):
    """Service locator contract for decoupled runtime resolution."""

    @abstractmethod
    def get(self, interface_type: Type[T], name: Optional[str] = None) -> T:
        """Retrieves registered service."""
        raise NotImplementedError


class IModuleLoader(ABC):
    """Contract for discovering, validating, and instantiating subsystem modules."""

    @abstractmethod
    def discover_modules(self) -> List[Any]:
        """Discovers all available platform modules."""
        raise NotImplementedError

    @abstractmethod
    async def load_module(self, descriptor: Any) -> Any:
        """Loads and initializes a discovered module."""
        raise NotImplementedError


class IPluginManager(ABC):
    """Contract for managing dynamic third-party and custom plugins."""

    @abstractmethod
    async def load_plugin(self, manifest_or_path: Any) -> Any:
        """Validates and loads a plugin into runtime."""
        raise NotImplementedError

    @abstractmethod
    async def unload_plugin(self, plugin_id: str) -> None:
        """Deactivates and removes a plugin."""
        raise NotImplementedError


class IRuntimeSupervisor(ABC):
    """Erlang OTP-style supervision contract monitoring subsystem health and restarts."""

    @abstractmethod
    async def supervise(self, module_name: str, coroutine_fn: Callable[[], Any]) -> Any:
        """Runs a subsystem under supervised recovery."""
        raise NotImplementedError

    @abstractmethod
    async def restart_subsystem(self, module_name: str) -> None:
        """Restarts a failed subsystem and restores its state."""
        raise NotImplementedError


class IHealthMonitor(ABC):
    """Contract for collecting and aggregating subsystem health states."""

    @abstractmethod
    async def check_health(self) -> Any:
        """Returns aggregate platform health status."""
        raise NotImplementedError


class IRuntimePlatform(ABC):
    """High-level platform runtime host contract."""

    @abstractmethod
    async def start(self) -> None:
        """Starts platform runtime."""
        raise NotImplementedError

    @abstractmethod
    async def stop(self) -> None:
        """Stops platform runtime."""
        raise NotImplementedError


class IRuntimeLifecycle(ABC):
    """Lifecycle contract for components governed by the runtime state machine."""

    @abstractmethod
    async def initialize(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def shutdown(self) -> None:
        raise NotImplementedError

