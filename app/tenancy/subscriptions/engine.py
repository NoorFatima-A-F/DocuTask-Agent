"""Subscription Lifecycle & Tier Management Engine (ESP-MOOS).

Governs plans:
FREE -> DEVELOPER -> PROFESSIONAL -> BUSINESS -> ENTERPRISE -> CUSTOM
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict
from app.tenancy.core.models import Subscription, SubscriptionTier
from app.tenancy.core.exceptions import SubscriptionExpiredError


class SubscriptionEngine:
    """Manages SaaS commercial subscriptions and tier entitlements."""

    TIER_DEFAULTS: Dict[SubscriptionTier, Dict[str, any]] = {
        SubscriptionTier.FREE: {
            "amount_usd": 0.0,
            "quotas": {"users": 2, "workspaces": 1, "workflows": 5, "agents": 2, "tokens_monthly": 100_000},
            "features": {"custom_domains": False, "white_label": False, "sso": False, "audit_export": False},
        },
        SubscriptionTier.DEVELOPER: {
            "amount_usd": 49.0,
            "quotas": {"users": 5, "workspaces": 3, "workflows": 25, "agents": 10, "tokens_monthly": 1_000_000},
            "features": {"custom_domains": True, "white_label": False, "sso": False, "audit_export": False},
        },
        SubscriptionTier.PROFESSIONAL: {
            "amount_usd": 199.0,
            "quotas": {"users": 20, "workspaces": 10, "workflows": 100, "agents": 50, "tokens_monthly": 10_000_000},
            "features": {"custom_domains": True, "white_label": True, "sso": False, "audit_export": True},
        },
        SubscriptionTier.ENTERPRISE: {
            "amount_usd": 999.0,
            "quotas": {"users": 1000, "workspaces": 100, "workflows": 5000, "agents": 1000, "tokens_monthly": 100_000_000},
            "features": {"custom_domains": True, "white_label": True, "sso": True, "audit_export": True},
        },
    }

    def __init__(self):
        self._subscriptions: Dict[str, Subscription] = {}

    def create_subscription(
        self,
        subscription_id: str,
        organization_id: str,
        tier: SubscriptionTier = SubscriptionTier.FREE,
        billing_interval: str = "MONTHLY",
    ) -> Subscription:
        """Create and activate a subscription for an organization."""
        defaults = self.TIER_DEFAULTS.get(tier, self.TIER_DEFAULTS[SubscriptionTier.FREE])

        sub = Subscription(
            subscription_id=subscription_id,
            organization_id=organization_id,
            tier=tier,
            start_date=datetime.now(timezone.utc),
            is_active=True,
            features=dict(defaults["features"]),
            quotas=dict(defaults["quotas"]),
            billing_interval=billing_interval,
            amount_usd=defaults["amount_usd"],
        )
        self._subscriptions[organization_id] = sub
        return sub

    def get_subscription(self, organization_id: str) -> Subscription:
        """Retrieve active subscription for an organization."""
        sub = self._subscriptions.get(organization_id)
        if not sub:
            # Create default free tier
            return self.create_subscription(f"sub_{organization_id[:8]}", organization_id, SubscriptionTier.FREE)
        if not sub.is_active:
            raise SubscriptionExpiredError(f"Subscription for organization '{organization_id}' is inactive or expired")
        return sub

    def upgrade_tier(self, organization_id: str, new_tier: SubscriptionTier) -> Subscription:
        """Upgrade or downgrade tenant subscription tier."""
        sub = self.get_subscription(organization_id)
        defaults = self.TIER_DEFAULTS.get(new_tier, self.TIER_DEFAULTS[SubscriptionTier.FREE])

        sub.tier = new_tier
        sub.amount_usd = defaults["amount_usd"]
        sub.features.update(defaults["features"])
        sub.quotas.update(defaults["quotas"])
        return sub
