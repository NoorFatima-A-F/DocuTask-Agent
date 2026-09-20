"""
Context Window Assembly & Token Budgeting Subsystem.
Provides TokenBudget, ContextWindow, and ContextAssembler to prepare token-bounded context windows for Planners.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.agents.memory.exceptions import ContextWindowExceededException
from app.agents.memory.repository import MemoryItem


class TokenBudget(BaseModel):
    """Token budget configuration."""

    max_tokens: int = Field(default=4000, ge=100)
    allocated_tokens: int = Field(default=0, ge=0)
    model_config = {"frozen": True}

    @property
    def remaining_tokens(self) -> int:
        return max(0, self.max_tokens - self.allocated_tokens)


class ContextWindow(BaseModel):
    """Assembled token-bounded context window for LLM prompt context."""

    items: List[MemoryItem] = Field(default_factory=list)
    total_tokens: int = Field(default=0, ge=0)
    token_limit: int = Field(default=4000, ge=100)
    model_config = {"frozen": True}


class ContextAssembler:
    """Assembler preparing token-budgeted context windows from memory records."""

    def __init__(self, max_tokens: int = 4000):
        self.max_tokens = max_tokens

    def assemble(self, items: List[MemoryItem]) -> ContextWindow:
        """Assembles context window within token budget constraints, prioritising high-importance items."""
        sorted_items = list(items)
        sorted_items.sort(key=lambda x: x.statistics.importance_score, reverse=True)

        selected: List[MemoryItem] = []
        accumulated_tokens = 0

        for item in sorted_items:
            # Estimate token count (~4 characters per token)
            text = str(item.value)
            est_tokens = max(1, len(text) // 4)

            if accumulated_tokens + est_tokens <= self.max_tokens:
                selected.append(item)
                accumulated_tokens += est_tokens
            else:
                break

        return ContextWindow(
            items=selected,
            total_tokens=accumulated_tokens,
            token_limit=self.max_tokens
        )
