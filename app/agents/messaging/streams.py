"""
Message Stream Subsystem.
"""

from typing import List
from app.agents.messaging.envelopes import MessageEnvelope


class MessageStream:
    """Stream of ordered message envelopes for event streaming."""

    def __init__(self):
        self._stream: List[MessageEnvelope] = []

    def append(self, envelope: MessageEnvelope) -> None:
        self._stream.append(envelope)

    def read_all(self) -> List[MessageEnvelope]:
        return list(self._stream)
