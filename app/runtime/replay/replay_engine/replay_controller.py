"""
Replay Controller for Phase 13.4.
Manages playback actions (play, pause, step forward, step backward, seek, jump to bookmark).
"""

from typing import Dict, Optional
from app.runtime.replay.replay_engine.replay_session import ReplaySessionState, ReplayBookmark


class ReplayController:
    """
    Stateful replay playback manager.
    """

    def __init__(self):
        self._sessions: Dict[str, ReplaySessionState] = {}

    def create_session(self, mission_id: str, total_events: int) -> ReplaySessionState:
        session = ReplaySessionState(
            mission_id=mission_id,
            total_events=total_events,
            status="PAUSED",
            current_cursor=0,
        )
        self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[ReplaySessionState]:
        return self._sessions.get(session_id)

    def play(self, session_id: str, speed: float = 1.0) -> ReplaySessionState:
        s = self._get_required(session_id)
        s.status = "PLAYING"
        s.playback_speed = speed
        s.is_reverse = False
        return s

    def pause(self, session_id: str) -> ReplaySessionState:
        s = self._get_required(session_id)
        s.status = "PAUSED"
        return s

    def step_forward(self, session_id: str) -> ReplaySessionState:
        s = self._get_required(session_id)
        if s.current_cursor < s.total_events - 1:
            s.current_cursor += 1
        return s

    def step_backward(self, session_id: str) -> ReplaySessionState:
        s = self._get_required(session_id)
        if s.current_cursor > 0:
            s.current_cursor -= 1
        return s

    def seek_to(self, session_id: str, target_cursor: int) -> ReplaySessionState:
        s = self._get_required(session_id)
        s.current_cursor = max(0, min(s.total_events - 1, target_cursor))
        return s

    def add_bookmark(self, session_id: str, label: str, note: Optional[str] = None) -> ReplayBookmark:
        import uuid
        s = self._get_required(session_id)
        bm = ReplayBookmark(
            bookmark_id=f"bm_{uuid.uuid4().hex[:8]}",
            cursor=s.current_cursor,
            label=label,
            note=note,
        )
        s.bookmarks.append(bm)
        return bm

    def _get_required(self, session_id: str) -> ReplaySessionState:
        s = self._sessions.get(session_id)
        if not s:
            raise KeyError(f"Replay session {session_id} not found")
        return s


replay_controller = ReplayController()
