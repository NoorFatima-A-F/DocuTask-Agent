"""
Message Router Subsystem.
"""

from app.agents.messaging.envelopes import MessageEnvelope


class MessageRouter:
    """Router resolving destination topic or queue for a message envelope."""

    def resolve_destination(self, envelope: MessageEnvelope) -> str:
        return f"topic.{envelope.payload_type.lower()}"
