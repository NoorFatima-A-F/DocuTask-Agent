"""
Decision Validation Engine - Replay Verifier
Asserts that decisions replayed through ESMR event sourcing yield bitwise-identical plan selections.
"""

from typing import Dict, List, Any, Callable


class ReplayVerifier:
    """Verifies that an optimizer decision is 100% reproducible when replayed."""

    @staticmethod
    def verify_replay_determinism(
        optimize_fn: Callable[[List[Dict[str, Any]], Dict[str, float]], Dict[str, Any]],
        candidates: List[Dict[str, Any]],
        constraints: Dict[str, float],
        original_decision_id: str,
        trials: int = 5,
    ) -> bool:
        for _ in range(trials):
            result = optimize_fn(candidates, constraints)
            sel = result.get("selected_plan", {})
            sel_id = sel.get("id") or sel.get("plan_id")
            if sel_id != original_decision_id:
                return False
        return True
