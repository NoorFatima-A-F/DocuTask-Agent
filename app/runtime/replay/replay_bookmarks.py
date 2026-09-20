"""
Replay Bookmark Manager for Key Mission Milestones.
Tracks failure points, graph mutations, human interventions, and verification proofs.
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class BookmarkType(str, Enum):
    MISSION_START = "MISSION_START"
    PLANNER_MUTATION = "PLANNER_MUTATION"
    TASK_FAILURE = "TASK_FAILURE"
    RECOVERY_INJECTION = "RECOVERY_INJECTION"
    HUMAN_INTERVENTION = "HUMAN_INTERVENTION"
    SMT_VERIFICATION = "SMT_VERIFICATION"
    MISSION_COMPLETE = "MISSION_COMPLETE"
    CUSTOM = "CUSTOM"


class ReplayBookmark(BaseModel):
    bookmark_id: str = Field(..., description="Unique bookmark ID")
    mission_id: str = Field(..., description="Mission identifier")
    event_index: int = Field(..., description="0-indexed event index position")
    event_id: str = Field(..., description="Associated event ID")
    bookmark_type: BookmarkType = Field(..., description="Category of bookmark")
    label: str = Field(..., description="Human-readable milestone label")
    description: Optional[str] = Field(default=None, description="Detailed description")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ReplayBookmarkManager:
    """Manages bookmarks for a mission replay."""

    def __init__(self, mission_id: str):
        self.mission_id = mission_id
        self._bookmarks: Dict[str, ReplayBookmark] = {}

    def add_bookmark(
        self,
        event_index: int,
        event_id: str,
        bookmark_type: BookmarkType,
        label: str,
        description: Optional[str] = None,
        bookmark_id: Optional[str] = None,
    ) -> ReplayBookmark:
        b_id = bookmark_id or f"bm_{self.mission_id}_{event_index}_{bookmark_type.value.lower()}"
        bm = ReplayBookmark(
            bookmark_id=b_id,
            mission_id=self.mission_id,
            event_index=event_index,
            event_id=event_id,
            bookmark_type=bookmark_type,
            label=label,
            description=description,
        )
        self._bookmarks[b_id] = bm
        return bm

    def get_bookmark(self, bookmark_id: str) -> Optional[ReplayBookmark]:
        return self._bookmarks.get(bookmark_id)

    def list_bookmarks(self) -> List[ReplayBookmark]:
        return sorted(list(self._bookmarks.values()), key=lambda b: b.event_index)

    def remove_bookmark(self, bookmark_id: str) -> bool:
        return self._bookmarks.pop(bookmark_id, None) is not None
