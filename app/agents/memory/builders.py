"""
Fluent Builder Suite for Memory Aggregates.
Provides MemoryBuilder, KnowledgeBuilder, QueryBuilder, and SnapshotBuilder.
"""

from typing import Any, Dict, List, Optional
from app.agents.memory.knowledge import KnowledgeItem, KnowledgeSource
from app.agents.memory.metadata import MemoryMetadata
from app.agents.memory.repository import MemoryItem
from app.agents.memory.retrieval import MemoryQuery
from app.agents.memory.snapshots import MemorySnapshot
from app.agents.memory.validators import MemoryValidator


class MemoryBuilder:
    """Fluent builder for MemoryItem aggregate models."""

    def __init__(self, key: str, value: Any):
        self._key = key
        self._value = value
        self._importance = 0.5
        self._tags: List[str] = []

    def with_importance(self, importance: float) -> "MemoryBuilder":
        self._importance = importance
        return self

    def with_tags(self, tags: List[str]) -> "MemoryBuilder":
        self._tags = list(tags)
        return self

    def build(self) -> MemoryItem:
        meta = MemoryMetadata(tags=self._tags)
        item = MemoryItem(key=self._key, value=self._value, metadata=meta)
        item.statistics.importance_score = self._importance
        MemoryValidator.validate_item(item)
        return item


class KnowledgeBuilder:
    """Fluent builder for KnowledgeItem models."""

    def __init__(self, topic: str):
        self._topic = topic
        self._category = "FACT"
        self._content: Dict[str, Any] = {}

    def with_category(self, category: str) -> "KnowledgeBuilder":
        self._category = category
        return self

    def with_content(self, content: Dict[str, Any]) -> "KnowledgeBuilder":
        self._content = dict(content)
        return self

    def build(self) -> KnowledgeItem:
        return KnowledgeItem(
            topic=self._topic,
            category=self._category,
            content=self._content
        )


class QueryBuilder:
    """Fluent builder for MemoryQuery models."""

    def __init__(self, query_text: str):
        self._query_text = query_text
        self._top_k = 5

    def with_top_k(self, top_k: int) -> "QueryBuilder":
        self._top_k = top_k
        return self

    def build(self) -> MemoryQuery:
        return MemoryQuery(query_text=self._query_text, top_k=self._top_k)


class SnapshotBuilder:
    """Fluent builder for MemorySnapshot models."""

    def __init__(self, snapshot_id: str):
        self._snapshot_id = snapshot_id
        self._payload: Dict[str, Any] = {}

    def with_payload(self, payload: Dict[str, Any]) -> "SnapshotBuilder":
        self._payload = dict(payload)
        return self

    def build(self) -> MemorySnapshot:
        return MemorySnapshot(snapshot_id=self._snapshot_id, state_payload=self._payload)
