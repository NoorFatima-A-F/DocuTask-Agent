"""
Runtime Resource Manager.
Tracks memory, compute slots, and token budgets across concurrent tasks.
"""

from typing import Dict
from pydantic import BaseModel, Field
from app.agents.execution.token_budget import TokenBudgetManager


class ResourceManager:
    """Manages memory, CPU, and token limits during execution."""

    def __init__(self, max_memory_mb: float = 2048.0, max_tokens: int = 50000):
        self.max_memory_mb = max_memory_mb
        self.current_memory_mb = 0.0
        self.token_manager = TokenBudgetManager(max_tokens=max_tokens)

    def allocate_memory(self, amount_mb: float) -> bool:
        if self.current_memory_mb + amount_mb <= self.max_memory_mb:
            self.current_memory_mb += amount_mb
            return True
        return False

    def release_memory(self, amount_mb: float) -> None:
        self.current_memory_mb = max(0.0, self.current_memory_mb - amount_mb)
