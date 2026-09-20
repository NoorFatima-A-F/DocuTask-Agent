"""
Base Event Architecture Primitives.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import uuid

@dataclass(frozen=True)
class EventMetadata:
    event_id: str = field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:12]}")
    correlation_id: str = field(default_factory=lambda: f"corr_{uuid.uuid4().hex[:12]}")
    causation_id: Optional[str] = None
    tenant_id: str = "default-tenant"
    version: str = "1.0.0"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_subsystem: str = "VERIFICATION_PLATFORM"


@dataclass(frozen=True)
class BaseEvent:
    metadata: EventMetadata = field(default_factory=EventMetadata)
    event_name: str = "BaseEvent"
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DomainEvent(BaseEvent):
    aggregate_id: str = ""
    aggregate_type: str = ""


@dataclass(frozen=True)
class IntegrationEvent(BaseEvent):
    target_subsystem: str = "PLATFORM_BUS"
