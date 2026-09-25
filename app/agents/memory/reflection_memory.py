"""
Reflection Memory Sub-Tier.
Stores self-reflection feedback, quality metrics, and replanning triggers.
"""

from typing import Any, Optional
from app.agents.memory.providers import BaseMemoryProvider, InMemoryProvider
from app.agents.memory.repository import MemoryItem


class ReflectionMemory:
    """Reflection Memory Tier for self-correction feedback."""

    def __init__(self, provider: Optional[BaseMemoryProvider] = None):
        self.provider = provider or InMemoryProvider(name="ReflectionMemoryProvider")

    async def record_reflection(self, reflection_id: str, feedback: Any) -> None:
        item = MemoryItem(key=f"refl:{reflection_id}", value=feedback)
        await self.provider.put(item)
