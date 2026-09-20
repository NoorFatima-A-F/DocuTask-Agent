"""
Procedural Memory Sub-Tier.
Stores workflow DAG templates, execution rules, and learned task routines.
"""

from typing import Any, Optional
from app.agents.memory.providers import BaseMemoryProvider, InMemoryProvider
from app.agents.memory.repository import MemoryItem


class ProceduralMemory:
    """Procedural Memory Tier for workflow routines and execution rules."""

    def __init__(self, provider: Optional[BaseMemoryProvider] = None):
        self.provider = provider or InMemoryProvider(name="ProceduralMemoryProvider")

    async def store_procedure(self, name: str, procedure_definition: Any) -> None:
        item = MemoryItem(key=f"procedure:{name}", value=procedure_definition)
        await self.provider.put(item)
