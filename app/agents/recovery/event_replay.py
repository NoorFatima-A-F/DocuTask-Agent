"""
Event Replay Engine.
Replays domain events from event logs for deterministic state recreation.
"""

from typing import Any, Dict, List


class EventReplayEngine:
    """Replays domain events sequentially to reconstruct state."""

    def replay_events(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        reconstructed_state: Dict[str, Any] = {}
        for event in events:
            payload = event.get("payload", {})
            reconstructed_state.update(payload)
        return reconstructed_state
