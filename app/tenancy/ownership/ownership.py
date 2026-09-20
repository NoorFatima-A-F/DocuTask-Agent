"""Resource Ownership & Identity Framework (ESP-MOOS).

Stamps and validates ResourceIdentity across all platform assets:
Workflows, Agents, Knowledge, Connectors, Secrets, Prompts, Templates, and Executions.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from app.tenancy.core.models import ResourceIdentity, ResourceType, TenantContext
from app.tenancy.core.exceptions import CrossTenantViolationError
from app.tenancy.context.context import get_current_tenant_context


class ResourceOwnershipManager:
    """Manages resource ownership identities and cross-tenant boundaries."""

    def __init__(self):
        self._identities: Dict[str, ResourceIdentity] = {}

    def stamp_resource(
        self,
        resource_id: str,
        resource_type: ResourceType,
        context: Optional[TenantContext] = None,
        creator_id: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ) -> ResourceIdentity:
        """Create and register a ResourceIdentity from context."""
        ctx = context or get_current_tenant_context()
        if not ctx:
            raise CrossTenantViolationError("Cannot stamp resource identity without active TenantContext")

        identity = ResourceIdentity(
            resource_id=resource_id,
            resource_type=resource_type,
            organization_id=ctx.organization_id,
            workspace_id=ctx.workspace_id,
            environment_id=ctx.environment_id,
            project_id=ctx.project_id,
            owner_id=ctx.user_id,
            creator_id=creator_id or ctx.user_id,
            tags=tags or {},
        )
        self._identities[resource_id] = identity
        return identity

    def get_identity(self, resource_id: str) -> Optional[ResourceIdentity]:
        """Retrieve ResourceIdentity for a given resource."""
        return self._identities.get(resource_id)

    def verify_access(
        self,
        resource_id: str,
        context: Optional[TenantContext] = None,
        require_same_workspace: bool = False,
    ) -> bool:
        """Verify that the active tenant has permission to access the resource."""
        ctx = context or get_current_tenant_context()
        if not ctx:
            raise CrossTenantViolationError("Cannot access resource without active TenantContext")

        identity = self.get_identity(resource_id)
        if not identity:
            # Resource not registered with an identity yet; allow or block based on configuration
            return True

        # Check organization boundary
        if identity.organization_id != ctx.organization_id:
            raise CrossTenantViolationError(
                f"Cross-tenant access forbidden: resource '{resource_id}' belongs to org '{identity.organization_id}', caller is '{ctx.organization_id}'"
            )

        # Check workspace boundary if enforced
        if require_same_workspace and identity.workspace_id != ctx.workspace_id:
            raise CrossTenantViolationError(
                f"Workspace isolation violation: resource '{resource_id}' belongs to workspace '{identity.workspace_id}', caller is '{ctx.workspace_id}'"
            )

        return True

    def list_resources_by_type(
        self,
        resource_type: ResourceType,
        context: Optional[TenantContext] = None,
    ) -> List[ResourceIdentity]:
        """List all resources of a specific type owned by the current tenant."""
        ctx = context or get_current_tenant_context()
        if not ctx:
            return []

        return [
            ident for ident in self._identities.values()
            if ident.resource_type == resource_type and ident.organization_id == ctx.organization_id
        ]
