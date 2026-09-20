"""
Bulkhead Resource Isolation.
Partitions execution and recovery concurrency pools to prevent cascading exhaustion.
"""

from app.agents.recovery.exceptions import BulkheadExhaustionException


class Bulkhead:
    """Resource partition isolating concurrency for a specific failure domain."""

    def __init__(self, name: str, max_concurrent_calls: int = 10):
        self.name = name
        self.max_concurrent_calls = max_concurrent_calls
        self.active_calls = 0

    def acquire(self) -> None:
        if self.active_calls >= self.max_concurrent_calls:
            raise BulkheadExhaustionException(f"Bulkhead '{self.name}' saturated ({self.active_calls}/{self.max_concurrent_calls}).")
        self.active_calls += 1

    def release(self) -> None:
        self.active_calls = max(0, self.active_calls - 1)


class BulkheadManager:
    """Manages named bulkheads for tools, workers, and recovery operations."""

    def __init__(self):
        self._bulkheads = {}

    def get_or_create(self, name: str, max_concurrent: int = 10) -> Bulkhead:
        if name not in self._bulkheads:
            self._bulkheads[name] = Bulkhead(name, max_concurrent)
        return self._bulkheads[name]
