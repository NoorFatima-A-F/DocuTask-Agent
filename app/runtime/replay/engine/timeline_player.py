"""
Timeline Player for Phase 13.4.
Generates ordered chronological frame buffers for smooth UI playback streaming.
"""

from typing import Dict, Any, List


class TimelinePlayer:
    """
    Chronological event stepping and delta stream player.
    """

    @classmethod
    def generate_timeline_frames(
        cls,
        events: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        frames = []
        for idx, ev in enumerate(events):
            evt_type = ev.get("event_type", "")
            frames.append({
                "frame_index": idx,
                "event_id": ev.get("event_id"),
                "event_type": evt_type,
                "subsystem": evt_type.split(".")[0] if "." in evt_type else "core",
                "timestamp": ev.get("timestamp"),
                "summary": ev.get("payload", {}).get("goal") or ev.get("payload", {}).get("selected_strategy") or evt_type,
                "confidence": ev.get("payload", {}).get("overall_score") or ev.get("payload", {}).get("confidence"),
            })
        return frames
