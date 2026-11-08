"""Generate the synthetic evaluation dataset (deterministic; see SOURCES.md).

Each document gets a directory ``evals/dataset/<id>/`` with:

* ``document.png`` - the rendered page (what OCR sees in live mode);
* ``text.txt``     - the exact text that was rendered (clean-OCR upper bound);
* ``truth.json``   - ``{"document_type": ..., "fields": {...}}`` ground truth.

Usage::

    python evals/generate.py            # writes 36 documents (12 invoices, 12 receipts, 12 utility bills)
"""

from __future__ import annotations

import json
import random
import shutil
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent / "dataset"
SEED = 20261108
PER_TYPE = 12

# Fictional names only (not real companies or people).
VENDORS = [
    "Halvorsen Tooling",
    "Brightwater Analytics",
    "Quillfeather Print Co",
    "Orrin & Vale Logistics",
    "Mossgrove Catering",
    "Tidepool Software",
    "Kestrel Office Supply",
    "Larchmont Electrical",
]
CUSTOMERS = ["Pinecrest Dental", "Aldermoor School", "Ravensdale Cafe", "Juniper Lane Studio", "Marlow Bikes"]
STORES = ["Corner Pantry", "Fenwick Hardware", "Bluebell Bakery", "Northgate Pharmacy", "Saltmarsh Grocers"]
UTILITIES = ["Riverbend Power", "Clearwell Water Authority", "Summit Gas & Light"]
ITEMS = [
    "Consulting hours",
    "Printer toner",
    "Network cable 10m",
    "Annual license",
    "Desk lamp",
    "Training session",
    "Paper A4 box",
    "USB-C hub",
    "Coffee beans 1kg",
    "Delivery fee",
]
GROCERIES = ["Milk 1L", "Sourdough loaf", "Eggs dozen", "Apples 1kg", "Batteries AA", "Light bulb", "Tea 80ct"]
DATE_FORMATS = ["%Y-%m-%d", "%B %d, %Y", "%d/%m/%Y"]
CURRENCIES = {"USD": "$", "EUR": "EUR ", "GBP": "GBP "}


def _item(desc: str, qty: int, unit: float) -> dict[str, Any]:
    return {"description": desc, "quantity": float(qty), "unit_price": unit, "total_price": round(qty * unit, 2)}


def money(x: float) -> str:
    return f"{x:,.2f}"


def rand_date(rng: random.Random) -> date:
    return date(2026, 1, 1) + timedelta(days=rng.randrange(0, 300))


def fmt(d: date, rng: random.Random) -> str:
    return d.strftime(rng.choice(DATE_FORMATS))


def invoice(rng: random.Random, n: int) -> tuple[list[str], dict[str, Any]]:
    currency = rng.choice(list(CURRENCIES))
    sym = CURRENCIES[currency]
    issued = rand_date(rng)
    due = issued + timedelta(days=rng.choice([14, 30, 45]))
    items: list[dict[str, Any]] = []
    for desc in rng.sample(ITEMS, rng.randint(2, 4)):
        qty = rng.randint(1, 5)
        unit = round(rng.uniform(5, 400), 2)
        items.append(
            {"description": desc, "quantity": float(qty), "unit_price": unit, "total_price": round(qty * unit, 2)}
        )
    subtotal = round(sum(i["total_price"] for i in items), 2)
    tax = round(subtotal * rng.choice([0.0, 0.05, 0.08, 0.2]), 2)
    total = round(subtotal + tax, 2)
    fields: dict[str, Any] = {
        "invoice_number": f"INV-{2026}{n:04d}",
        "vendor_name": rng.choice(VENDORS),
        "customer_name": rng.choice(CUSTOMERS),
        "invoice_date": issued.isoformat(),
        "due_date": due.isoformat(),
        "subtotal": subtotal,
        "tax_amount": tax,
        "total_amount": total,
        "currency": currency,
        "line_items": items,
    }
    lines: list[str] = [
        fields["vendor_name"].upper(),
        "INVOICE",
        f"Invoice No: {fields['invoice_number']}",
        f"Date: {fmt(issued, rng)}",
        f"Due: {fmt(due, rng)}",
        f"Bill to: {fields['customer_name']}",
        "",
        "Description            Qty   Unit price   Amount",
        *[
            f"{i['description']:<22} {int(i['quantity']):>3}   "
            f"{money(i['unit_price']):>10}   {money(i['total_price']):>10}"
            for i in items
        ],
        "",
        f"Subtotal: {sym}{money(subtotal)}",
        f"Tax: {sym}{money(tax)}",
        f"Total due ({currency}): {sym}{money(total)}",
    ]
    return lines, fields


