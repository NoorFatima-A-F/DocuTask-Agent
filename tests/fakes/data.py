"""Shared test fixtures data: the audit's Contoso invoice as OCR text, plus helpers."""

from __future__ import annotations

import io

from PIL import Image

CONTOSO_INVOICE_TEXT = """Contoso Ltd
12 Harbour Road, Dublin, Ireland
INVOICE
Invoice No: A-7731
Invoice Date: 2026-10-14
Due Date: 2026-11-13
Bill To: Fabrikam GmbH
Description          Qty   Unit Price   Amount
Paper A4 box           2        10.00    20.00
Toner cartridge        1        15.10    15.10
Subtotal: 35.10
VAT: 7.00
Total: 42.10 EUR
"""

#: The correct extraction for CONTOSO_INVOICE_TEXT.
CONTOSO_INVOICE_JSON = {
    "invoice_number": "A-7731",
    "vendor_name": "Contoso Ltd",
    "customer_name": "Fabrikam GmbH",
    "invoice_date": "2026-10-14",
    "due_date": "2026-11-13",
    "subtotal": 35.10,
    "tax_amount": 7.00,
    "total_amount": 42.10,
    "currency": "EUR",
    "line_items": [
        {"description": "Paper A4 box", "quantity": 2, "unit_price": 10.00, "total_price": 20.00},
        {"description": "Toner cartridge", "quantity": 1, "unit_price": 15.10, "total_price": 15.10},
    ],
}

#: What the old dev-mode fallback fabricated for an invoice (see audit).
FABRICATED_FALLBACK_JSON = {
    "invoice_number": "INV-2026-001",
    "vendor_name": "John Doe",
    "customer_name": "John Doe",
    "invoice_date": "2026-08-17",
    "due_date": "2026-08-17",
    "total_amount": 1500.0,
    "currency": "Extracted currency value",
    "tax_amount": 1500.0,
    "line_items": [],
}


def png_bytes(width: int = 100, height: int = 50) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (width, height), color="white").save(buf, format="PNG")
    return buf.getvalue()
