"""
Agent Memory Interface.
Defines contract for short-term, long-term, and episodic agent memory storage.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from app.agents.context import AgentContext


class AgentMemory(ABC):
    """Abstract interface for agent memory management engine."""

    @abstractmethod
    async def store(self, key: str, value: Any, context: AgentContext) -> None:
        """Stores a memory record within context scope."""
        pass

    @abstractmethod
    async def retrieve(self, key: str, context: AgentContext) -> Any:
        """Retrieves a memory record within context scope."""
        pass

    @abstractmethod
    async def search_similar(self, query: str, context: AgentContext, top_k: int = 5) -> List[Dict[str, Any]]:
        """Searches episodic memory via semantic vector similarity."""
        pass
