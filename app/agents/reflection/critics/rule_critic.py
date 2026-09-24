"""
Rule Critic for Multi-Critic Reflection System.
Performs deterministic mathematical verification, schema completeness, and format validation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class CritiqueFeedback:
    """Individual critique score and diagnostic details."""

    critic_name: str
    score: float  # 0.0 to 1.0
    passed: bool
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)


class RuleCritic:
    """Deterministic validator evaluating arithmetic consistency, mandatory keys, and regex formats."""

    def evaluate(self, data: Dict[str, Any]) -> CritiqueFeedback:
        """Evaluates extracted document payload against strict financial and structural rules."""
        issues: List[str] = []
        suggestions: List[str] = []
        total_checks = 0
        passed_checks = 0

        # 1. Schema & Mandatory Field Completeness
        mandatory_fields = ["vendor_name", "invoice_number", "total_amount"]
        for f in mandatory_fields:
            total_checks += 1
            if f in data and data[f] is not None and str(data[f]).strip() != "":
                passed_checks += 1
            else:
                issues.append(f"Missing or empty mandatory field: '{f}'")
                suggestions.append(f"Re-extract document specifically targeting field '{f}'")

        # 2. Arithmetic Consistency (Subtotal + Tax == Total)
        total_amt = data.get("total_amount")
        subtotal = data.get("subtotal")
        tax = data.get("tax_amount", 0.0)

        if total_amt is not None and subtotal is not None:
            total_checks += 1
            try:
                t_val = float(str(total_amt).replace("$", "").replace(",", "").strip())
                s_val = float(str(subtotal).replace("$", "").replace(",", "").strip())
                tax_val = float(str(tax).replace("$", "").replace(",", "").strip()) if tax else 0.0
                
                expected_total = s_val + tax_val
                if abs(t_val - expected_total) < 0.02:
                    passed_checks += 1
                else:
                    issues.append(
                        f"Arithmetic mismatch: Subtotal ({s_val:.2f}) + Tax ({tax_val:.2f}) = {expected_total:.2f} != Total ({t_val:.2f})"
                    )
                    suggestions.append("Recalculate invoice totals using table line items.")
            except (ValueError, TypeError) as ex:
                issues.append(f"Could not parse numeric amounts for math validation: {ex}")

        # 3. Line Items Sum Check (if present)
        line_items = data.get("line_items")
        if isinstance(line_items, list) and line_items and subtotal is not None:
            total_checks += 1
            try:
                line_sum = 0.0
                for item in line_items:
                    if isinstance(item, dict) and "amount" in item:
                        line_sum += float(str(item["amount"]).replace("$", "").replace(",", "").strip())
                s_val = float(str(subtotal).replace("$", "").replace(",", "").strip())
                if abs(line_sum - s_val) < 0.05:
                    passed_checks += 1
                else:
                    issues.append(f"Line items sum ({line_sum:.2f}) does not match subtotal ({s_val:.2f})")
                    suggestions.append("Check line items bounding boxes for missed rows.")
            except Exception:
                pass

        score = (passed_checks / total_checks) if total_checks > 0 else 1.0
        return CritiqueFeedback(
            critic_name="RuleCritic",
            score=round(score, 4),
            passed=score >= 0.85 and len(issues) == 0,
            issues=issues,
            suggestions=suggestions,
        )
