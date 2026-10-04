"""
evals/metrics/extraction_accuracy.py
Calculates entity-level precision, recall, F1, exact match, and numerical field tolerance.
"""

from __future__ import annotations
import math
from typing import Any, Dict, List


def calculate_extraction_accuracy(
    ground_truth: Dict[str, Any],
    extracted: Dict[str, Any],
    numerical_tolerance: float = 0.01,
) -> Dict[str, Any]:
    """Evaluates extraction accuracy between ground truth entities and extracted entities."""
    if not ground_truth:
        return {
            "exact_match_ratio": 1.0,
            "field_accuracy": 1.0,
            "total_fields": 0,
            "matched_fields": 0,
            "field_details": {},
        }

    total_fields = len(ground_truth)
    matched_fields = 0
    field_details: Dict[str, Dict[str, Any]] = {}

    for key, expected_val in ground_truth.items():
        if key not in extracted:
            field_details[key] = {
                "matched": False,
                "expected": expected_val,
                "actual": None,
                "reason": "missing_key",
            }
            continue

        actual_val = extracted[key]
        is_match = False

        if isinstance(expected_val, (int, float)) and isinstance(actual_val, (int, float)):
            diff = abs(float(expected_val) - float(actual_val))
            if math.isclose(float(expected_val), float(actual_val), rel_tol=numerical_tolerance, abs_tol=1e-3):
                is_match = True
            elif diff < 1e-4:
                is_match = True
        elif isinstance(expected_val, str) and isinstance(actual_val, str):
            if expected_val.strip().lower() == actual_val.strip().lower():
                is_match = True
        elif expected_val == actual_val:
            is_match = True

        if is_match:
            matched_fields += 1
            field_details[key] = {"matched": True, "expected": expected_val, "actual": actual_val}
        else:
            field_details[key] = {
                "matched": False,
                "expected": expected_val,
                "actual": actual_val,
                "reason": "value_mismatch",
            }

    field_accuracy = round(matched_fields / total_fields, 4) if total_fields > 0 else 1.0
    exact_match = 1.0 if matched_fields == total_fields else 0.0

    return {
        "exact_match_ratio": exact_match,
        "field_accuracy": field_accuracy,
        "total_fields": total_fields,
        "matched_fields": matched_fields,
        "field_details": field_details,
    }
