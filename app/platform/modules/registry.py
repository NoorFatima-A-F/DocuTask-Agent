"""
Platform Module Registry.
"""

from typing import Dict, List, Optional
from .models import ModuleRecord, ModuleState
from ..kernel.exceptions import ModuleLoadException


class ModuleRegistry:
    """Registry maintaining active module records and status."""

    def __init__(self):
        self._modules: Dict[str, ModuleRecord] = {}

    def register(self, record: ModuleRecord) -> None:
        """Register a module record."""
        self._modules[record.name] = record

    def get(self, name: str) -> Optional[ModuleRecord]:
        """Get module record by name."""
        return self._modules.get(name)

    def list_modules(self, state: Optional[ModuleState] = None) -> List[ModuleRecord]:
        """List modules, optionally filtered by state."""
        if state is None:
            return list(self._modules.values())
        return [m for m in self._modules.values() if m.state == state]

    def update_state(self, name: str, new_state: ModuleState, error_message: Optional[str] = None) -> None:
        """Transition module state."""
        record = self._modules.get(name)
        if not record:
            raise ModuleLoadException(f"Module '{name}' not found in registry")
        record.state = new_state
        if error_message:
            record.error_message = error_message

    def unregister(self, name: str) -> None:
        """Remove module from registry."""
        self._modules.pop(name, None)
