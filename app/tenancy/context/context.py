"""Tenant Context Management with Async ContextVars (ESP-MOOS)."""

from __future__ import annotations

import contextvars
from typing import Optional
from app.tenancy.core.models import TenantContext

# Global thread/async-safe context variable
_CURRENT_TENANT_CONTEXT: contextvars.ContextVar[Optional[TenantContext]] = contextvars.ContextVar(
    "current_tenant_context", default=None
)


def get_current_tenant_context() -> Optional[TenantContext]:
    """Retrieve the active tenant context for the current execution thread/task."""
    return _CURRENT_TENANT_CONTEXT.get()


def set_current_tenant_context(context: Optional[TenantContext]) -> contextvars.Token:
    """Set the active tenant context for the current execution thread/task."""
    return _CURRENT_TENANT_CONTEXT.set(context)


def reset_tenant_context(token: contextvars.Token) -> None:
    """Reset the tenant context using the token from `set_current_tenant_context`."""
    _CURRENT_TENANT_CONTEXT.reset(token)


class TenantContextScope:
    """Context manager for setting a scoped tenant context."""

    def __init__(self, context: TenantContext):
        self.context = context
        self._token: Optional[contextvars.Token] = None

    def __enter__(self) -> TenantContext:
        self._token = set_current_tenant_context(self.context)
        return self.context

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._token is not None:
            reset_tenant_context(self._token)
