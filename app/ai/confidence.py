"""Evidence-based extraction confidence.

A score is computed from evidence in the source document, not from how many fields the
model filled in:

* **Grounding** - does each extracted scalar value appear in the OCR text (numbers with
  locale-aware parsing, dates normalised to ISO, strings by fuzzy match)?
* **Required-field completeness** - per document type; schema defaults (e.g. a currency
  of ``USD``) only count if they are grounded.
* **Consistency** - arithmetic and date checks (line items vs subtotal, subtotal + tax vs
  total, due date vs issue date, quantity x unit price vs line total).
* **OCR quality** - mean word confidence of the source pages.

The document score is a weighted mean, capped by the weakest required field, and capped
below the review threshold when any consistency check fails. ``routing_status`` turns the
result into ``COMPLETED`` or ``NEEDS_REVIEW``.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from typing import Any

from dateutil import parser as date_parser
from rapidfuzz import fuzz

from app.core.errors.extraction import ExtractionStatus

#: Required fields per document type (single source of truth).
REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "invoice": ("invoice_number", "vendor_name", "invoice_date", "total_amount", "currency"),
    "receipt": ("store_name", "transaction_date", "total_amount"),
    "purchase_order": ("po_number", "vendor_name", "order_date", "total_cost"),
    "resume": ("full_name",),
    "passport": ("passport_number", "surname", "date_of_birth", "expiry_date"),
    "driver_license": ("license_number", "full_name", "date_of_birth", "expiry_date"),
    "national_id": ("id_number", "full_name", "date_of_birth"),
    "medical_report": ("patient_name", "visit_date"),
    "insurance_form": ("policy_number", "policyholder_name", "insurer_name"),
    "contract": ("contract_title", "effective_date"),
    "bank_statement": ("bank_name", "account_number", "closing_balance"),
    "utility_bill": ("utility_company", "account_number", "amount_due", "due_date"),
    "research_paper": ("title",),
    "generic": (),
}

#: Free-text fields the model writes in its own words; they are not expected to appear verbatim.
UNGROUNDABLE_FIELDS = frozenset({"summary", "abstract", "conclusions", "recommendations", "diagnosis"})

CURRENCY_SYMBOLS = {"€": "EUR", "$": "USD", "£": "GBP", "¥": "JPY", "₹": "INR", "₨": "PKR", "CHF": "CHF"}

WEIGHT_GROUNDING = 0.5
WEIGHT_REQUIRED = 0.3
WEIGHT_OCR = 0.2
FUZZY_THRESHOLD = 90
AMOUNT_TOLERANCE = 0.01


@dataclass
class FieldEvidence:
    value: Any
    grounded: bool | None  # None when the value is null or not groundable
    score: float | None
    required: bool = False


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str


@dataclass
class ConfidenceReport:
    score: float
    fields: dict[str, FieldEvidence] = field(default_factory=dict)
    required_missing: list[str] = field(default_factory=list)
    required_ungrounded: list[str] = field(default_factory=list)
    checks: list[CheckResult] = field(default_factory=list)
    ocr_confidence: float | None = None

    @property
    def failed_checks(self) -> list[CheckResult]:
        return [c for c in self.checks if not c.passed]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["failed_checks"] = [c.name for c in self.failed_checks]
        return data


# --------------------------------------------------------------------------- normalisation

#: Unsigned numbers (signs are dropped; values are compared by magnitude).
_NUMBER_RE = re.compile(r"(?<![\d.,])\d{1,3}(?:[.,' ]\d{3})*(?:[.,]\d+)?(?!\d)|\d+(?:[.,]\d+)?")


def parse_number(token: str) -> float | None:
    """Parse ``1.234,56`` / ``1,234.56`` / ``1234.5`` / ``1 234,56`` into a float."""
    t = token.strip().replace("'", "").replace(" ", "").replace("\u00a0", "")
    if not t or not re.search(r"\d", t):
        return None
    last_dot, last_comma = t.rfind("."), t.rfind(",")
    if last_dot >= 0 and last_comma >= 0:
        decimal = "." if last_dot > last_comma else ","
        thousands = "," if decimal == "." else "."
        t = t.replace(thousands, "").replace(decimal, ".")
    elif last_comma >= 0:
        # "1,234" (thousands) vs "12,34" (decimal): 3 trailing digits => thousands separator.
        t = t.replace(",", "") if len(t) - last_comma - 1 == 3 and t.count(",") >= 1 else t.replace(",", ".")
    elif t.count(".") > 1:
        t = t.replace(".", "")
    try:
        return float(t)
    except ValueError:
        return None


def numbers_in(text: str) -> list[float]:
    found = []
    for match in _NUMBER_RE.finditer(text):
        value = parse_number(match.group(0))
        if value is not None:
            found.append(value)
    return found


def parse_date(value: str) -> date | None:
    try:
        parsed: datetime = date_parser.parse(value, fuzzy=False)
        return parsed.date()
    except (ValueError, OverflowError, TypeError):
        return None


_DATE_CANDIDATE_RE = re.compile(
    r"\b\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\b"
    r"|\b\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}\b"
    r"|\b\d{1,2}\s+[A-Za-z]{3,9}\.?,?\s+\d{4}\b"
    r"|\b[A-Za-z]{3,9}\.?\s+\d{1,2},?\s+\d{4}\b"
)


def dates_in(text: str) -> set[date]:
    found: set[date] = set()
    for match in _DATE_CANDIDATE_RE.finditer(text):
        token = match.group(0)
        for dayfirst in (False, True):
            try:
                found.add(date_parser.parse(token, dayfirst=dayfirst).date())
            except (ValueError, OverflowError):
                continue
    return found


def normalise_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    value = re.sub(r"[^\w\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


# --------------------------------------------------------------------------- grounding


def _looks_like_date_field(name: str) -> bool:
    return name.endswith("_date") or name in {"date_of_birth", "patient_dob", "publication_date"}


def ground_value(name: str, value: Any, text: str, norm_text: str) -> bool | None:
    """True/False if the value is (not) supported by the text; None if null or not groundable."""
    if value is None or value == "" or isinstance(value, (list, dict, bool)):
        return None
    if name in UNGROUNDABLE_FIELDS:
        return None
    if isinstance(value, (int, float)):
        return any(abs(n - abs(float(value))) <= AMOUNT_TOLERANCE for n in numbers_in(text))
    sval = str(value).strip()
    if name == "currency":
        code = sval.upper()
        if re.search(rf"\b{re.escape(code)}\b", text, re.IGNORECASE):
            return True
        return any(sym in text for sym, c in CURRENCY_SYMBOLS.items() if c == code)
    if _looks_like_date_field(name):
        parsed = parse_date(sval)
        if parsed is not None:
            return parsed in dates_in(text)
    needle = normalise_text(sval)
    if not needle:
        return None
    if needle in norm_text:
        return True
    if any(ch.isdigit() for ch in needle):
        # Identifiers, account numbers, addresses: one wrong digit is a different value, so no fuzzy match.
        return False
    return fuzz.partial_ratio(needle, norm_text) >= FUZZY_THRESHOLD


# --------------------------------------------------------------------------- consistency


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= max(AMOUNT_TOLERANCE, 0.005 * max(abs(a), abs(b)))


def _num(value: Any) -> float | None:
    """A JSON number as float; ``None`` for anything else (bools are not numbers here)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _line_checks(items: list[dict[str, Any]], prefix: str) -> list[CheckResult]:
    checks = []
    for i, item in enumerate(items):
        qty, unit, total = _num(item.get("quantity")), _num(item.get("unit_price")), _num(item.get("total_price"))
        if qty is not None and unit is not None and total:
            ok = _close(qty * unit, total)
            checks.append(CheckResult(f"{prefix}[{i}].quantity_x_unit_price", ok, f"{qty} x {unit} vs {total}"))
    return checks


