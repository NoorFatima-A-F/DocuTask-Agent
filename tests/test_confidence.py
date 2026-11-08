"""Evidence-based confidence: grounding, completeness, consistency, routing."""

from __future__ import annotations

import copy
from typing import Any

import pytest

from app.ai.confidence import (
    REQUIRED_FIELDS,
    assess,
    dates_in,
    ground_value,
    normalise_text,
    parse_number,
    routing_status,
)
from app.ai.prompt_builder import PromptBuilder
from app.ai.validator import AIValidator
from app.core.errors.extraction import ExtractionStatus
from tests.fakes.data import CONTOSO_INVOICE_JSON, CONTOSO_INVOICE_TEXT, FABRICATED_FALLBACK_JSON

THRESHOLD = 0.85


def run(data: dict, text: str = CONTOSO_INVOICE_TEXT, ocr: float | None = 0.92, doc_type: str = "invoice"):
    validated = AIValidator.validate(data, doc_type)
    report = assess(doc_type, validated, text, ocr, THRESHOLD)
    return report, routing_status(report, THRESHOLD)


@pytest.mark.parametrize(
    ("token", "value"),
    [("1.234,56", 1234.56), ("1,234.56", 1234.56), ("1 234,56", 1234.56), ("42.10", 42.10), ("12,34", 12.34)],
)
def test_locale_number_parsing(token: str, value: float) -> None:
    assert parse_number(token) == pytest.approx(value)


def test_dates_found_in_text_are_iso_comparable() -> None:
    assert {d.isoformat() for d in dates_in("Issued 14 Oct 2026, due 2026-11-13")} >= {"2026-10-14", "2026-11-13"}


def test_string_grounding_is_case_and_punctuation_insensitive() -> None:
    text = "CONTOSO, LTD.\nInvoice"
    assert ground_value("vendor_name", "Contoso Ltd", text, normalise_text(text)) is True
    assert ground_value("vendor_name", "Northwind Traders", text, normalise_text(text)) is False
    assert ground_value("vendor_name", None, text, normalise_text(text)) is None


def test_grounded_correct_invoice_completes() -> None:
    report, status = run(CONTOSO_INVOICE_JSON)
    assert status == ExtractionStatus.COMPLETED
    assert report.score >= THRESHOLD
    assert not report.required_missing and not report.required_ungrounded
    assert {c.name for c in report.checks} >= {"subtotal_plus_tax_equals_total", "line_items_sum_equals_subtotal"}
    assert all(c.passed for c in report.checks)


def test_hallucinated_vendor_routes_to_review() -> None:
    data = {**CONTOSO_INVOICE_JSON, "vendor_name": "Northwind Traders"}
    report, status = run(data)
    assert status == ExtractionStatus.NEEDS_REVIEW
    assert report.fields["vendor_name"].grounded is False
    assert "vendor_name" in report.required_ungrounded
    assert report.score < THRESHOLD


def test_inconsistent_totals_route_to_review_with_named_check() -> None:
    # 99.99 appears in the text so the total is grounded; only the arithmetic is wrong.
    text = CONTOSO_INVOICE_TEXT + "\nRef 99.99\n"
    data = {**CONTOSO_INVOICE_JSON, "total_amount": 99.99}
    report, status = run(data, text=text)
    assert status == ExtractionStatus.NEEDS_REVIEW
    assert "subtotal_plus_tax_equals_total" in report.to_dict()["failed_checks"]
    assert report.score < THRESHOLD


def test_line_item_arithmetic_checked() -> None:
    data: dict[str, Any] = copy.deepcopy(CONTOSO_INVOICE_JSON)
    data["line_items"][0]["quantity"] = 3
    report, status = run(data, text=CONTOSO_INVOICE_TEXT + " 3")
    assert status == ExtractionStatus.NEEDS_REVIEW
    assert "line_items[0].quantity_x_unit_price" in report.to_dict()["failed_checks"]


