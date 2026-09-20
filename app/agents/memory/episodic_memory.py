"""
Episodic Memory Sub-Tier.
Stores chronological execution events, past tool calls, and agent experience history.
"""

from typing import Any, List, Optional
from app.agents.memory.providers import BaseMemoryProvider, InMemoryProvider
from app.agents.memory.repository import MemoryItem


class EpisodicMemory:
    """Episodic Memory Tier for event trajectories and historical experience."""

    def __init__(self, provider: Optional[BaseMemoryProvider] = None):
        self.provider = provider or InMemoryProvider(name="EpisodicMemoryProvider")

    async def record_episode(self, episode_id: str, episode_data: Any) -> None:
        item = MemoryItem(key=f"episode:{episode_id}", value=episode_data)
        await self.provider.put(item)
