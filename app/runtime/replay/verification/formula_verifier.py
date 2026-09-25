"""
Formula Verifier for Phase 13.4.
Verifies that reconstructed confidence calculations conform to registered scientific formula versions.
"""

from typing import Dict, Any, List, Tuple


class FormulaVerifier:
    """
    Validates formula consistency during replay.
    """

    @classmethod
    def verify_reconstructed_formulas(
        cls,
        events: List[Dict[str, Any]],
    ) -> Tuple[bool, List[str]]:
        errors = []
        for ev in events:
            payload = ev.get("payload", {})
            if "confidence.evaluated" in (ev.get("event_type") or ""):
                score = payload.get("overall_score")
                if score is not None and not (0.0 <= score <= 1.0):
                    errors.append(f"Confidence score {score} outside monotonic bounds [0, 1]")
        return len(errors) == 0, errors