def test_due_date_before_invoice_date_fails() -> None:
    data = {**CONTOSO_INVOICE_JSON, "due_date": "2026-10-01"}
    report, _ = run(data, text=CONTOSO_INVOICE_TEXT + " 2026-10-01")
    assert "due_date_after_invoice_date" in report.to_dict()["failed_checks"]


def test_empty_result_is_never_completed() -> None:
    report, status = run({})
    assert status == ExtractionStatus.NEEDS_REVIEW
    assert report.score == 0.0
    assert set(report.required_missing) == {"invoice_number", "vendor_name", "invoice_date", "total_amount"}
    # schema default currency="USD" is not in the text, so it does not count as extracted
    assert "currency" in report.required_ungrounded


def test_audit_fabricated_output_scores_below_threshold() -> None:
    """Acceptance: the old fallback's 'John Doe' / 1500 output against the real Contoso text."""
    report, status = run(FABRICATED_FALLBACK_JSON)
    assert status == ExtractionStatus.NEEDS_REVIEW
    assert report.score < THRESHOLD
    assert {"vendor_name", "invoice_number", "total_amount"} <= set(report.required_ungrounded)


def test_low_ocr_quality_lowers_score() -> None:
    good, _ = run(CONTOSO_INVOICE_JSON, ocr=0.95)
    poor, _ = run(CONTOSO_INVOICE_JSON, ocr=0.10)
    assert poor.score < good.score


def test_breakdown_is_serialisable() -> None:
    import json

    report, _ = run(CONTOSO_INVOICE_JSON)
    data = json.loads(json.dumps(report.to_dict(), default=str))
    assert data["fields"]["vendor_name"]["grounded"] is True
    assert data["ocr_confidence"] == 0.92


def test_required_fields_defined_for_every_document_type() -> None:
    assert set(REQUIRED_FIELDS) == set(PromptBuilder.DOCUMENT_MODEL_MAP)
    for doc_type, fields in REQUIRED_FIELDS.items():
        props = PromptBuilder.get_json_schema(doc_type)["properties"]
        assert set(fields) <= set(props), doc_type


def test_receipt_consistency() -> None:
    text = "Corner Shop\n2026-11-01\nMilk 2.50\nBread 3.00\nSubtotal 5.50\nTax 0.50\nTotal 6.00"
    data = {
        "store_name": "Corner Shop",
        "transaction_date": "2026-11-01",
        "subtotal": 5.50,
        "tax": 0.50,
        "total_amount": 6.00,
        "line_items": [
            {"description": "Milk", "total_price": 2.50},
            {"description": "Bread", "total_price": 3.00},
        ],
    }
    report, status = run(data, text=text, doc_type="receipt")
    assert status == ExtractionStatus.COMPLETED, report.to_dict()
    _bad, bad_status = run({**data, "total_amount": 5.50}, text=text, doc_type="receipt")
    assert bad_status == ExtractionStatus.NEEDS_REVIEW


def test_purchase_order_consistency() -> None:
    text = "PO-55 Fabrikam 2026-09-01 Widgets 4 x 2.50 = 10.00 Total 10.00"
    data = {
        "po_number": "PO-55",
        "vendor_name": "Fabrikam",
        "order_date": "2026-09-01",
        "total_cost": 12.00,
        "items": [{"description": "Widgets", "quantity": 4, "unit_price": 2.50, "total_price": 10.00}],
    }
    report, status = run(data, text=text + " 12.00", doc_type="purchase_order")
    assert status == ExtractionStatus.NEEDS_REVIEW
    assert "items_sum_equals_total_cost" in report.to_dict()["failed_checks"]


def test_identifier_with_one_wrong_digit_is_not_grounded() -> None:
    """Found by evals/run_eval.py --mode routing: fuzzy matching accepted INV-...02 for INV-...01."""
    text = "INVOICE\nInvoice No: INV-20260001\nTotal 10.00"
    norm = normalise_text(text)
    assert ground_value("invoice_number", "INV-20260001", text, norm) is True
    assert ground_value("invoice_number", "INV-20260002", text, norm) is False
    assert ground_value("vendor_name", "Contoso Ltd.", "Contoso Ltd invoice", normalise_text("Contoso Ltd invoice"))
