"""
Memory Subsystem Core Interfaces.
Defines contracts for IMemoryManager, IMemoryRetriever, IMemoryIndexer, and IMemoryRanker.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.agents.memory.repository import MemoryItem


class IMemoryManager(ABC):
    """Abstract interface for Memory Manager."""

    @abstractmethod
    async def store(self, key: str, value: Any, importance: float = 0.5) -> MemoryItem:
        """Stores a memory item in active memory tier."""
        pass

    @abstractmethod
    async def retrieve(self, key: str) -> Optional[MemoryItem]:
        """Retrieves a memory item by key."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Deletes a memory item by key."""
        pass


class IMemoryRetriever(ABC):
    """Abstract interface for Memory Retriever."""

    @abstractmethod
    async def search(self, query: str, top_k: int = 5) -> List[MemoryItem]:
        """Searches memory items by keyword or vector similarity."""
        pass
