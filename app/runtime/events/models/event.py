"""
DocuTask Agent - Universal Domain Event Model
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from dataclasses import dataclass, field
import hashlib
import json
import time
import uuid
from typing import Dict, Any, Optional
from app.runtime.events.models.event_types import (
    DomainEventType,
    EventSubsystem,
    EventSeverity,
)
from app.runtime.events.models.event_metadata import EventActor


@dataclass
class DomainEvent:
    """
    Universal Domain Event Model.
    Every runtime operation (planning, execution, validation, recovery, proof)
    emits an immutable instance of DomainEvent.
    """

    event_id: str = field(default_factory=lambda: f"evt-{uuid.uuid4().hex[:12]}")
    mission_id: str = "global-mission"
    parent_event_id: Optional[str] = None
    correlation_id: str = field(default_factory=lambda: f"corr-{uuid.uuid4().hex[:10]}")
    causation_id: str = field(default_factory=lambda: f"cause-{uuid.uuid4().hex[:10]}")
    timestamp_utc: float = field(default_factory=time.time)
    actor: EventActor = field(default_factory=lambda: EventActor(actor_id="system", actor_type="SYSTEM"))
    subsystem: EventSubsystem = EventSubsystem.MISSION_CONTROL
    component: str = "MissionController"
    event_type: DomainEventType = DomainEventType.MISSION_CREATED
    version: str = "13.1.0"
    payload: Dict[str, Any] = field(default_factory=dict)
    evidence_hash: Optional[str] = None
    truth_ledger_hash: Optional[str] = None
    replay_offset: int = 0
    severity: EventSeverity = EventSeverity.INFO

    def __post_init__(self):
        # Auto-compute evidence hash if not provided
        if not self.evidence_hash:
            canonical_payload = json.dumps(self.payload, sort_keys=True, default=str)
            raw_data = f"{self.event_id}:{self.mission_id}:{self.event_type.value}:{self.timestamp_utc}:{canonical_payload}"
            self.evidence_hash = hashlib.sha256(raw_data.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Converts domain event to a clean JSON-serializable dictionary."""
        return {
            "event_id": self.event_id,
            "mission_id": self.mission_id,
            "parent_event_id": self.parent_event_id,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "timestamp_utc": self.timestamp_utc,
            "actor": {
                "actor_id": self.actor.actor_id,
                "actor_type": self.actor.actor_type,
                "role": self.actor.role,
                "session_id": self.actor.session_id,
            },
            "subsystem": self.subsystem.value if isinstance(self.subsystem, EventSubsystem) else str(self.subsystem),
            "component": self.component,
            "event_type": self.event_type.value if isinstance(self.event_type, DomainEventType) else str(self.event_type),
            "version": self.version,
            "payload": self.payload,
            "evidence_hash": self.evidence_hash,
            "truth_ledger_hash": self.truth_ledger_hash,
            "replay_offset": self.replay_offset,
            "severity": self.severity.value if isinstance(self.severity, EventSeverity) else str(self.severity),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DomainEvent":
        actor_data = data.get("actor", {})
        actor = EventActor(
            actor_id=actor_data.get("actor_id", "system"),
            actor_type=actor_data.get("actor_type", "SYSTEM"),
            role=actor_data.get("role"),
            session_id=actor_data.get("session_id"),
        )
        
        event_type_str = data.get("event_type", "MissionCreated")
        try:
            event_type = DomainEventType(event_type_str)
        except ValueError:
            event_type = DomainEventType.MISSION_CREATED

        subsystem_str = data.get("subsystem", "MISSION_CONTROL")
        try:
            subsystem = EventSubsystem(subsystem_str)
        except ValueError:
            subsystem = EventSubsystem.MISSION_CONTROL

        severity_str = data.get("severity", "INFO")
        try:
            severity = EventSeverity(severity_str)
        except ValueError:
            severity = EventSeverity.INFO

        return cls(
            event_id=data.get("event_id", f"evt-{uuid.uuid4().hex[:12]}"),
            mission_id=data.get("mission_id", "global-mission"),
            parent_event_id=data.get("parent_event_id"),
            correlation_id=data.get("correlation_id", f"corr-{uuid.uuid4().hex[:10]}"),
            causation_id=data.get("causation_id", f"cause-{uuid.uuid4().hex[:10]}"),
            timestamp_utc=data.get("timestamp_utc", time.time()),
            actor=actor,
            subsystem=subsystem,
            component=data.get("component", "UnknownComponent"),
            event_type=event_type,
            version=data.get("version", "13.1.0"),
            payload=data.get("payload", {}),
            evidence_hash=data.get("evidence_hash"),
            truth_ledger_hash=data.get("truth_ledger_hash"),
            replay_offset=data.get("replay_offset", 0),
            severity=severity,
        )
