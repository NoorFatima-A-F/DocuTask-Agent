"""
Memory Manager Subsystem Orchestrator.
Orchestrates memory operations across working, short-term, long-term, semantic, procedural, episodic, and conversation memory tiers.
Never depends on concrete storage providers.
"""

from typing import Any, List, Optional
from app.agents.memory.context import ContextAssembler, ContextWindow
from app.agents.memory.interfaces import IMemoryManager
from app.agents.memory.providers import BaseMemoryProvider, InMemoryProvider
from app.agents.memory.repository import MemoryItem
from app.agents.memory.retrieval import MemoryRetriever


class MemoryManager(IMemoryManager):
    """
    Enterprise Memory Manager.
    Unified orchestrator managing memory item lifecycle, retrieval, promotion, snapshotting, and context window assembly.
    """

    def __init__(self, provider: Optional[BaseMemoryProvider] = None):
        self.provider = provider or InMemoryProvider(name="MemoryManagerProvider")
        self.retriever = MemoryRetriever(provider=self.provider)
        self.assembler = ContextAssembler()

    async def store(self, key: str, value: Any, importance: float = 0.5) -> MemoryItem:
        """Stores a memory item in active provider storage."""
        item = MemoryItem(key=key, value=value)
        item.statistics.importance_score = importance
        await self.provider.put(item)
        return item

    async def retrieve(self, key: str) -> Optional[MemoryItem]:
        """Retrieves a memory item by key."""
        item = await self.provider.get(key)
        if item and not item.is_expired():
            return item
        return None

    async def delete(self, key: str) -> bool:
        """Deletes a memory item by key."""
        return await self.provider.delete(key)

    async def search(self, query: str, top_k: int = 5) -> List[MemoryItem]:
        """Searches memory items using retriever."""
        return await self.retriever.search(query=query, top_k=top_k)

    async def assemble_context(self, max_tokens: int = 4000) -> ContextWindow:
        """Assembles token-bounded context window for LLM prompts."""
        all_items = await self.provider.list_all()
        assembler = ContextAssembler(max_tokens=max_tokens)
        return assembler.assemble(all_items)
