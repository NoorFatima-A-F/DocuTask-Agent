"""
AMAEOP Pillar 6 - Cross-Agent Communication Bus Package
"""

from app.runtime.communication.communication_bus import CommunicationBus, EnterpriseMessage, communication_bus
from app.runtime.communication.message_router import MessageRouter, message_router
from app.runtime.communication.channel_manager import ChannelManager, CommunicationChannel, channel_manager
from app.runtime.communication.conversation_history import ConversationHistory

__all__ = [
    "CommunicationBus",
    "EnterpriseMessage",
    "communication_bus",
    "MessageRouter",
    "message_router",
    "ChannelManager",
    "CommunicationChannel",
    "channel_manager",
    "ConversationHistory",
]
