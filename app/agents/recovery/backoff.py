"""
Backoff Calculator.
Calculates linear, exponential, and jittered delays for recovery retries.
"""

import random


class BackoffCalculator:
    """Calculates backoff delays for recovery retry policies."""

    @staticmethod
    def calculate_exponential_backoff(
        attempt: int,
        initial_seconds: float = 1.0,
        factor: float = 2.0,
        max_seconds: float = 30.0,
        jitter: bool = True
    ) -> float:
        delay = min(initial_seconds * (factor ** attempt), max_seconds)
        if jitter:
            delay += random.uniform(0.0, 0.5)
        return delay
