"""
Bulkhead Resource Isolation.
Implements bulkhead isolation patterns preventing noisy neighbors from starving shared platform resources.
"""

import asyncio
from typing import Any, Callable, Coroutine, Optional
from app.agents.runtime.exceptions import RuntimeKernelException


class BulkheadCapacityExceededError(RuntimeKernelException):
    """Raised when a bulkhead compartment's concurrency limit is reached."""
    pass


class Bulkhead:
    """Isolated concurrency compartment with bounded active slots and queue limits."""

    def __init__(self, name: str, max_concurrent: int = 10, max_queue: int = 20) -> None:
        self.name = name
        self.max_concurrent = max_concurrent
        self.max_queue = max_queue
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._active_count = 0
        self._waiting_count = 0

    @property
    def active_count(self) -> int:
        return self._active_count

    async def execute(self, coroutine_fn: Callable[[], Coroutine[Any, Any, Any]]) -> Any:
        """Executes operation within the isolated bulkhead slot."""
        if self._waiting_count >= self.max_queue:
            raise BulkheadCapacityExceededError(
                f"Bulkhead '{self.name}' queue is full ({self._waiting_count}/{self.max_queue})."
            )

        self._waiting_count += 1
        try:
            async with self._semaphore:
                self._waiting_count -= 1
                self._active_count += 1
                try:
                    return await coroutine_fn()
                finally:
                    self._active_count -= 1
        except Exception:
            if self._waiting_count > 0:
                self._waiting_count -= 1
            raise
