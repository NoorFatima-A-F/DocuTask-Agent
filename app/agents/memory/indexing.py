"""
Memory Indexer Subsystem.
Indexes memory items by tags, session IDs, and execution IDs.
"""

from typing import Dict, Set
from app.agents.memory.repository import MemoryItem


class MemoryIndexer:
    """Indexer maintaining secondary lookup indexes for memory items."""

    def __init__(self):
        self._tag_index: Dict[str, Set[str]] = {}

    def index_item(self, item: MemoryItem) -> None:
        """Indexes item by tags."""
        for tag in item.metadata.tags:
            tag_upper = tag.upper()
            if tag_upper not in self._tag_index:
                self._tag_index[tag_upper] = set()
            self._tag_index[tag_upper].add(item.key)
