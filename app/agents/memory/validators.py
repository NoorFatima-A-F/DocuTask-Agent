"""
Memory Validator Guards.
Provides fail-fast validation for MemoryItem models and key constraints.
"""

from app.agents.memory.exceptions import MemoryValidationException
from app.agents.memory.repository import MemoryItem


class MemoryValidator:
    """Fail-fast validator for memory models."""

    @staticmethod
    def validate_item(item: MemoryItem) -> None:
        """Validates MemoryItem fields."""
        if not item.key or not item.key.strip():
            raise MemoryValidationException("Memory key cannot be empty.")
