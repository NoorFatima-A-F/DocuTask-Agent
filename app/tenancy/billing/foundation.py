"""Billing Foundation & Financial Abstraction (ESP-MOOS).

Manages invoices, credits, discounts, usage charges, and payment status without coupling
core runtime execution to billing gateways.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class InvoiceItem(BaseModel):
    """Line item in a tenant billing invoice."""
    description: str
    quantity: float
    unit_price_usd: float
    total_usd: float


class Invoice(BaseModel):
    """Billing invoice entity."""
    invoice_id: str
    organization_id: str
    subscription_id: str
    items: List[InvoiceItem] = Field(default_factory=list)
    subtotal_usd: float
    discount_usd: float = 0.0
    tax_usd: float = 0.0
    total_usd: float
    status: str = "DRAFT"  # DRAFT, ISSUED, PAID, VOID, OVERDUE
    issued_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    paid_at: Optional[datetime] = None


class BillingFoundation:
    """Manages tenant credit balances, invoice generation, and billing operations."""

    def __init__(self):
        self._invoices: Dict[str, Invoice] = {}
        self._credit_balances: Dict[str, float] = {}

    def add_credits(self, organization_id: str, amount_usd: float) -> float:
        """Add prepaid balance credits to an organization."""
        current = self._credit_balances.get(organization_id, 0.0)
        self._credit_balances[organization_id] = current + amount_usd
        return self._credit_balances[organization_id]

    def get_credit_balance(self, organization_id: str) -> float:
        """Get current credit balance."""
        return self._credit_balances.get(organization_id, 0.0)

    def generate_invoice(
        self,
        organization_id: str,
        subscription_id: str,
        items: List[InvoiceItem],
        discount_usd: float = 0.0,
        tax_rate: float = 0.0,
    ) -> Invoice:
        """Create and calculate an invoice for a billing period."""
        subtotal = sum(item.total_usd for item in items)
        tax = (subtotal - discount_usd) * tax_rate
        total = max(0.0, subtotal - discount_usd + tax)

        invoice = Invoice(
            invoice_id=f"inv_{uuid.uuid4().hex[:10]}",
            organization_id=organization_id,
            subscription_id=subscription_id,
            items=items,
            subtotal_usd=subtotal,
            discount_usd=discount_usd,
            tax_usd=tax,
            total_usd=total,
            status="ISSUED",
        )
        self._invoices[invoice.invoice_id] = invoice
        return invoice

    def pay_invoice_with_credits(self, invoice_id: str) -> Invoice:
        """Pay invoice using available prepaid credits."""
        invoice = self._invoices.get(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice '{invoice_id}' not found")

        balance = self.get_credit_balance(invoice.organization_id)
        if balance < invoice.total_usd:
            raise ValueError(f"Insufficient credit balance (${balance:.2f}) for invoice total (${invoice.total_usd:.2f})")

        self._credit_balances[invoice.organization_id] = balance - invoice.total_usd
        invoice.status = "PAID"
        invoice.paid_at = datetime.now(timezone.utc)
        return invoice

    def list_invoices(self, organization_id: str) -> List[Invoice]:
        """List all invoices for an organization."""
        return [inv for inv in self._invoices.values() if inv.organization_id == organization_id]
