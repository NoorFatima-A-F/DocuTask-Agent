"""
Projection Verifier for Phase 13.4.
Verifies that reconstructed read projections are monotonically consistent.
"""

from typing import Dict, Any, List, Tuple


class ProjectionVerifier:
    """
    Validates projection monotonic invariance during replay.
    """

    @classmethod
    def verify_projections(
        cls,
        events: List[Dict[str, Any]],
    ) -> Tuple[bool, List[str]]:
        errors = []
        last_cursor = -1
        for idx, ev in enumerate(events):
            cursor = ev.get("cursor", idx)
            if cursor < last_cursor:
                errors.append(f"Non-monotonic cursor sequence at index {idx}: {cursor} < {last_cursor}")
            last_cursor = cursor
        return len(errors) == 0, errors
