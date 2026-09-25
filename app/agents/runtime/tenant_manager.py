"""
Tenant Manager.
Enforces multi-tenant isolation across Memory, Workflows, Tools, Policies, and File Storage.
"""

from typing import Dict, List, Optional
from app.agents.runtime.exceptions import TenantIsolationViolationError
from app.agents.runtime.tenant import Tenant, TenantTier


class TenantManager:
    """Manages tenant enrollment, validation, and multi-tenant boundary enforcement."""

    def __init__(self) -> None:
        self._tenants: Dict[str, Tenant] = {}
        # Pre-seed default enterprise tenant
        self.register_tenant(
            Tenant(
                tenant_id="default",
                name="Default Enterprise Tenant",
                tier=TenantTier.ENTERPRISE,
            )
        )

    def register_tenant(self, tenant: Tenant) -> None:
        """Enrolls a tenant into the runtime."""
        self._tenants[tenant.tenant_id] = tenant

    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        """Retrieves tenant record."""
        return self._tenants.get(tenant_id)

    def validate_tenant_access(self, tenant_id: str) -> Tenant:
        """Validates that a tenant exists and is active; raises TenantIsolationViolationError otherwise."""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            raise TenantIsolationViolationError(f"Tenant '{tenant_id}' is not enrolled in runtime platform.")
        if not tenant.is_active:
            raise TenantIsolationViolationError(f"Tenant '{tenant_id}' is currently suspended or inactive.")
        return tenant

    def is_tool_allowed(self, tenant_id: str, tool_name: str) -> bool:
        """Checks if a tool is permitted under the tenant's policy."""
        tenant = self.validate_tenant_access(tenant_id)
        if not tenant.allowed_tools:
            return True  # Empty means all permitted by default for enterprise
        return tool_name in tenant.allowed_tools

    def list_tenants(self) -> List[Tenant]:
        """Returns all enrolled tenants."""
        return list(self._tenants.values())
