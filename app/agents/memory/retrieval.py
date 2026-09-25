"""
Memory Retrieval Layer.
Defines MemoryQuery, RetrievalResult, and MemoryRetriever supporting keyword, semantic, and hybrid search.
"""

from typing import List
from pydantic import BaseModel, Field
from app.agents.memory.interfaces import IMemoryRetriever
from app.agents.memory.providers import BaseMemoryProvider
from app.agents.memory.repository import MemoryItem


class MemoryQuery(BaseModel):
    """Query model for retrieving memory items."""

    query_text: str
    min_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    min_importance: float = Field(default=0.0, ge=0.0, le=1.0)
    top_k: int = Field(default=5, ge=1)
    tags: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}


class RetrievalResult(BaseModel):
    """Ranked memory retrieval result."""

    items: List[MemoryItem] = Field(default_factory=list)
    total_count: int = Field(default=0, ge=0)
    model_config = {"frozen": True}


class MemoryRetriever(IMemoryRetriever):
    """Retriever searching memory records across provider tiers."""

    def __init__(self, provider: BaseMemoryProvider):
        self.provider = provider

    async def search(self, query: str, top_k: int = 5) -> List[MemoryItem]:
        """Executes keyword text search across stored memory items."""
        all_items = await self.provider.list_all()
        query_lower = query.lower()
        matched: List[MemoryItem] = []

        for item in all_items:
            if item.is_expired():
                continue
            item_str = str(item.value).lower()
            if query_lower in item_str or query_lower in item.key.lower():
                matched.append(item)

        matched.sort(key=lambda m: m.statistics.importance_score, reverse=True)
        return matched[:top_k]
