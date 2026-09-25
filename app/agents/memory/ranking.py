"""
Memory Ranker Subsystem.
Ranks retrieved memory items based on recency, importance, confidence, and relevance.
"""

from typing import List
from app.agents.memory.repository import MemoryItem


class MemoryRanker:
    """Ranker scoring candidate memory items."""

    @staticmethod
    def rank_items(items: List[MemoryItem], recency_weight: float = 0.5, importance_weight: float = 0.5) -> List[MemoryItem]:
        """Ranks memory items by importance and recency."""
        sorted_items = list(items)
        sorted_items.sort(
            key=lambda m: (m.statistics.importance_score * importance_weight) + (m.statistics.confidence_score * recency_weight),
            reverse=True
        )
        return sorted_items
