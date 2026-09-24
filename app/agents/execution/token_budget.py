"""
Token Budget Management.
Tracks and limits LLM token consumption across all nodes during execution.
"""

from pydantic import BaseModel, Field


class TokenBudget(BaseModel):
    """Budget constraints for tokens."""
    max_tokens: int = Field(default=50000, ge=0)
    consumed_tokens: int = Field(default=0, ge=0)


class TokenBudgetManager:
    """Manages runtime token consumption preventing budget overruns."""

    def __init__(self, max_tokens: int = 50000):
        self._budget = TokenBudget(max_tokens=max_tokens)

    def can_consume(self, estimated_tokens: int) -> bool:
        return (self._budget.consumed_tokens + estimated_tokens) <= self._budget.max_tokens

    def record_consumption(self, tokens: int) -> None:
        self._budget.consumed_tokens += tokens

    @property
    def remaining_tokens(self) -> int:
        return max(0, self._budget.max_tokens - self._budget.consumed_tokens)

    @property
    def consumed_tokens(self) -> int:
        return self._budget.consumed_tokens
