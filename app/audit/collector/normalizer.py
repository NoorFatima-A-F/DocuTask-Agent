"""Audit Event Normalizer."""

from typing import Dict, Any, Union
from datetime import datetime, timezone
import uuid
from ..core.events import AuditEvent, EventCategory, ActorType, AuditSeverity, OutcomeType


class EventNormalizer:
    """Normalizes heterogeneous input dictionaries, logger objects, and raw payloads into canonical AuditEvent."""

    @staticmethod
    def normalize(data: Union[AuditEvent, Dict[str, Any]]) -> AuditEvent:
        if isinstance(data, AuditEvent):
            return data

        d = dict(data)
        
        # Ensure mandatory event_id and timestamp
        if "event_id" not in d:
            d["event_id"] = f"aud_evt_{uuid.uuid4().hex[:12]}"
        if "timestamp" not in d or not d["timestamp"]:
            d["timestamp"] = datetime.now(timezone.utc)

        # Ensure enums
        if "category" in d and isinstance(d["category"], str):
            try:
                d["category"] = EventCategory(d["category"].upper())
            except ValueError:
                d["category"] = EventCategory.SYSTEM

        if "actor_type" in d and isinstance(d["actor_type"], str):
            try:
                d["actor_type"] = ActorType(d["actor_type"].upper())
            except ValueError:
                d["actor_type"] = ActorType.USER

        if "severity" in d and isinstance(d["severity"], str):
            try:
                d["severity"] = AuditSeverity(d["severity"].upper())
            except ValueError:
                d["severity"] = AuditSeverity.INFO

        if "outcome" in d and isinstance(d["outcome"], str):
            try:
                d["outcome"] = OutcomeType(d["outcome"].upper())
            except ValueError:
                d["outcome"] = OutcomeType.SUCCESS

        return AuditEvent(**d)
