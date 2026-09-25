"""
Resource Sharing Manager.
Enforces shared concurrency limits and token quotas across cooperating agents within a team or session.
"""

from typing import Dict
from uuid import UUID
from pydantic import BaseModel, Field


class SharedResourceQuota(BaseModel):
    """Resource quotas shared across a team."""
    max_total_concurrency: int = Field(default=8, ge=1)
    allocated_concurrency: int = Field(default=0, ge=0)
    token_budget: int = Field(default=50000, ge=0)
    consumed_tokens: int = Field(default=0, ge=0)

    def can_allocate_concurrency(self, count: int = 1) -> bool:
        return (self.allocated_concurrency + count) <= self.max_total_concurrency

    def allocate_concurrency(self, count: int = 1) -> "SharedResourceQuota":
        return self.model_copy(update={"allocated_concurrency": self.allocated_concurrency + count})

    def release_concurrency(self, count: int = 1) -> "SharedResourceQuota":
        return self.model_copy(update={"allocated_concurrency": max(0, self.allocated_concurrency - count)})

    def consume_tokens(self, tokens: int) -> "SharedResourceQuota":
        return self.model_copy(update={"consumed_tokens": self.consumed_tokens + tokens})


class ResourceSharingManager:
    """Manages team-level resource quotas."""

    def __init__(self):
        self._team_quotas: Dict[UUID, SharedResourceQuota] = {}

    def get_or_create_quota(self, team_id: UUID, max_concurrency: int = 8) -> SharedResourceQuota:
        if team_id not in self._team_quotas:
            self._team_quotas[team_id] = SharedResourceQuota(max_total_concurrency=max_concurrency)
        return self._team_quotas[team_id]

    def update_quota(self, team_id: UUID, quota: SharedResourceQuota) -> None:
        self._team_quotas[team_id] = quota
