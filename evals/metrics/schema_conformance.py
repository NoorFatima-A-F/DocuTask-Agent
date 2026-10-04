"""
evals/metrics/schema_conformance.py
Evaluates schema field-match accuracy, type consistency, and hallucination rate.
"""

from __future__ import annotations
from typing import Any, Dict


def calculate_schema_conformance(ground_truth: Dict[str, Any], extracted: Dict[str, Any]) -> float:
    """Calculates field-level matching accuracy between ground truth and extracted schema."""
    if not ground_truth:
        return 1.0

    matches = 0
    total = len(ground_truth)

    for key, expected_val in ground_truth.items():
        if key in extracted:
            actual_val = extracted[key]
            # Handle float comparison with precision tolerance
            if isinstance(expected_val, float) and isinstance(actual_val, (int, float)):
                if abs(float(expected_val) - float(actual_val)) < 1e-4:
                    matches += 1
            elif str(expected_val).strip().lower() == str(actual_val).strip().lower():
                matches += 1

    return round(matches / total, 4)
