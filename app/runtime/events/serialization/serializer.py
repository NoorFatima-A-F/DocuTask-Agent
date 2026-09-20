"""
DocuTask Agent - Event Serializer & Canonical Encoders
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

import json
from typing import Dict, Any, Union
from app.runtime.events.models.event import DomainEvent


class EventSerializer:
    """
    Canonical Event Serializer.
    Converts domain events to/from JSON strings and dictionaries with deterministic key ordering.
    """

    @staticmethod
    def serialize_json(event: DomainEvent) -> str:
        """Serializes event to canonical JSON string."""
        return json.dumps(event.to_dict(), sort_keys=True, default=str)

    @staticmethod
    def deserialize_json(json_str: str) -> DomainEvent:
        """Deserializes canonical JSON string into DomainEvent."""
        data = json.loads(json_str)
        return DomainEvent.from_dict(data)

    @staticmethod
    def to_dict(event: DomainEvent) -> Dict[str, Any]:
        return event.to_dict()

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> DomainEvent:
        return DomainEvent.from_dict(data)
