"""
Service Registry.
Implements IServiceRegistry; provides centralized, type-safe registry of all platform subsystem engines and facades.
"""

from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar
from app.agents.runtime.exceptions import (
    DuplicateServiceRegistrationError,
    ServiceNotFoundError,
)
from app.agents.runtime.interfaces import IServiceRegistry

T = TypeVar("T")


class ServiceRegistry(IServiceRegistry):
    """Thread-safe registry binding interface types to subsystem instances."""

    def __init__(self) -> None:
        # Key: (InterfaceType, optional_name)
        self._registry: Dict[Tuple[Type[Any], Optional[str]], Any] = {}

    def register(
        self,
        interface_type: Type[T],
        instance: T,
        name: Optional[str] = None,
        allow_override: bool = False,
    ) -> None:
        """Registers a service instance under an interface type."""
        key = (interface_type, name)
        if key in self._registry and not allow_override:
            raise DuplicateServiceRegistrationError(
                f"Service for '{interface_type.__name__}' (name='{name}') already registered."
            )
        self._registry[key] = instance

    def resolve(self, interface_type: Type[T], name: Optional[str] = None) -> T:
        """Resolves registered service instance or raises ServiceNotFoundError."""
        key = (interface_type, name)
        if key not in self._registry:
            # Fallback to default name if specific name not found and name is None
            raise ServiceNotFoundError(
                f"No service registered for interface '{interface_type.__name__}' (name='{name}')."
            )
        return self._registry[key]

    def has(self, interface_type: Type[T], name: Optional[str] = None) -> bool:
        """Checks if service is registered."""
        return (interface_type, name) in self._registry

    def list_registered_services(self) -> List[str]:
        """Returns string representation of all registered services."""
        return [
            f"{itype.__name__}" + (f" ({name})" if name else "")
            for (itype, name) in self._registry.keys()
        ]

    def count(self) -> int:
        """Returns total number of registered services."""
        return len(self._registry)

    def clear(self) -> None:
        """Clears all registered services."""
        self._registry.clear()
