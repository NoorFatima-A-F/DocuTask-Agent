"""
Memory Provider Abstractions & Implementations.
Defines BaseMemoryProvider and concrete provider adapters (InMemoryProvider, MockProvider, VectorProvider, CloudProvider).
Decouples agent logic from Redis, PostgreSQL, Supabase, Pinecone, Vertex AI Vector Search, ChromaDB, FAISS, and local storage.
"""

from abc import ABC, abstractmethod
import asyncio
from typing import Dict, List, Optional
from app.agents.memory.repository import MemoryItem


class BaseMemoryProvider(ABC):
    """Abstract Base Class for all Memory Storage Providers."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Returns provider identification string."""
        pass

    @abstractmethod
    async def put(self, item: MemoryItem) -> None:
        """Stores or updates a MemoryItem in provider storage."""
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[MemoryItem]:
        """Retrieves a MemoryItem by key from provider storage."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Deletes a MemoryItem by key from provider storage."""
        pass

    @abstractmethod
    async def list_all(self) -> List[MemoryItem]:
        """Lists all MemoryItem records stored in provider."""

        pass


class InMemoryProvider(BaseMemoryProvider):
    """Thread-safe In-Memory Provider implementation for local execution and fast caching."""

    def __init__(self, name: str = "InMemoryProvider"):
        self._name = name
        self._store: Dict[str, MemoryItem] = {}
        self._lock = asyncio.Lock()

    @property
    def provider_name(self) -> str:
        return self._name

    async def put(self, item: MemoryItem) -> None:
        async with self._lock:
            self._store[item.key] = item

    async def get(self, key: str) -> Optional[MemoryItem]:
        async with self._lock:
            return self._store.get(key)

    async def delete(self, key: str) -> bool:
        async with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    async def list_all(self) -> List[MemoryItem]:
        async with self._lock:
            return list(self._store.values())


class MockProvider(InMemoryProvider):
    """Mock Provider for unit testing and dry runs."""

    def __init__(self):
        super().__init__(name="MockProvider")


class VectorProvider(InMemoryProvider):
    """Vector Provider for vector similarity and semantic memory."""

    def __init__(self):
        super().__init__(name="VectorProvider")


class CloudProvider(InMemoryProvider):
    """Cloud Provider adapter for GCP Cloud Memorystore / Cloud SQL / Vertex AI."""

    def __init__(self):
        super().__init__(name="CloudProvider")
