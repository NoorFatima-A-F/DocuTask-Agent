"""Cascading Timeout and Deadline Budget Manager."""

from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass
class DeadlineContext:
    total_timeout_ms: float
    started_at: float
    deadline: float

    @property
    def remaining_ms(self) -> float:
        now = time.time()
        left = (self.deadline - now) * 1000.0
        return max(0.0, left)

    @property
    def is_expired(self) -> bool:
        return time.time() >= self.deadline


class TimeoutManager:
    """Manages distributed request deadline propagation across multiple hops."""

    @staticmethod
    def create_deadline(timeout_ms: float) -> DeadlineContext:
        now = time.time()
        deadline = now + (timeout_ms / 1000.0)
        return DeadlineContext(
            total_timeout_ms=timeout_ms,
            started_at=now,
            deadline=deadline,
        )

    @staticmethod
    def sub_deadline(parent: DeadlineContext, requested_timeout_ms: float) -> DeadlineContext:
        """Create a child deadline bounded by the parent remaining budget."""
        remaining = parent.remaining_ms
        effective_timeout = min(remaining, requested_timeout_ms)
        return TimeoutManager.create_deadline(effective_timeout)