def receipt(rng: random.Random, n: int) -> tuple[list[str], dict[str, Any]]:
    when = rand_date(rng)
    items: list[dict[str, Any]] = []
    for desc in rng.sample(GROCERIES, rng.randint(2, 5)):
        qty = rng.randint(1, 3)
        unit = round(rng.uniform(0.5, 15), 2)
        items.append(
            {"description": desc, "quantity": float(qty), "unit_price": unit, "total_price": round(qty * unit, 2)}
        )
    subtotal = round(sum(i["total_price"] for i in items), 2)
    tax = round(subtotal * 0.07, 2)
    total = round(subtotal + tax, 2)
    fields: dict[str, Any] = {
        "store_name": rng.choice(STORES),
        "transaction_date": when.isoformat(),
        "subtotal": subtotal,
        "tax": tax,
        "total_amount": total,
        "payment_method": rng.choice(["Cash", "Credit", "Debit"]),
        "line_items": items,
    }
    lines: list[str] = [
        fields["store_name"],
        f"Receipt #{1000 + n}   {fmt(when, rng)}",
        "",
        *[
            f"{int(i['quantity'])} x {i['description']:<16} @ {money(i['unit_price'])}  {money(i['total_price'])}"
            for i in items
        ],
        "",
        f"Subtotal {money(subtotal)}",
        f"Sales tax 7% {money(tax)}",
        f"TOTAL {money(total)}",
        f"Paid by {fields['payment_method']}",
    ]
    return lines, fields


def utility_bill(rng: random.Random, n: int) -> tuple[list[str], dict[str, Any]]:
    billed = rand_date(rng)
    due = billed + timedelta(days=21)
    kwh = rng.randint(120, 1400)
    amount = round(kwh * rng.uniform(0.11, 0.32) + 9.5, 2)
    fields: dict[str, Any] = {
        "utility_company": rng.choice(UTILITIES),
        "account_number": f"{rng.randint(10, 99)}-{rng.randint(100000, 999999)}",
        "service_address": f"{rng.randint(1, 999)} {rng.choice(['Elm', 'Harbor', 'Mill', 'Station'])} Street",
        "bill_date": billed.isoformat(),
        "due_date": due.isoformat(),
        "amount_due": amount,
        "consumption": f"{kwh} kWh",
    }
    lines: list[str] = [
        fields["utility_company"],
        "Statement of account",
        f"Account number: {fields['account_number']}",
        f"Service address: {fields['service_address']}",
        f"Bill date: {fmt(billed, rng)}",
        f"Usage this period: {fields['consumption']}",
        "",
        f"Amount due: ${money(amount)}",
        f"Please pay by {fmt(due, rng)}",
    ]
    return lines, fields


def render(lines: list[str], path: Path) -> None:
    font = ImageFont.load_default(size=22)
    width, line_h = 1100, 34
    img = Image.new("L", (width, 80 + line_h * len(lines)), color=255)
    draw = ImageDraw.Draw(img)
    for i, line in enumerate(lines):
        draw.text((40, 40 + i * line_h), line, fill=0, font=font)
    img.save(path, optimize=True)


def main() -> None:
    rng = random.Random(SEED)  # noqa: S311 - reproducible synthetic data, not security
    if ROOT.exists():
        shutil.rmtree(ROOT)
    builders = {"invoice": invoice, "receipt": receipt, "utility_bill": utility_bill}
    for doc_type, build in builders.items():
        for n in range(1, PER_TYPE + 1):
            lines, fields = build(rng, n)
            out = ROOT / f"{doc_type}-{n:02d}"
            out.mkdir(parents=True)
            render(lines, out / "document.png")
            (out / "text.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
            (out / "truth.json").write_text(
                json.dumps({"document_type": doc_type, "fields": fields}, indent=2) + "\n", encoding="utf-8"
            )
    print(f"wrote {len(builders) * PER_TYPE} documents to {ROOT}")


if __name__ == "__main__":
    main()
