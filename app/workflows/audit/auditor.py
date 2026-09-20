"""
Enterprise Workflow Auditor.
Generates immutable structured audit trails and timelines for regulatory compliance.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class AuditTimelineEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    execution_id: str = ""
    event_type: str = "workflow.state_changed"
    actor: str = "system"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "execution_id": self.execution_id,
            "event_type": self.event_type,
            "actor": self.actor,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details,
        }


class WorkflowAuditor:
    """Manages append-only execution audit timelines."""

    def __init__(self):
        # Key: execution_id -> List[AuditTimelineEvent]
        self._timelines: Dict[str, List[AuditTimelineEvent]] = {}

    def record_event(
        self,
        execution_id: str,
        event_type: str,
        actor: str = "system",
        details: Optional[Dict[str, Any]] = None,
    ) -> AuditTimelineEvent:
        """Append an audit event to the execution timeline."""
        evt = AuditTimelineEvent(
            execution_id=execution_id,
            event_type=event_type,
            actor=actor,
            details=details or {},
        )
        if execution_id not in self._timelines:
            self._timelines[execution_id] = []
        self._timelines[execution_id].append(evt)
        return evt

    def get_timeline(self, execution_id: str) -> List[AuditTimelineEvent]:
        """Retrieve full audit timeline."""
        return list(self._timelines.get(execution_id, []))
