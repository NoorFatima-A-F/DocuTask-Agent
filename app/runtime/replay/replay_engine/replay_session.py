"""
Replay Session for Phase 13.4.
Encapsulates runtime state, cursor position, speed, and bookmarks for an active replay session.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import uuid


class ReplayBookmark(BaseModel):
    bookmark_id: str
    cursor: int
    label: str
    category: str = "MILESTONE"
    note: Optional[str] = None


class ReplaySessionState(BaseModel):
    session_id: str = Field(default_factory=lambda: f"rpl_sess_{uuid.uuid4().hex[:10]}")
    mission_id: str
    status: str = "PAUSED"
    current_cursor: int = 0
    total_events: int = 0
    playback_speed: float = 1.0
    is_reverse: bool = False
    bookmarks: List[ReplayBookmark] = Field(default_factory=list)
    active_frame_data: Optional[Dict[str, Any]] = None
