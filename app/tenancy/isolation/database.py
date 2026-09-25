"""Tenant-Aware Database Isolation Layer (ESP-MOOS).

Enforces automatic row-level tenant filtering (Shared Database, Row-Level Isolation)
to prevent cross-tenant data leakage.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TypeVar, Generic
from app.tenancy.core.models import TenantContext
from app.tenancy.core.exceptions import CrossTenantViolationError
from app.tenancy.context.context import get_current_tenant_context

T = TypeVar("T")


class TenantScopedQuery(Generic[T]):
    """Wraps queries to automatically inject organization and workspace filters."""

    def __init__(self, items: List[T], org_id: str, workspace_id: Optional[str] = None):
        self._items = items
        self._org_id = org_id
        self._workspace_id = workspace_id

    def filter(self, **kwargs) -> List[T]:
        """Execute filtered query ensuring tenant bounds."""
        results = []
        for item in self._items:
            # Check organization boundary
            item_org = getattr(item, "organization_id", None) or (
                item.get("organization_id") if isinstance(item, dict) else None
            )
            if item_org and item_org != self._org_id:
                continue

            # Check workspace boundary if specified
            if self._workspace_id:
                item_ws = getattr(item, "workspace_id", None) or (
                    item.get("workspace_id") if isinstance(item, dict) else None
                )
                if item_ws and item_ws != self._workspace_id:
                    continue

            # Check custom filter kwargs
            match = True
            for k, v in kwargs.items():
                val = getattr(item, k, None) if not isinstance(item, dict) else item.get(k)
                if val != v:
                    match = False
                    break
            if match:
                results.append(item)
        return results

    def first(self) -> Optional[T]:
        """Get first match or None."""
        results = self.filter()
        return results[0] if results else None

    def all(self) -> List[T]:
        """Get all matching items."""
        return self.filter()


class TenantDatabaseManager:
    """Manages tenant-isolated database access and query construction."""

    def __init__(self):
        self._tables: Dict[str, List[Any]] = {}

    def insert(self, table_name: str, record: Any, context: Optional[TenantContext] = None) -> Any:
        """Insert a record with mandatory tenant ownership stamping."""
        ctx = context or get_current_tenant_context()
        if not ctx:
            raise CrossTenantViolationError("Cannot perform database write without active TenantContext")

        # Stamp record with tenant IDs
        if isinstance(record, dict):
            record["organization_id"] = ctx.organization_id
            record["workspace_id"] = ctx.workspace_id
        else:
            if hasattr(record, "organization_id"):
                setattr(record, "organization_id", ctx.organization_id)
            if hasattr(record, "workspace_id"):
                setattr(record, "workspace_id", ctx.workspace_id)

        if table_name not in self._tables:
            self._tables[table_name] = []
        self._tables[table_name].append(record)
        return record

    def query(
        self,
        table_name: str,
        context: Optional[TenantContext] = None,
        enforce_workspace: bool = False,
    ) -> TenantScopedQuery:
        """Construct a tenant-scoped query for a table."""
        ctx = context or get_current_tenant_context()
        if not ctx:
            raise CrossTenantViolationError("Cannot query database without active TenantContext")

        items = self._tables.get(table_name, [])
        ws_id = ctx.workspace_id if enforce_workspace else None
        return TenantScopedQuery(items, org_id=ctx.organization_id, workspace_id=ws_id)

    def verify_isolation(self, target_record: Any, context: Optional[TenantContext] = None) -> bool:
        """Verify that record belongs strictly to the active tenant."""
        ctx = context or get_current_tenant_context()
        if not ctx:
            return False

        org_id = getattr(target_record, "organization_id", None) or (
            target_record.get("organization_id") if isinstance(target_record, dict) else None
        )
        if org_id != ctx.organization_id:
            raise CrossTenantViolationError(
                f"Unauthorized access: record belongs to organization '{org_id}', but caller is '{ctx.organization_id}'"
            )
        return True
