"""
Execution Rate Limiter.
Enforces dispatching rate limits across distributed nodes.
"""

import asyncio
from datetime import datetime, timezone


class ExecutionRateLimiter:
    """Token-bucket or leaky-bucket rate limiter for task dispatching."""

    def __init__(self, max_requests_per_second: float = 10.0):
        self.rate = max_requests_per_second
        self.interval = 1.0 / max_requests_per_second if max_requests_per_second > 0 else 0.1
        self._last_dispatch = datetime.now(timezone.utc).timestamp()

    async def acquire(self) -> None:
        now = datetime.now(timezone.utc).timestamp()
        elapsed = now - self._last_dispatch
        if elapsed < self.interval:
            await asyncio.sleep(self.interval - elapsed)
        self._last_dispatch = datetime.now(timezone.utc).timestamp()
