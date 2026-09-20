"""
Replay Cursor Subsystem.
Maintains state position, progress ratio, active event reference, and navigation limits.
"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class ReplayCursor(BaseModel):
    current_index: int = Field(default=0, ge=0, description="Current event index")
    total_events: int = Field(default=0, ge=0, description="Total events available in stream")
    current_event_id: Optional[str] = Field(default=None, description="Active event ID under cursor")
    current_timestamp: Optional[str] = Field(default=None, description="ISO timestamp of active event")
    is_at_start: bool = Field(default=True, description="True if at index 0")
    is_at_end: bool = Field(default=False, description="True if at last event")
    progress_percentage: float = Field(default=0.0, ge=0.0, le=100.0, description="Progress (0.0 to 100.0)")
    last_seek_time: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def update_position(self, index: int, total: int, event_id: Optional[str] = None, timestamp: Optional[str] = None) -> None:
        """Updates cursor metrics safely bounded by [0, max(0, total - 1)]."""
        self.total_events = total
        if total == 0:
            self.current_index = 0
            self.is_at_start = True
            self.is_at_end = True
            self.progress_percentage = 0.0
            self.current_event_id = None
            self.current_timestamp = None
            return

        clamped = max(0, min(index, total - 1))
        self.current_index = clamped
        self.current_event_id = str(event_id) if event_id is not None else None
        self.current_timestamp = str(timestamp) if timestamp is not None else None
        self.is_at_start = (clamped == 0)
        self.is_at_end = (clamped >= total - 1)
        self.progress_percentage = round((clamped / max(1, total - 1)) * 100.0, 2)
        self.last_seek_time = datetime.now(timezone.utc).isoformat()
