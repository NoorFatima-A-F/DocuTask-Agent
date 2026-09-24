"""
Module Registry & Descriptor.
Defines ModuleDescriptor contracts and maintains the platform catalog of subsystem modules.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ModuleDescriptor(BaseModel):
    """Declarative specification of a platform subsystem module."""
    name: str
    version: str = "1.0.0"
    dependencies: List[str] = Field(default_factory=list)
    description: str = ""
    is_essential: bool = True
    is_initialized: bool = False

    model_config = {"frozen": False}


class ModuleRegistry:
    """Registry maintaining active and discovered platform subsystem modules."""

    def __init__(self) -> None:
        self._modules: Dict[str, ModuleDescriptor] = {}
        self._instances: Dict[str, Any] = {}

    def register_module(self, descriptor: ModuleDescriptor) -> None:
        """Registers a subsystem module descriptor."""
        self._modules[descriptor.name] = descriptor

    def register_instance(self, name: str, instance: Any) -> None:
        """Stores the initialized instance for a module."""
        self._instances[name] = instance
        if name in self._modules:
            self._modules[name].is_initialized = True

    def get_module(self, name: str) -> Optional[ModuleDescriptor]:
        """Retrieves module descriptor by name."""
        return self._modules.get(name)

    def get_instance(self, name: str) -> Optional[Any]:
        """Retrieves instantiated subsystem by name."""
        return self._instances.get(name)

    def list_modules(self) -> List[ModuleDescriptor]:
        """Returns all registered module descriptors."""
        return list(self._modules.values())

    def is_registered(self, name: str) -> bool:
        """Checks if module is registered."""
        return name in self._modules

    def count(self) -> int:
        """Returns number of registered modules."""
        return len(self._modules)
