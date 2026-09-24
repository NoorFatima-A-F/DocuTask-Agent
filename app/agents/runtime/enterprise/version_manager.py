"""
Runtime Version Manager.
Enforces version negotiation, validates subsystem module versions against kernel constraints,
and rejects breaking API versions.
"""

from typing import Dict, Optional
from app.agents.runtime.enterprise.compatibility_checker import VersionCompatibilityChecker
from app.agents.runtime.exceptions import RuntimeKernelException


class IncompatibleVersionError(RuntimeKernelException):
    """Raised when a subsystem or plugin version violates runtime compatibility rules."""
    pass


class RuntimeVersionManager:
    """Manages active runtime API versions and negotiates component compatibility."""

    def __init__(self, current_runtime_version: str = "23.0.0") -> None:
        self.current_runtime_version = current_runtime_version
        self._registered_versions: Dict[str, str] = {}

    def register_component_version(self, component_name: str, version: str) -> bool:
        """Registers a component version and validates compatibility with the runtime."""
        if not VersionCompatibilityChecker.is_compatible(self.current_runtime_version, version):
            raise IncompatibleVersionError(
                f"Component '{component_name}' v{version} is incompatible with Runtime v{self.current_runtime_version}."
            )
        self._registered_versions[component_name] = version
        return True

    def get_version(self, component_name: str) -> Optional[str]:
        return self._registered_versions.get(component_name)

    def list_components(self) -> Dict[str, str]:
        return dict(self._registered_versions)
