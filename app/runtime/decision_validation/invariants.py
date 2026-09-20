"""
Decision Validation Engine - Invariant Checkers
Asserts mathematical, physical, and domain bounds on optimization outputs.
"""

from typing import Dict, List, Any, Tuple
import math


class InvariantChecker:
    """Verifies that decisions satisfy axiomatic mathematical invariants."""

    @staticmethod
    def check_decision_invariants(decision_record: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []

        # 1. Non-negativity of cost and latency
        cost = decision_record.get("cost_usd", 0.0)
        lat = decision_record.get("latency_ms", 0.0)
        if cost < 0.0:
            errors.append(f"Invariant violation: cost (${cost}) cannot be negative.")
        if lat < 0.0:
            errors.append(f"Invariant violation: latency ({lat}ms) cannot be negative.")

        # 2. Probability bounds [0, 1]
        for prob_key in ["accuracy", "confidence", "reliability", "overall_risk"]:
            if prob_key in decision_record:
                val = decision_record[prob_key]
                if val < 0.0 or val > 1.0 + 1e-6:
                    errors.append(f"Invariant violation: probability '{prob_key}'={val} outside [0, 1].")

        # 3. Utility monotonicity
        utility = decision_record.get("utility", decision_record.get("expected_utility", 0.0))
        if utility < 0.0 or utility > 1.0 + 1e-6:
            errors.append(f"Invariant violation: utility={utility} outside [0, 1].")

        return len(errors) == 0, errors
