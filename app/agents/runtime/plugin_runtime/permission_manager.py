"""
Plugin Permission Manager.
Enforces fine-grained logical security permissions:
filesystem.read, filesystem.write, network.access, database.access, secret.access.
"""

from enum import Enum
from typing import Dict, List, Optional, Set
from app.agents.runtime.exceptions import PluginValidationError


class PermissionDeniedError(PluginValidationError):
    """Raised when a plugin performs an action without required security permission."""
    pass


class PluginPermission(str, Enum):
    """Standard enterprise security permissions granted to plugins."""
    FILESYSTEM_READ = "filesystem.read"
    FILESYSTEM_WRITE = "filesystem.write"
    NETWORK_ACCESS = "network.access"
    DATABASE_ACCESS = "database.access"
    SECRET_ACCESS = "secret.access"


class PluginPermissionManager:
    """Validates requested plugin permissions against allowed tenant and platform policies."""

    def __init__(self, allowed_permissions: Optional[Set[PluginPermission]] = None) -> None:
        self.allowed_permissions: Set[PluginPermission] = allowed_permissions or {
            PluginPermission.FILESYSTEM_READ,
            PluginPermission.FILESYSTEM_WRITE,
            PluginPermission.NETWORK_ACCESS,
            PluginPermission.DATABASE_ACCESS,
            PluginPermission.SECRET_ACCESS,
        }
        # plugin_id -> set of granted PluginPermission
        self._granted_permissions: Dict[str, Set[PluginPermission]] = {}

    def grant_permission(self, plugin_id: str, permission: PluginPermission) -> None:
        if plugin_id not in self._granted_permissions:
            self._granted_permissions[plugin_id] = set()
        self._granted_permissions[plugin_id].add(permission)

    def revoke_permission(self, plugin_id: str, permission: PluginPermission) -> None:
        if plugin_id in self._granted_permissions:
            self._granted_permissions[plugin_id].discard(permission)

    def has_permission(self, plugin_id: str, permission: PluginPermission) -> bool:
        return permission in self._granted_permissions.get(plugin_id, set())

    def assert_permission(self, plugin_id: str, permission: PluginPermission) -> None:
        if not self.has_permission(plugin_id, permission):
            raise PermissionDeniedError(
                f"Security violation: Plugin '{plugin_id}' lacks required permission '{permission.value}'"
            )

    def verify_permissions(self, requested_permissions: List[str]) -> None:
        """Verifies that all requested permissions are permitted."""
        unauthorized = []
        for perm_str in requested_permissions:
            try:
                perm_enum = PluginPermission(perm_str)
                if perm_enum not in self.allowed_permissions:
                    unauthorized.append(perm_str)
            except ValueError:
                unauthorized.append(perm_str)

        if unauthorized:
            raise PluginValidationError(
                f"Plugin requested unauthorized security permissions: {unauthorized}"
            )
