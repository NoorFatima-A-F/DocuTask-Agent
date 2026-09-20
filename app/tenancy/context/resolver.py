"""Tenant Context Resolver (ESP-MOOS).

Extracts and resolves TenantContext from HTTP request headers, JWT claims,
custom host domains, or background asynchronous task metadata.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Optional
from app.tenancy.core.models import (
    TenantContext,
    Region,
    ComplianceProfileType,
    SubscriptionTier,
)
from app.tenancy.core.exceptions import TenantNotFoundError


class TenantContextResolver:
    """Resolves TenantContext across HTTP and background execution boundaries."""

    def __init__(self, org_registry: Optional[Any] = None):
        self._org_registry = org_registry

    def resolve_from_headers(
        self,
        headers: Dict[str, str],
        user_id: Optional[str] = None,
        jwt_claims: Optional[Dict[str, Any]] = None,
    ) -> TenantContext:
        """Resolve TenantContext from HTTP request headers and JWT claims."""
        org_id = (
            headers.get("X-Organization-Id")
            or headers.get("x-organization-id")
            or (jwt_claims.get("org_id") if jwt_claims else None)
            or (jwt_claims.get("organization_id") if jwt_claims else None)
        )
        if not org_id:
            raise TenantNotFoundError("Missing organization identifier in request context")

        workspace_id = (
            headers.get("X-Workspace-Id")
            or headers.get("x-workspace-id")
            or (jwt_claims.get("workspace_id") if jwt_claims else None)
            or "default_workspace"
        )
        environment_id = (
            headers.get("X-Environment-Id")
            or headers.get("x-environment-id")
            or "production"
        )
        project_id = (
            headers.get("X-Project-Id")
            or headers.get("x-project-id")
            or "default_project"
        )
        resolved_user_id = (
            user_id
            or headers.get("X-User-Id")
            or headers.get("x-user-id")
            or (jwt_claims.get("sub") if jwt_claims else None)
            or "anonymous_user"
        )
        request_id = (
            headers.get("X-Request-Id")
            or headers.get("x-request-id")
            or str(uuid.uuid4())
        )
        trace_id = (
            headers.get("X-Trace-Id")
            or headers.get("x-trace-id")
            or str(uuid.uuid4())
        )

        permissions = set()
        role_ids = []
        if jwt_claims:
            role_ids = jwt_claims.get("roles", [])
            permissions = set(jwt_claims.get("permissions", []))

        return TenantContext(
            organization_id=org_id,
            workspace_id=workspace_id,
            environment_id=environment_id,
            project_id=project_id,
            user_id=resolved_user_id,
            role_ids=role_ids,
            permissions=permissions,
            request_id=request_id,
            trace_id=trace_id,
        )

    def resolve_from_task_metadata(self, metadata: Dict[str, Any]) -> TenantContext:
        """Resolve TenantContext passed to background workers, workflows, and agents."""
        org_id = metadata.get("organization_id") or metadata.get("tenant_context_id")
        if not org_id:
            raise TenantNotFoundError("Worker task metadata missing organization identifier")

        return TenantContext(
            organization_id=org_id,
            workspace_id=metadata.get("workspace_id", "default_workspace"),
            environment_id=metadata.get("environment_id", "default"),
            project_id=metadata.get("project_id", "default"),
            user_id=metadata.get("user_id", "system_worker"),
            role_ids=metadata.get("role_ids", []),
            permissions=set(metadata.get("permissions", [])),
            region=Region(metadata.get("region", Region.US_EAST.value)),
            compliance_profile=ComplianceProfileType(
                metadata.get("compliance_profile", ComplianceProfileType.STANDARD.value)
            ),
            subscription_plan=SubscriptionTier(
                metadata.get("subscription_plan", SubscriptionTier.FREE.value)
            ),
            feature_flags=metadata.get("feature_flags", {}),
            request_id=metadata.get("request_id"),
            trace_id=metadata.get("trace_id"),
            metadata=metadata.get("metadata", {}),
        )
