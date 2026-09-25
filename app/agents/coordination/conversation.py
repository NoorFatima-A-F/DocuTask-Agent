"""
Conversation and Dialogue Thread Models.
Tracks multi-agent conversations, turn-taking, and thread histories.
"""

from datetime import datetime, timezone
from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.coordination.communication import AgentMessage


class ConversationThread(BaseModel):
    """Thread of messages exchanged between two or more agents on a specific topic."""
    conversation_id: UUID = Field(default_factory=uuid4)
    topic: str
    participants: List[UUID] = Field(default_factory=list)
    messages: List[AgentMessage] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def append_message(self, message: AgentMessage) -> "ConversationThread":
        """Returns new immutable thread with appended message."""
        new_participants = list(self.participants)
        if message.sender_id not in new_participants:
            new_participants.append(message.sender_id)
        if message.recipient_id and message.recipient_id not in new_participants:
            new_participants.append(message.recipient_id)

        return self.model_copy(update={
            "participants": new_participants,
            "messages": [*self.messages, message]
        })
