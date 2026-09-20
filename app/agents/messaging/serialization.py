"""
Message Serializer Subsystem.
Serializes MessageEnvelope for JSON, Cloud Pub/Sub, and Cloud Tasks payloads.
"""

from typing import Any, Dict
from app.agents.messaging.envelopes import MessageEnvelope


class MessageSerializer:
    """Serializer converting MessageEnvelope models to JSON string / dictionary payloads."""

    @staticmethod
    def to_dict(envelope: MessageEnvelope) -> Dict[str, Any]:
        return envelope.model_dump(mode="json")

    @staticmethod
    def to_json(envelope: MessageEnvelope) -> str:
        return envelope.model_dump_json()
