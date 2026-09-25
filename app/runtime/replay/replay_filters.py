"""
Replay Event Filtering Subsystem.
Allows filtering event logs by category, severity, worker, and execution stages.
"""

from typing import List, Optional, Set
from pydantic import BaseModel, Field
from app.runtime.observability.schemas import EventCategory, EventSeverity, RuntimeEvent


class ReplayFilterCriteria(BaseModel):
    categories: Optional[Set[EventCategory]] = Field(default=None, description="Categories to include")
    severities: Optional[Set[EventSeverity]] = Field(default=None, description="Severities to include")
    stages: Optional[Set[str]] = Field(default=None, description="Execution stages to include")
    worker_ids: Optional[Set[str]] = Field(default=None, description="Specific workers to filter")
    errors_only: bool = Field(default=False, description="Filter only failure and error events")
    min_timestamp: Optional[str] = Field(default=None, description="Inclusive start ISO timestamp")
    max_timestamp: Optional[str] = Field(default=None, description="Inclusive end ISO timestamp")

    def matches(self, event: RuntimeEvent) -> bool:
        """Determines if a given RuntimeEvent satisfies the filter criteria."""
        if self.errors_only and event.severity not in {EventSeverity.ERROR, EventSeverity.CRITICAL}:
            return False

        if self.categories and event.category not in self.categories:
            return False

        if self.severities and event.severity not in self.severities:
            return False

        if self.stages and event.stage not in self.stages:
            return False

        if self.worker_ids and event.worker_id not in self.worker_ids:
            return False

        if self.min_timestamp and event.timestamp < self.min_timestamp:
            return False

        if self.max_timestamp and event.timestamp > self.max_timestamp:
            return False

        return True


class ReplayFilterEngine:
    @staticmethod
    def apply_filters(events: List[RuntimeEvent], criteria: Optional[ReplayFilterCriteria]) -> List[RuntimeEvent]:
        """Applies filter criteria to a sequence of events."""
        if not criteria:
            return list(events)
        return [e for e in events if criteria.matches(e)]
