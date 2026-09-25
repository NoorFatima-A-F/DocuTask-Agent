"""
Memory Serializer Subsystem.
Serializes memory records for JSON, Pub/Sub, and Cloud Tasks payloads.
"""

from typing import Any, Dict
from app.agents.memory.repository import MemoryItem


class MemorySerializer:
    """Serializer converting MemoryItem models to JSON string / dictionary payloads."""

    @staticmethod
    def to_dict(item: MemoryItem) -> Dict[str, Any]:
        """Serializes MemoryItem to dictionary."""
        return item.model_dump(mode="json")

    @staticmethod
    def to_json(item: MemoryItem) -> str:
        """Serializes MemoryItem to JSON string."""
        return item.model_dump_json()
