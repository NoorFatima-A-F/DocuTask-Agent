"""
Conversation Memory Sub-Tier.
Stores user dialogue turns and interaction context.
"""

from typing import Optional
from app.agents.memory.providers import BaseMemoryProvider, InMemoryProvider

from app.agents.memory.repository import MemoryItem


class ConversationMemory:
    """Conversation Memory Tier for dialogue history."""

    def __init__(self, provider: Optional[BaseMemoryProvider] = None):
        self.provider = provider or InMemoryProvider(name="ConversationMemoryProvider")

    async def add_message(self, role: str, content: str) -> None:
        item = MemoryItem(key=f"msg:{role}", value={"role": role, "content": content})
        await self.provider.put(item)