def _sum_check(items: list[dict[str, Any]], target: Any, name: str) -> list[CheckResult]:
    totals = [it.get("total_price") for it in items]
    if not items or not isinstance(target, (int, float)) or not all(isinstance(t, (int, float)) for t in totals):
        return []
    s = round(sum(totals), 2)  # type: ignore[arg-type]
    return [CheckResult(name, _close(s, target), f"sum(line totals)={s} vs {target}")]


def _date_order(data: dict[str, Any], first: str, second: str) -> list[CheckResult]:
    a, b = data.get(first), data.get(second)
    da = parse_date(a) if isinstance(a, str) else None
    db = parse_date(b) if isinstance(b, str) else None
    if da is None or db is None:
        return []
    return [CheckResult(f"{second}_after_{first}", db >= da, f"{first}={da} {second}={db}")]


def consistency_checks(document_type: str, data: dict[str, Any]) -> list[CheckResult]:
    checks: list[CheckResult] = []
    if document_type in ("invoice", "receipt"):
        items = data.get("line_items") or []
        subtotal = data.get("subtotal")
        tax = data.get("tax_amount") if document_type == "invoice" else data.get("tax")
        total = data.get("total_amount")
        checks += _line_checks(items, "line_items")
        checks += _sum_check(items, subtotal, "line_items_sum_equals_subtotal")
        subtotal_n, tax_n, total_n = _num(subtotal), _num(tax), _num(total)
        if subtotal_n is not None and tax_n is not None and total_n is not None:
            checks.append(
                CheckResult(
                    "subtotal_plus_tax_equals_total",
                    _close(subtotal_n + tax_n, total_n),
                    f"{subtotal} + {tax} vs {total}",
                )
            )
        elif subtotal is None and not isinstance(tax, (int, float)):
            checks += _sum_check(items, total, "line_items_sum_equals_total")
        if document_type == "invoice":
            checks += _date_order(data, "invoice_date", "due_date")
    elif document_type == "purchase_order":
        items = data.get("items") or []
        checks += _line_checks(items, "items")
        checks += _sum_check(items, data.get("total_cost"), "items_sum_equals_total_cost")
        checks += _date_order(data, "order_date", "delivery_date")
    elif document_type in ("passport", "driver_license"):
        checks += _date_order(data, "issue_date", "expiry_date")
    return checks


