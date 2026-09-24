"""
Platform Resource Manager.
Enforces multi-tenant limits, quotas, token budgets, and capacity reservations.
"""

from typing import Dict, Optional
from .models import ResourceQuota, ResourceType, ResourceUsage
from ...core.errors.exceptions import PlatformException
from ...core.errors.error_codes import ErrorCategory


class QuotaExceededException(PlatformException):
    """Raised when tenant exceeds resource quota."""
    def __init__(self, tenant_id: str, resource_type: ResourceType, limit: float, requested: float):
        super().__init__(
            f"Quota exceeded for tenant '{tenant_id}' on resource '{resource_type.value}': limit={limit}, requested={requested}",
            category=ErrorCategory.PLATFORM,
            error_code="QUOTA_EXCEEDED",
            http_status=429,
        )


class ResourceManager:
    """Central Resource Management and Quota Enforcement Engine."""

    def __init__(self):
        self._quotas: Dict[str, Dict[ResourceType, ResourceQuota]] = {}
        self._usage: Dict[str, Dict[ResourceType, ResourceUsage]] = {}

    def set_quota(self, quota: ResourceQuota) -> None:
        """Set or update a tenant resource quota."""
        if quota.tenant_id not in self._quotas:
            self._quotas[quota.tenant_id] = {}
        self._quotas[quota.tenant_id][quota.resource_type] = quota

    def get_quota(self, tenant_id: str, resource_type: ResourceType) -> Optional[ResourceQuota]:
        """Get quota for a tenant resource."""
        return self._quotas.get(tenant_id, {}).get(resource_type)

    def allocate(self, tenant_id: str, resource_type: ResourceType, amount: float) -> bool:
        """Attempt to allocate resource units for a tenant."""
        quota = self.get_quota(tenant_id, resource_type)

        if tenant_id not in self._usage:
            self._usage[tenant_id] = {}
        if resource_type not in self._usage[tenant_id]:
            self._usage[tenant_id][resource_type] = ResourceUsage(tenant_id=tenant_id, resource_type=resource_type)

        current = self._usage[tenant_id][resource_type].current_usage

        if quota:
            max_allowed = quota.burst_limit if (quota.burst_allowed and quota.burst_limit > 0) else quota.limit
            if current + amount > max_allowed:
                raise QuotaExceededException(tenant_id, resource_type, max_allowed, current + amount)

        self._usage[tenant_id][resource_type].current_usage += amount
        self._usage[tenant_id][resource_type].peak_usage = max(
            self._usage[tenant_id][resource_type].peak_usage,
            self._usage[tenant_id][resource_type].current_usage,
        )
        return True

    def release(self, tenant_id: str, resource_type: ResourceType, amount: float) -> None:
        """Release allocated resource units."""
        if tenant_id in self._usage and resource_type in self._usage[tenant_id]:
            self._usage[tenant_id][resource_type].current_usage = max(
                0.0,
                self._usage[tenant_id][resource_type].current_usage - amount,
            )

    def get_usage(self, tenant_id: str, resource_type: ResourceType) -> float:
        """Get current usage."""
        if tenant_id in self._usage and resource_type in self._usage[tenant_id]:
            return self._usage[tenant_id][resource_type].current_usage
        return 0.0
