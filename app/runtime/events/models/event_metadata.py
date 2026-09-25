"""
DocuTask Agent - Event Metadata Models
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from app.runtime.events.models.event_types import EventSubsystem, EventSeverity


@dataclass
class EventActor:
    actor_id: str
    actor_type: str  # "PLANNER", "WORKER", "HUMAN", "SYSTEM", "CHAOS_ORCHESTRATOR"
    role: Optional[str] = None
    session_id: Optional[str] = None


@dataclass
class EventMetadata:
    actor: EventActor
    subsystem: EventSubsystem
    component: str
    version: str = "13.1.0"
    severity: EventSeverity = EventSeverity.INFO
    schema_version: int = 1
    environment: str = "production"
    custom_attributes: Dict[str, Any] = field(default_factory=dict)
