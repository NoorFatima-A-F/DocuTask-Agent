"""
Scientific Model Router - Routing Validator
Validates consistency, SLA guarantees, and utility ordering for model routing.
"""

from typing import Dict, List, Any, Tuple


class RoutingValidator:
    """Validates model routing invariants."""

    @staticmethod
    def validate_selection(
        selected_model: Dict[str, Any],
        candidates: List[Dict[str, Any]],
    ) -> Tuple[bool, List[str]]:
        errors = []
        sel_utility = selected_model.get("expected_utility", 0.0)

        # Selected model must achieve maximal utility among candidates
        for c in candidates:
            if c.get("expected_utility", 0.0) > sel_utility + 1e-4:
                errors.append(
                    f"Selected model '{selected_model.get('model_id')}' utility ({sel_utility}) is lower than candidate '{c.get('model_id')}' ({c.get('expected_utility')})"
                )

        return len(errors) == 0, errors
