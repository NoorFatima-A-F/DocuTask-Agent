"""
Enterprise Module Manager.
Orchestrates module lifecycles, dependency satisfaction, and runtime execution.
"""

from typing import Any, Dict, Optional, Type
from .models import ModuleRecord, ModuleState
from .registry import ModuleRegistry
from .loader import ModuleLoader
from ..kernel.exceptions import ModuleLoadException


class ModuleManager:
    """Central manager for platform modules."""

    def __init__(self, registry: Optional[ModuleRegistry] = None):
        self.registry = registry or ModuleRegistry()
        self.loader = ModuleLoader()

    def register_module(self, module_cls: Type[Any], configuration: Optional[Dict[str, Any]] = None) -> ModuleRecord:
        """Register and validate a new module."""
        record = self.loader.create_record(module_cls, configuration=configuration)
        self.registry.register(record)
        self.registry.update_state(record.name, ModuleState.REGISTERED)
        return record

    async def initialize_module(self, name: str, context: Optional[Any] = None) -> None:
        """Initialize a registered module."""
        record = self.registry.get(name)
        if not record:
            raise ModuleLoadException(f"Module '{name}' not found")

        # Check dependencies
        for dep in record.metadata.dependencies:
            dep_rec = self.registry.get(dep)
            if not dep_rec or dep_rec.state not in (ModuleState.INITIALIZED, ModuleState.RUNNING):
                raise ModuleLoadException(f"Module '{name}' depends on '{dep}' which is not ready")

        if record.instance and hasattr(record.instance, "initialize"):
            await record.instance.initialize(context)

        self.registry.update_state(name, ModuleState.INITIALIZED)

    async def start_module(self, name: str) -> None:
        """Start an initialized module."""
        record = self.registry.get(name)
        if not record:
            raise ModuleLoadException(f"Module '{name}' not found")

        if record.instance and hasattr(record.instance, "start"):
            await record.instance.start()

        self.registry.update_state(name, ModuleState.RUNNING)

    async def stop_module(self, name: str) -> None:
        """Stop a running module."""
        record = self.registry.get(name)
        if not record:
            return

        if record.instance and hasattr(record.instance, "stop"):
            await record.instance.stop()

        self.registry.update_state(name, ModuleState.STOPPED)

    async def unload_module(self, name: str) -> None:
        """Unload and remove a module."""
        await self.stop_module(name)
        self.registry.update_state(name, ModuleState.UNLOADED)
        self.registry.unregister(name)

    async def initialize_all(self, context: Optional[Any] = None) -> None:
        """Initialize all registered modules."""
        for record in self.registry.list_modules(state=ModuleState.REGISTERED):
            await self.initialize_module(record.name, context=context)

    async def start_all(self) -> None:
        """Start all initialized modules."""
        for record in self.registry.list_modules(state=ModuleState.INITIALIZED):
            await self.start_module(record.name)

    async def stop_all(self) -> None:
        """Stop all running modules."""
        for record in self.registry.list_modules(state=ModuleState.RUNNING):
            await self.stop_module(record.name)
