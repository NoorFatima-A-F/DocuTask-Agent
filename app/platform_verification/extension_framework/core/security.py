"""
Plugin Security & Permission Enforcement Engine.
Restricts access to models, datasets, network, and storage per plugin permissions.
"""
from typing import List, Tuple
from app.platform_verification.extension_framework.domain.models import (
    PluginPermission, PluginSecurityContext, PluginMetadata
)


class PluginSecurityManager:
    @staticmethod
    def validate_permissions(
        required_permission: PluginPermission,
        context: PluginSecurityContext
    ) -> Tuple[bool, str]:
        if required_permission not in context.permissions:
            return False, f"Permission denied: Missing required permission '{required_permission.value}'."
        return True, "Authorized"

    @staticmethod
    def create_security_context(
        metadata: PluginMetadata,
        caller_identity: str = "EnterpriseVerificationRunner",
        is_sandboxed: bool = True
    ) -> PluginSecurityContext:
        return PluginSecurityContext(
            caller_identity=caller_identity,
            permissions=metadata.granted_permissions,
            is_sandboxed=is_sandboxed,
            max_memory_mb=1024,
            max_execution_time_seconds=60
        )


plugin_security_manager = PluginSecurityManager()
