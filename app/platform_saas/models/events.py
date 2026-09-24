"""
Phase 13.19: Domain Events for SaaS Platform.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class SaaSPlatformEvent(BaseModel):
    event_id: str
    tenant_id: str
    event_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TenantProvisionedEvent(SaaSPlatformEvent):
    event_type: str = "TENANT_PROVISIONED"


class SubscriptionUpdatedEvent(SaaSPlatformEvent):
    event_type: str = "SUBSCRIPTION_UPDATED"
    tier: str = "ENTERPRISE"


class UsageLimitReachedEvent(SaaSPlatformEvent):
    event_type: str = "USAGE_LIMIT_REACHED"
    metric: str = ""


class PolicyViolationDetectedEvent(SaaSPlatformEvent):
    event_type: str = "POLICY_VIOLATION_DETECTED"
    reason: str = ""


class MarketplaceAssetPublishedEvent(SaaSPlatformEvent):
    event_type: str = "MARKETPLACE_ASSET_PUBLISHED"
    asset_id: str = ""
