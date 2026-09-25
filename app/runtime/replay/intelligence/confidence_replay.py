"""
Confidence Replay for Phase 13.4.
Computes frame-by-frame confidence evolution curves and uncertainty bands.
"""

from typing import Dict, Any, List


class ConfidenceReplayEngine:
    """
    Computes confidence score and uncertainty trajectory over replay frames.
    """

    @classmethod
    def compute_trajectory(cls, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        trajectory = []
        curr_score = 0.50
        curr_unc = 0.20

        for idx, ev in enumerate(events):
            payload = ev.get("payload", {})
            if "overall_score" in payload or "confidence" in payload:
                curr_score = float(payload.get("overall_score") or payload.get("confidence"))
            if "total_uncertainty" in payload:
                curr_unc = float(payload["total_uncertainty"])

            trajectory.append({
                "cursor": idx,
                "event_id": ev.get("event_id"),
                "confidence_score": round(curr_score, 4),
                "uncertainty_band": round(curr_unc, 4),
                "ci_lower": round(max(0.0, curr_score - curr_unc), 4),
                "ci_upper": round(min(1.0, curr_score + curr_unc), 4),
            })

        return trajectory
