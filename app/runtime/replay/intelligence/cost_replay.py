"""
Cost Replay for Phase 13.4.
Tracks dollar cost accumulation and model token expenditure over replay frames.
"""

from typing import Dict, Any, List


class CostReplayEngine:
    """
    Computes cumulative cost curve along mission timeline.
    """

    @classmethod
    def compute_cost_trajectory(cls, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        trajectory = []
        cum_cost = 0.0
        cum_tokens = 0

        for idx, ev in enumerate(events):
            payload = ev.get("payload", {})
            cost = float(payload.get("cost_usd", 0.0))
            tokens = int(payload.get("tokens_used", 0) or payload.get("prompt_tokens", 0))

            cum_cost += cost
            cum_tokens += tokens

            trajectory.append({
                "cursor": idx,
                "event_id": ev.get("event_id"),
                "incremental_cost_usd": round(cost, 6),
                "cumulative_cost_usd": round(cum_cost, 6),
                "cumulative_tokens": cum_tokens,
            })

        return trajectory
