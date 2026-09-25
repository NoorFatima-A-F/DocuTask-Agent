"""
Enterprise Retry Policies & Circuit Breakers.
"""
import time
import random
from typing import Callable, TypeVar, Optional

T = TypeVar("T")

class RetryPolicy:
    def __init__(self, max_retries: int = 3, initial_delay_sec: float = 0.1, backoff_multiplier: float = 2.0):
        self.max_retries = max_retries
        self.initial_delay_sec = initial_delay_sec
        self.backoff_multiplier = backoff_multiplier

    def execute(self, fn: Callable[[], T]) -> T:
        delay = self.initial_delay_sec
        last_exception: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                return fn()
            except Exception as e:
                last_exception = e
                if attempt == self.max_retries:
                    break
                jitter = random.uniform(0.8, 1.2)
                time.sleep(delay * jitter)
                delay *= self.backoff_multiplier

        if last_exception:
            raise last_exception
        raise RuntimeError("Retry policy failed with unknown state")


ExponentialBackoffPolicy = RetryPolicy


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout_sec: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_sec = recovery_timeout_sec
        self._failure_count = 0
        self._last_failure_time: float = 0
        self._state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    @property
    def state(self) -> str:
        if self._state == "OPEN":
            if time.time() - self._last_failure_time > self.recovery_timeout_sec:
                self._state = "HALF_OPEN"
        return self._state

    def call(self, fn: Callable[[], T]) -> T:
        if self.state == "OPEN":
            raise RuntimeError("Circuit breaker is OPEN. Fast-failing downstream request.")

        try:
            res = fn()
            if self._state == "HALF_OPEN":
                self._state = "CLOSED"
                self._failure_count = 0
            return res
        except Exception as e:
            self._failure_count += 1
            self._last_failure_time = time.time()
            if self._failure_count >= self.failure_threshold:
                self._state = "OPEN"
            raise e