# --------------------------------------------------------------------------- scoring


def assess(
    document_type: str,
    data: dict[str, Any],
    ocr_text: str,
    ocr_confidence: float | None,
    threshold: float,
) -> ConfidenceReport:
    """Score a validated extraction against its source text."""
    required = REQUIRED_FIELDS.get(document_type, ())
    norm_text = normalise_text(ocr_text)

    fields: dict[str, FieldEvidence] = {}
    for name, value in data.items():
        grounded = ground_value(name, value, ocr_text, norm_text)
        fields[name] = FieldEvidence(
            value=value,
            grounded=grounded,
            score=None if grounded is None else float(grounded),
            required=name in required,
        )

    missing = [f for f in required if data.get(f) in (None, "", [], {})]
    ungrounded = [f for f in required if f not in missing and fields[f].grounded is False]

    groundable = [f for f in fields.values() if f.grounded is not None]
    grounding_rate = sum(f.grounded for f in groundable) / len(groundable) if groundable else 0.0  # type: ignore[misc]
    if required:
        ok_required = len(required) - len(missing) - len(ungrounded)
        completeness = ok_required / len(required)
    else:
        completeness = 1.0 if groundable else 0.0

    parts = [(WEIGHT_GROUNDING, grounding_rate), (WEIGHT_REQUIRED, completeness)]
    if ocr_confidence is not None:
        parts.append((WEIGHT_OCR, ocr_confidence))
    score = sum(w * v for w, v in parts) / sum(w for w, _ in parts)

    if required:
        # Capped by the weakest required field: any missing/ungrounded required field scores 0.
        score = min(score, 0.0 if (missing or ungrounded) else 1.0)
    elif not groundable:
        score = 0.0  # nothing verifiable was extracted

    checks = consistency_checks(document_type, data)
    if any(not c.passed for c in checks):
        score = min(score, max(0.0, threshold - 0.01))

    return ConfidenceReport(
        score=round(score, 4),
        fields=fields,
        required_missing=missing,
        required_ungrounded=ungrounded,
        checks=checks,
        ocr_confidence=ocr_confidence,
    )


def routing_status(report: ConfidenceReport, threshold: float) -> ExtractionStatus:
    """COMPLETED only when every gate passes; otherwise a human must review it."""
    if report.score < threshold or report.required_missing or report.required_ungrounded or report.failed_checks:
        return ExtractionStatus.NEEDS_REVIEW
    return ExtractionStatus.COMPLETED
