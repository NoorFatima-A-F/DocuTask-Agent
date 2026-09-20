"""
Replay Executor for Phase 13.4.
Executes frame-by-frame state derivation from event logs without running underlying business actions.
"""

from typing import Dict, Any, List
from app.runtime.replay.reconstruction.mission_reconstructor import MissionReconstructor


class ReplayExecutor:
    """
    Frame-by-frame state derivation engine.
    """

    @classmethod
    def execute_frame(
        cls,
        mission_id: str,
        events: List[Dict[str, Any]],
        cursor: int,
    ) -> Dict[str, Any]:
        state = MissionReconstructor.reconstruct_up_to_cursor(mission_id, events, cursor)
        target_ev = events[cursor] if (0 <= cursor < len(events)) else {}

        return {
            "mission_id": mission_id,
            "cursor": cursor,
            "event_id": target_ev.get("event_id"),
            "event_type": target_ev.get("event_type"),
            "timestamp": target_ev.get("timestamp"),
            "reconstructed_state": state.model_dump(),
        }
