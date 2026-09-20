"""
Service Locator.
Provides decoupled access to registered platform services without direct dependency coupling.
"""

from typing import Any, Optional, Type, TypeVar
from app.agents.runtime.interfaces import IServiceLocator, IServiceRegistry
from app.agents.runtime.service_registry import ServiceRegistry

T = TypeVar("T")


class ServiceLocator(IServiceLocator):
    """Facade for resolving platform services from a backing ServiceRegistry."""

    _global_registry: Optional[IServiceRegistry] = None

    def __init__(self, registry: Optional[IServiceRegistry] = None) -> None:
        self._registry = registry or ServiceLocator._global_registry or ServiceRegistry()

    @classmethod
    def set_global_registry(cls, registry: IServiceRegistry) -> None:
        """Sets the process-wide global service registry."""
        cls._global_registry = registry

    def get(self, interface_type: Type[T], name: Optional[str] = None) -> T:
        """Resolves the service by interface."""
        return self._registry.resolve(interface_type, name=name)

    def has(self, interface_type: Type[T], name: Optional[str] = None) -> bool:
        """Checks if service is registered."""
        return self._registry.has(interface_type, name=name)
