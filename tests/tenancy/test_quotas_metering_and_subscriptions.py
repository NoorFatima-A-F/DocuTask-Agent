"""Test Quotas, Metering, Subscriptions & Feature Entitlements."""

import pytest
from app.tenancy.core.models import QuotaState, SubscriptionTier
from app.tenancy.core.exceptions import QuotaExceededError, FeatureNotEntitledError
from app.tenancy.quotas.manager import QuotaManager
from app.tenancy.metering.engine import UsageMeteringPlatform
from app.tenancy.subscriptions.engine import SubscriptionEngine
from app.tenancy.entitlements.service import FeatureEntitlementService
from app.tenancy.billing.foundation import BillingFoundation, InvoiceItem


def test_quota_management_and_threshold_states():
    """Verify quota tracking through NORMAL -> WARNING -> EXCEEDED states."""
    qm = QuotaManager()
    org_id = "org_quota_test"

    qm.set_quota(org_id, "monthly_workflows", limit_value=10, warning_threshold=0.8)

    # 5 runs -> NORMAL
    q = qm.record_usage(org_id, "monthly_workflows", 5)
    assert q.quota_state == QuotaState.NORMAL

    # +3 runs (total 8) -> WARNING (80%)
    q = qm.record_usage(org_id, "monthly_workflows", 3)
    assert q.quota_state == QuotaState.WARNING

    # +3 runs (total 11) -> Exceeded hard limit -> Raises QuotaExceededError
    with pytest.raises(QuotaExceededError):
        qm.record_usage(org_id, "monthly_workflows", 3)


def test_usage_metering_and_cost_aggregation():
    """Verify granular metering and USD cost computation."""
    metering = UsageMeteringPlatform()
    org_id = "org_meter_test"

    metering.record_usage(org_id, "ws_1", "ai.tokens.prompt_1k", quantity=1000, unit="tokens_1k")
    metering.record_usage(org_id, "ws_1", "workflow.execution", quantity=50, unit="executions")

    spend = metering.get_total_spend(org_id)
    assert spend > 0.0
    summary = metering.get_usage_summary(org_id)
    assert "ai.tokens.prompt_1k" in summary
    assert "workflow.execution" in summary


def test_subscription_and_feature_entitlements():
    """Verify subscription tier upgrade and decoupled feature entitlements."""
    sub_engine = SubscriptionEngine()
    entitlement_service = FeatureEntitlementService(sub_engine)
    org_id = "org_entitlement_test"

    # Start on Free Tier
    sub_engine.create_subscription("sub_1", org_id, SubscriptionTier.FREE)
    assert entitlement_service.is_entitled(org_id, "white_label") is False

    with pytest.raises(FeatureNotEntitledError):
        entitlement_service.require_entitlement(org_id, "white_label")

    # Upgrade to Professional Tier
    sub_engine.upgrade_tier(org_id, SubscriptionTier.PROFESSIONAL)
    assert entitlement_service.is_entitled(org_id, "white_label") is True


def test_billing_foundation_invoice_and_credits():
    """Verify credit balance top-ups and invoice settlement."""
    billing = BillingFoundation()
    org_id = "org_billing_test"

    billing.add_credits(org_id, 250.0)
    assert billing.get_credit_balance(org_id) == 250.0

    items = [
        InvoiceItem(description="Monthly Professional Subscription", quantity=1, unit_price_usd=199.0, total_usd=199.0),
        InvoiceItem(description="Excess AI Tokens Metering", quantity=1, unit_price_usd=25.0, total_usd=25.0),
    ]

    invoice = billing.generate_invoice(org_id, "sub_1", items, discount_usd=24.0)
    assert invoice.total_usd == 200.0

    paid_invoice = billing.pay_invoice_with_credits(invoice.invoice_id)
    assert paid_invoice.status == "PAID"
    assert billing.get_credit_balance(org_id) == 50.0
