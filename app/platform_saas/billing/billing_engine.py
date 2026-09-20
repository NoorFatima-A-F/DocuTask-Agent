"""
Phase 13.19: Multi-Tenant Billing Engine & Invoicing Gateway.
Simulates Stripe & Paddle adapters, generates itemized invoices, calculates overage charges.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone, timedelta
import uuid
from app.platform_saas.models.schemas import (
    Invoice,
    InvoiceStatus,
    BillingProvider,
)


class BillingEngine:
    def __init__(self):
        self._invoices: Dict[str, Invoice] = {}
        self._seed_default_invoices()

    def _seed_default_invoices(self) -> None:
        inv1 = Invoice(
            invoice_id="inv_acme_2026_08",
            tenant_id="tenant_acme_corp",
            subscription_id="sub_acme_enterprise",
            amount_due_usd=7999.0,
            amount_paid_usd=7999.0,
            status=InvoiceStatus.PAID,
            billing_period="2026-08",
            created_at=datetime.now(timezone.utc).isoformat(),
            due_date=(datetime.now(timezone.utc) + timedelta(days=15)).isoformat(),
        )
        inv2 = Invoice(
            invoice_id="inv_globex_2026_08",
            tenant_id="tenant_globex_health",
            subscription_id="sub_globex_business",
            amount_due_usd=2499.0,
            amount_paid_usd=2499.0,
            status=InvoiceStatus.PAID,
            billing_period="2026-08",
            created_at=datetime.now(timezone.utc).isoformat(),
            due_date=(datetime.now(timezone.utc) + timedelta(days=15)).isoformat(),
        )
        self._invoices[inv1.invoice_id] = inv1
        self._invoices[inv2.invoice_id] = inv2

    def generate_invoice(
        self,
        tenant_id: str,
        subscription_id: str,
        base_amount_usd: float,
        overage_amount_usd: float = 0.0,
        billing_period: str = "2026-09",
    ) -> Invoice:
        inv_id = f"inv_{uuid.uuid4().hex[:8]}"
        total = base_amount_usd + overage_amount_usd
        inv = Invoice(
            invoice_id=inv_id,
            tenant_id=tenant_id,
            subscription_id=subscription_id,
            amount_due_usd=total,
            amount_paid_usd=0.0,
            status=InvoiceStatus.OPEN,
            billing_period=billing_period,
            created_at=datetime.now(timezone.utc).isoformat(),
            due_date=(datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
        )
        self._invoices[inv_id] = inv
        return inv

    def mark_invoice_paid(self, invoice_id: str) -> Invoice:
        inv = self._invoices.get(invoice_id)
        if not inv:
            raise ValueError(f"Invoice {invoice_id} not found")
        inv.amount_paid_usd = inv.amount_due_usd
        inv.status = InvoiceStatus.PAID
        return inv

    def list_invoices(self, tenant_id: Optional[str] = None) -> List[Invoice]:
        if tenant_id:
            return [i for i in self._invoices.values() if i.tenant_id == tenant_id]
        return list(self._invoices.values())

    def process_webhook_event(self, provider: BillingProvider, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Simulates Stripe / Paddle webhook processing."""
        event_type = payload.get("type", "payment_intent.succeeded")
        tenant_id = payload.get("tenant_id", "tenant_acme_corp")
        return {
            "provider": provider.value,
            "event_type": event_type,
            "tenant_id": tenant_id,
            "processed": True,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
