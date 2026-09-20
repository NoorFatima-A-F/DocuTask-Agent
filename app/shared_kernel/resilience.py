"""
Resilience Policies, Exponential Backoff, Circuit Breaker and Rate Limiter Contracts.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Type, Optional, Callable, Any
import math
import time

class RetryStrategy(str, Enum):
    IMMEDIATE = "IMMEDIATE"
    LINEAR = "LINEAR"
    EXPONENTIAL_BACKOFF = "EXPONENTIAL_BACKOFF"

@dataclass(frozen=True)
class RetryPolicy:
    max_retries: int = 3
    initial_delay_seconds: float = 0.1
    max_delay_seconds: float = 5.0
    backoff_multiplier: float = 2.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    retryable_exceptions: List[Type[Exception]] = field(default_factory=list)

    def compute_delay(self, attempt: int) -> float:
        if self.strategy == RetryStrategy.IMMEDIATE:
            return 0.0
        if self.strategy == RetryStrategy.LINEAR:
            return min(self.max_delay_seconds, self.initial_delay_seconds * attempt)
        # EXPONENTIAL_BACKOFF
        delay = self.initial_delay_seconds * math.pow(self.backoff_multiplier, attempt - 1)
        return min(self.max_delay_seconds, delay)

class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class CircuitBreakerContract(ABC):
    @abstractmethod
    def get_state(self) -> CircuitState:
        pass

    @abstractmethod
    def record_success(self) -> None:
        pass

    @abstractmethod
    def record_failure(self) -> None:
        pass

    @abstractmethod
    def allow_execution(self) -> bool:
        pass

class BulkheadContract(ABC):
    @abstractmethod
    def acquire(self) -> bool:
        pass

    @abstractmethod
    def release(self) -> None:
        pass

class RateLimiterContract(ABC):
    @abstractmethod
    def allow_request(self, key: str) -> bool:
        pass
