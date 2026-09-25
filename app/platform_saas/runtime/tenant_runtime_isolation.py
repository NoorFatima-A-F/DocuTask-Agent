"""
Phase 13.19: Tenant Runtime Isolation & Multi-Tenant Scoping Engine.
Ensures zero cross-tenant memory, vector, file, or compute leakage.
"""

from typing import Optional
from contextvars import ContextVar
import dataclasses


@dataclasses.dataclass
class TenantSecurityContext:
    tenant_id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    project_id: Optional[str] = None
    actor_id: Optional[str] = None
    role: str = "AGENT_OPERATOR"


_tenant_context_var: ContextVar[Optional[TenantSecurityContext]] = ContextVar("tenant_context", default=None)


class TenantRuntimeIsolation:
    @staticmethod
    def set_current_context(
        tenant_id: str,
        organization_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
        project_id: Optional[str] = None,
        actor_id: Optional[str] = None,
        role: str = "AGENT_OPERATOR",
    ) -> TenantSecurityContext:
        ctx = TenantSecurityContext(
            tenant_id=tenant_id,
            organization_id=organization_id,
            workspace_id=workspace_id,
            project_id=project_id,
            actor_id=actor_id,
            role=role,
        )
        _tenant_context_var.set(ctx)
        return ctx

    @staticmethod
    def get_current_context() -> Optional[TenantSecurityContext]:
        return _tenant_context_var.get()

    @staticmethod
    def assert_tenant_access(target_tenant_id: str) -> None:
        ctx = _tenant_context_var.get()
        if ctx is None:
            return  # System context bypass
        if ctx.role == "SUPER_ADMIN":
            return  # Platform Super Admin bypass
        if ctx.tenant_id != target_tenant_id:
            raise PermissionError(
                f"Cross-tenant violation: Context tenant {ctx.tenant_id} cannot access resource belonging to {target_tenant_id}"
            )
