"""Feature Entitlement Service (ESP-MOOS).

Decoupled feature entitlement checking without hardcoding 'if enterprise:' checks in business logic.
"""

from __future__ import annotations

from typing import Dict, Optional
from app.tenancy.core.models import SubscriptionTier
from app.tenancy.core.exceptions import FeatureNotEntitledError
from app.tenancy.subscriptions.engine import SubscriptionEngine


class FeatureEntitlementService:
    """Evaluates whether a tenant is entitled to specific platform features."""

    # Default catalog of features and required minimum tier
    FEATURE_CATALOG: Dict[str, SubscriptionTier] = {
        "advanced_agents": SubscriptionTier.PROFESSIONAL,
        "private_models": SubscriptionTier.ENTERPRISE,
        "custom_domains": SubscriptionTier.DEVELOPER,
        "white_label": SubscriptionTier.PROFESSIONAL,
        "sso_saml": SubscriptionTier.ENTERPRISE,
        "audit_export": SubscriptionTier.PROFESSIONAL,
        "unlimited_storage": SubscriptionTier.ENTERPRISE,
        "priority_support": SubscriptionTier.BUSINESS,
    }

    def __init__(self, subscription_engine: SubscriptionEngine):
        self.subscription_engine = subscription_engine

    def is_entitled(self, organization_id: str, feature_name: str) -> bool:
        """Check if organization is entitled to a feature."""
        sub = self.subscription_engine.get_subscription(organization_id)
        # Check custom overrides on subscription
        if feature_name in sub.features:
            return sub.features[feature_name]

        # Check against tier catalog
        required_tier = self.FEATURE_CATALOG.get(feature_name)
        if not required_tier:
            return True  # Free/standard feature

        tier_weights = {
            SubscriptionTier.FREE: 0,
            SubscriptionTier.DEVELOPER: 1,
            SubscriptionTier.PROFESSIONAL: 2,
            SubscriptionTier.BUSINESS: 3,
            SubscriptionTier.ENTERPRISE: 4,
            SubscriptionTier.CUSTOM: 5,
        }

        current_weight = tier_weights.get(sub.tier, 0)
        required_weight = tier_weights.get(required_tier, 0)
        return current_weight >= required_weight

    def require_entitlement(self, organization_id: str, feature_name: str) -> None:
        """Assert feature entitlement or raise FeatureNotEntitledError."""
        if not self.is_entitled(organization_id, feature_name):
            raise FeatureNotEntitledError(
                f"Organization '{organization_id}' is not entitled to feature '{feature_name}'. Please upgrade your subscription plan."
            )
