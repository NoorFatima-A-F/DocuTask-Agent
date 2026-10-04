"""
evals/metrics/schema_conformity.py
Evaluates schema validity, required key presence, and type conformity for extracted payloads.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional


def evaluate_schema_conformity(
    extracted_data: Dict[str, Any],
    expected_schema: Dict[str, Any],
    required_fields: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Computes schema conformance ratio, missing keys, and unexpected type mismatches."""
    if not expected_schema:
        return {"conformance_score": 1.0, "missing_fields": [], "type_mismatches": []}

    target_fields = required_fields if required_fields else list(expected_schema.keys())
    missing_fields: List[str] = []
    type_mismatches: List[str] = []
    matched_count = 0

    for key in target_fields:
        if key not in extracted_data:
            missing_fields.append(key)
            continue

        actual_val = extracted_data[key]
        expected_val = expected_schema.get(key)

        if expected_val is not None and actual_val is not None:
            expected_type = type(expected_val)
            # Allow int/float interchangeability
            if expected_type in (int, float) and isinstance(actual_val, (int, float)):
                matched_count += 1
            elif isinstance(actual_val, expected_type):
                matched_count += 1
            else:
                type_mismatches.append(f"{key}: expected {expected_type.__name__}, got {type(actual_val).__name__}")
        else:
            matched_count += 1

    total_target = len(target_fields)
    conformance_score = round(matched_count / total_target, 4) if total_target > 0 else 1.0

    return {
        "conformance_score": conformance_score,
        "missing_fields": missing_fields,
        "type_mismatches": type_mismatches,
        "is_valid": len(missing_fields) == 0 and len(type_mismatches) == 0,
    }
