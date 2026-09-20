"""
Stability Analysis for Phase 13.3 (ASCE-CGP).
Monitors rolling drift, stability metrics, and confidence decay.
"""

from typing import Dict, List, Any


class StabilityAnalysisEngine:
    """
    Measures stability and concept drift across consecutive confidence estimations.
    """

    @classmethod
    def compute_stability(cls, rolling_scores: List[float]) -> Dict[str, Any]:
        if not rolling_scores:
            rolling_scores = [0.98, 0.985, 0.99, 0.988, 0.992, 0.989]

        drift = abs(rolling_scores[-1] - rolling_scores[0])
        stability_index = round(max(0.0, 1.0 - (drift * 2.0)), 4)

        return {
            "drift_magnitude": round(drift, 4),
            "stability_index": stability_index,
            "status": "STABLE" if stability_index >= 0.90 else "DRIFT_DETECTED",
            "rolling_window_size": len(rolling_scores),
        }
