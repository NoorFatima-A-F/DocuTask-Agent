"""
Semantic Memory Sub-Tier.
Stores domain concepts, facts, and vector embeddings for semantic retrieval.
"""

from typing import Any, Optional
from app.agents.memory.providers import BaseMemoryProvider, VectorProvider
from app.agents.memory.repository import MemoryItem


class SemanticMemory:
    """Semantic Memory Tier for domain concepts and vector search."""

    def __init__(self, provider: Optional[BaseMemoryProvider] = None):
        self.provider = provider or VectorProvider()

    async def store_concept(self, concept_key: str, concept_value: Any) -> None:
        item = MemoryItem(key=f"concept:{concept_key}", value=concept_value)
        await self.provider.put(item)
