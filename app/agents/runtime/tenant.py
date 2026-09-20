"""
Tenant Model.
Represents an enterprise tenant with associated resource quotas, tiers, and capability access boundaries.
"""

from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class TenantTier(str, Enum):
    """SaaS pricing and isolation tier."""
    FREE = "FREE"
    STANDARD = "STANDARD"
    ENTERPRISE = "ENTERPRISE"


class Tenant(BaseModel):
    """Enterprise tenant record governing platform resource quotas and isolation."""
    tenant_id: str
    name: str
    tier: TenantTier = TenantTier.ENTERPRISE
    max_concurrent_workflows: int = 100
    allowed_tools: List[str] = Field(default_factory=list)
    is_active: bool = True

    model_config = {"frozen": True}
