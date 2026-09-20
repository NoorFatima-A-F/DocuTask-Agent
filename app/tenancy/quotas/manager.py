"""Resource Quota Management Platform (ESP-MOOS).

Tracks and enforces tenant resource limits across 5 operational states:
NORMAL (0-79%) -> WARNING (80-99%) -> LIMITED (100%) -> EXCEEDED (>100%) -> SUSPENDED.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from app.tenancy.core.models import QuotaLimit, QuotaState
from app.tenancy.core.exceptions import QuotaExceededError


class QuotaManager:
    """Manages multi-resource quota tracking and enforcement."""

    def __init__(self):
        # org_id -> (resource_name -> QuotaLimit)
        self._quotas: Dict[str, Dict[str, QuotaLimit]] = {}

    def set_quota(
        self,
        organization_id: str,
        resource_name: str,
        limit_value: int,
        warning_threshold: float = 0.8,
        hard_limit: bool = True,
    ) -> QuotaLimit:
        """Set or update quota for an organization."""
        if organization_id not in self._quotas:
            self._quotas[organization_id] = {}

        quota = QuotaLimit(
            resource_name=resource_name,
            limit_value=limit_value,
            warning_threshold=warning_threshold,
            hard_limit=hard_limit,
        )
        self._quotas[organization_id][resource_name] = quota
        return quota

    def record_usage(
        self,
        organization_id: str,
        resource_name: str,
        amount: int = 1,
    ) -> QuotaLimit:
        """Increment usage and update state machine."""
        org_quotas = self._quotas.get(organization_id, {})
        quota = org_quotas.get(resource_name)
        if not quota:
            # Default unconstrained quota
            quota = QuotaLimit(resource_name=resource_name, limit_value=1_000_000, current_usage=0)
            if organization_id not in self._quotas:
                self._quotas[organization_id] = {}
            self._quotas[organization_id][resource_name] = quota

        new_usage = quota.current_usage + amount
        ratio = new_usage / quota.limit_value if quota.limit_value > 0 else 0.0

        if ratio >= 1.0 and quota.hard_limit:
            quota.quota_state = QuotaState.EXCEEDED
            raise QuotaExceededError(
                f"Resource quota for '{resource_name}' exceeded: {new_usage}/{quota.limit_value}"
            )
        elif ratio >= 1.0:
            quota.quota_state = QuotaState.LIMITED
        elif ratio >= quota.warning_threshold:
            quota.quota_state = QuotaState.WARNING
        else:
            quota.quota_state = QuotaState.NORMAL

        quota.current_usage = new_usage
        return quota

    def get_quota(self, organization_id: str, resource_name: str) -> Optional[QuotaLimit]:
        """Get quota status for a specific resource."""
        return self._quotas.get(organization_id, {}).get(resource_name)

    def list_quotas(self, organization_id: str) -> List[QuotaLimit]:
        """List all resource quotas for an organization."""
        return list(self._quotas.get(organization_id, {}).values())
