"""
Phase 13.19: Multi-Tenant Subscription & Plan Tier Management.
Provides tier upgrades, feature gates, and plan entitlements.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone, timedelta
import uuid
from app.platform_saas.models.schemas import Subscription, PlanTier


class SubscriptionService:
    TIER_PRICING = {
        PlanTier.FREE: {"monthly_usd": 0.0, "max_agents": 2, "max_tokens": 5_000_000},
        PlanTier.PRO: {"monthly_usd": 499.0, "max_agents": 10, "max_tokens": 30_000_000},
        PlanTier.BUSINESS: {"monthly_usd": 2499.0, "max_agents": 50, "max_tokens": 150_000_000},
        PlanTier.ENTERPRISE: {"monthly_usd": 7999.0, "max_agents": 200, "max_tokens": 1_000_000_000},
    }

    def __init__(self):
        self._subscriptions: Dict[str, Subscription] = {}
        self._seed_default_subscriptions()

    def _seed_default_subscriptions(self) -> None:
        now = datetime.now(timezone.utc)
        sub1 = Subscription(
            subscription_id="sub_acme_enterprise",
            tenant_id="tenant_acme_corp",
            tier=PlanTier.ENTERPRISE,
            billing_interval="ANNUAL",
            current_period_start=now.isoformat(),
            current_period_end=(now + timedelta(days=365)).isoformat(),
            status="ACTIVE",
            base_price_monthly_usd=7999.0,
            auto_renew=True,
        )
        sub2 = Subscription(
            subscription_id="sub_globex_business",
            tenant_id="tenant_globex_health",
            tier=PlanTier.BUSINESS,
            billing_interval="MONTHLY",
            current_period_start=now.isoformat(),
            current_period_end=(now + timedelta(days=30)).isoformat(),
            status="ACTIVE",
            base_price_monthly_usd=2499.0,
            auto_renew=True,
        )
        self._subscriptions[sub1.subscription_id] = sub1
        self._subscriptions[sub2.subscription_id] = sub2

    def create_subscription(
        self,
        tenant_id: str,
        tier: PlanTier = PlanTier.BUSINESS,
        billing_interval: str = "MONTHLY",
    ) -> Subscription:
        sub_id = f"sub_{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc)
        days = 365 if billing_interval == "ANNUAL" else 30
        sub = Subscription(
            subscription_id=sub_id,
            tenant_id=tenant_id,
            tier=tier,
            billing_interval=billing_interval,
            current_period_start=now.isoformat(),
            current_period_end=(now + timedelta(days=days)).isoformat(),
            status="ACTIVE",
            base_price_monthly_usd=self.TIER_PRICING[tier]["monthly_usd"],
            auto_renew=True,
        )
        self._subscriptions[sub_id] = sub
        return sub

    def get_subscription_by_tenant(self, tenant_id: str) -> Optional[Subscription]:
        for sub in self._subscriptions.values():
            if sub.tenant_id == tenant_id and sub.status == "ACTIVE":
                return sub
        return None

    def upgrade_tier(self, tenant_id: str, new_tier: PlanTier) -> Subscription:
        sub = self.get_subscription_by_tenant(tenant_id)
        if not sub:
            sub = self.create_subscription(tenant_id, tier=new_tier)
            return sub
        sub.tier = new_tier
        sub.base_price_monthly_usd = self.TIER_PRICING[new_tier]["monthly_usd"]
        return sub

    def list_subscriptions(self) -> List[Subscription]:
        return list(self._subscriptions.values())
