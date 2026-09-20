"""
Enterprise Quota Manager.
Tracks and limits token consumption, active workflows, and agent concurrency per tenant.
"""

from typing import Dict
from pydantic import BaseModel, Field
from app.agents.runtime.exceptions import TenantIsolationViolationError


class TenantQuota(BaseModel):
    """Resource quotas allocated to an enterprise tenant."""
    max_tokens_per_minute: int = 100_000
    max_active_workflows: int = 50
    max_active_agents: int = 20
    tokens_consumed: int = 0
    active_workflows: int = 0
    active_agents: int = 0


class QuotaManager:
    """Manages dynamic quota consumption and rate checking."""

    def __init__(self) -> None:
        self._quotas: Dict[str, TenantQuota] = {}

    def set_quota(self, tenant_id: str, quota: TenantQuota) -> None:
        """Sets or updates quota for a tenant."""
        self._quotas[tenant_id] = quota

    def get_quota(self, tenant_id: str) -> TenantQuota:
        """Retrieves or creates default quota for tenant."""
        if tenant_id not in self._quotas:
            self._quotas[tenant_id] = TenantQuota()
        return self._quotas[tenant_id]

    def consume_tokens(self, tenant_id: str, tokens: int) -> bool:
        """Consumes tokens or raises quota exceeded error."""
        quota = self.get_quota(tenant_id)
        if quota.tokens_consumed + tokens > quota.max_tokens_per_minute:
            raise TenantIsolationViolationError(
                f"Tenant '{tenant_id}' exceeded token quota: {quota.tokens_consumed + tokens} > {quota.max_tokens_per_minute}"
            )
        quota.tokens_consumed += tokens
        return True

    def reset_usage(self, tenant_id: str) -> None:
        """Resets token consumption counter."""
        quota = self.get_quota(tenant_id)
        quota.tokens_consumed = 0
