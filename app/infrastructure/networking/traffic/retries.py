"""Traffic Resilience, Retries, Exponential Backoff, and Retry Budgets."""

from dataclasses import dataclass
import random
import time
from typing import Callable, List, Optional, Set, TypeVar

T = TypeVar("T")


@dataclass
class RetryPolicy:
    """Configurable retry policy."""
    max_attempts: int = 3
    base_delay_ms: float = 100.0
    max_delay_ms: float = 2000.0
    backoff_multiplier: float = 2.0
    jitter: bool = True
    retryable_status_codes: Set[int] = None

    def __post_init__(self) -> None:
        if self.retryable_status_codes is None:
            self.retryable_status_codes = {408, 429, 500, 502, 503, 504}


class RetryEngine:
    """Executes callables with exponential backoff and retry budgets."""

    def __init__(self, default_policy: Optional[RetryPolicy] = None) -> None:
        self.policy = default_policy or RetryPolicy()
        self._retry_tokens = 100
        self._max_retry_tokens = 100

    def compute_backoff(self, attempt: int, policy: Optional[RetryPolicy] = None) -> float:
        """Compute delay in seconds for the given attempt."""
        pol = policy or self.policy
        delay_ms = pol.base_delay_ms * (pol.backoff_multiplier ** (attempt - 1))
        delay_ms = min(delay_ms, pol.max_delay_ms)

        if pol.jitter:
            delay_ms = delay_ms * (0.5 + random.random() * 0.5)

        return delay_ms / 1000.0

    def should_retry(self, attempt: int, status_code: Optional[int] = None, policy: Optional[RetryPolicy] = None) -> bool:
        """Evaluate if another retry attempt is permitted."""
        pol = policy or self.policy
        if attempt >= pol.max_attempts:
            return False

        if status_code is not None and status_code not in pol.retryable_status_codes:
            return False

        # Consume retry token from budget
        if self._retry_tokens > 0:
            self._retry_tokens -= 1
            return True
        return False

    def replenish_budget(self, count: int = 1) -> None:
        """Replenish retry tokens on successful calls."""
        self._retry_tokens = min(self._max_retry_tokens, self._retry_tokens + count)
