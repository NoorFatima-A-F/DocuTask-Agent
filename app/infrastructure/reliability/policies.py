"""
Reliability Policy Engine & Fault-Tolerance Primitives.

Implements Circuit Breakers, 5 Retry Strategies (Immediate, Linear, Exponential,
Randomized Jitter, Adaptive), Bulkhead concurrency isolation, Timeouts, and Fallbacks.
"""

from __future__ import annotations

import asyncio
import logging
import random
import time
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

from app.infrastructure.reliability.models import (
    BulkheadConfig,
    CircuitBreakerConfig,
    CircuitBreakerState,
    ReliabilityPolicy,
    RetryPolicyConfig,
    RetryStrategy,
)

logger = logging.getLogger("infrastructure.reliability.policies")

T = TypeVar("T")


class CircuitBreakerOpenError(Exception):
    """Raised when an operation is attempted while circuit breaker is OPEN."""
    pass


class BulkheadFullError(Exception):
    """Raised when bulkhead concurrent capacity and wait queue are saturated."""
    pass


class ReliabilityTimeoutError(Exception):
    """Raised when an operation exceeds its configured timeout budget."""
    pass


class CircuitBreaker:
    """
    3-State Circuit Breaker: CLOSED -> OPEN -> HALF_OPEN -> CLOSED (or back to OPEN).
    """

    def __init__(self, name: str, config: Optional[CircuitBreakerConfig] = None) -> None:
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self._state = CircuitBreakerState.CLOSED
        self._consecutive_failures = 0
        self._consecutive_successes = 0
        self._total_calls = 0
        self._failed_calls = 0
        self._last_state_change = time.time()
        self._last_failure_time: Optional[float] = None
        self._half_open_active_requests = 0

    @property
    def state(self) -> CircuitBreakerState:
        self._check_cooldown()
        return self._state

    @property
    def consecutive_failures(self) -> int:
        return self._consecutive_failures

    def _check_cooldown(self) -> None:
        if self._state == CircuitBreakerState.OPEN:
            elapsed = time.time() - self._last_state_change
            if elapsed >= self.config.recovery_timeout_seconds:
                self._transition_to(CircuitBreakerState.HALF_OPEN)

    def _transition_to(self, new_state: CircuitBreakerState) -> None:
        old_state = self._state
        self._state = new_state
        self._last_state_change = time.time()
        if new_state == CircuitBreakerState.HALF_OPEN:
            self._half_open_active_requests = 0
            self._consecutive_successes = 0
        elif new_state == CircuitBreakerState.CLOSED:
            self._consecutive_failures = 0
            self._consecutive_successes = 0
        logger.info(f"CircuitBreaker '{self.name}' transitioned from {old_state.value} to {new_state.value}")

    def before_call(self) -> None:
        """Verify circuit allows execution before running operation."""
        self._check_cooldown()
        if self._state == CircuitBreakerState.OPEN:
            raise CircuitBreakerOpenError(
                f"Circuit breaker '{self.name}' is OPEN. Requests blocked until cooldown expires."
            )
        if self._state == CircuitBreakerState.HALF_OPEN:
            if self._half_open_active_requests >= self.config.half_open_max_requests:
                raise CircuitBreakerOpenError(
                    f"Circuit breaker '{self.name}' is HALF_OPEN and reached max trial concurrency "
                    f"({self.config.half_open_max_requests})."
                )
            self._half_open_active_requests += 1

    def on_success(self) -> None:
        """Record successful execution."""
        self._total_calls += 1
        self._consecutive_failures = 0
        if self._state == CircuitBreakerState.HALF_OPEN:
            self._half_open_active_requests = max(0, self._half_open_active_requests - 1)
            self._consecutive_successes += 1
            if self._consecutive_successes >= self.config.half_open_success_threshold:
                self._transition_to(CircuitBreakerState.CLOSED)

    def on_failure(self, exception: Exception) -> None:
        """Record failed execution."""
        self._total_calls += 1
        self._failed_calls += 1
        self._consecutive_failures += 1
        self._last_failure_time = time.time()

        if self._state == CircuitBreakerState.HALF_OPEN:
            self._half_open_active_requests = max(0, self._half_open_active_requests - 1)
            self._transition_to(CircuitBreakerState.OPEN)
        elif self._state == CircuitBreakerState.CLOSED:
            if self._consecutive_failures >= self.config.failure_threshold:
                self._transition_to(CircuitBreakerState.OPEN)
            elif self._total_calls >= 10:
                rate = self._failed_calls / self._total_calls
                if rate >= self.config.failure_rate_threshold:
                    self._transition_to(CircuitBreakerState.OPEN)

    def reset(self) -> None:
        """Manually reset circuit breaker to CLOSED."""
        self._transition_to(CircuitBreakerState.CLOSED)
        self._total_calls = 0
        self._failed_calls = 0


class Bulkhead:
    """
    Bulkhead pattern isolating resources with concurrent limits and bounded queues.
    """

    def __init__(self, name: str, config: Optional[BulkheadConfig] = None) -> None:
        self.name = name
        self.config = config or BulkheadConfig()
        self._active_calls = 0
        self._queued_calls = 0

    @property
    def active_calls(self) -> int:
        return self._active_calls

    @property
    def queued_calls(self) -> int:
        return self._queued_calls

    def acquire(self) -> bool:
        if self._active_calls < self.config.max_concurrent_calls:
            self._active_calls += 1
            return True
        elif self._queued_calls < self.config.max_wait_queue_size:
            self._queued_calls += 1
            return True
        return False

    def release(self, was_queued: bool = False) -> None:
        if was_queued and self._queued_calls > 0:
            self._queued_calls -= 1
        elif self._active_calls > 0:
            self._active_calls -= 1


class RetryEngine:
    """
    Calculates backoff intervals and coordinates retries across 5 strategies:
    IMMEDIATE, LINEAR, EXPONENTIAL, RANDOMIZED_JITTER, ADAPTIVE.
    """

    @staticmethod
    def calculate_delay(attempt: int, config: RetryPolicyConfig, consecutive_errors: int = 0) -> float:
        """Compute delay for retry attempt (0-indexed)."""
        if attempt < 0:
            return 0.0

        if config.strategy == RetryStrategy.IMMEDIATE:
            return 0.0

        elif config.strategy == RetryStrategy.LINEAR:
            delay = config.initial_interval_seconds * (attempt + 1)

        elif config.strategy == RetryStrategy.EXPONENTIAL:
            delay = config.initial_interval_seconds * (config.backoff_multiplier ** attempt)

        elif config.strategy == RetryStrategy.RANDOMIZED_JITTER:
            base_delay = config.initial_interval_seconds * (config.backoff_multiplier ** attempt)
            jitter_range = base_delay * config.jitter_factor
            jitter = random.uniform(-jitter_range, jitter_range)
            delay = max(0.01, base_delay + jitter)

        elif config.strategy == RetryStrategy.ADAPTIVE:
            # Adaptive scales aggressively under high consecutive error count
            scale_factor = 1.0 + (consecutive_errors * 0.2)
            base_delay = config.initial_interval_seconds * (config.backoff_multiplier ** attempt) * scale_factor
            jitter = random.uniform(0, base_delay * config.jitter_factor)
            delay = base_delay + jitter

        else:
            delay = config.initial_interval_seconds

        return min(delay, config.max_interval_seconds)

    @staticmethod
    def is_retryable(exception: Exception, config: RetryPolicyConfig) -> bool:
        """Determine if the raised exception qualifies for retry."""
        exc_name = type(exception).__name__
        if not config.retryable_exceptions:
            return True
        return exc_name in config.retryable_exceptions or any(
            isinstance(exception, getattr(__builtins__, name, Exception))
            for name in config.retryable_exceptions
            if hasattr(__builtins__, name)
        )


class ReliabilityPolicyEngine:
    """
    Unified engine applying ReliabilityPolicy (Circuit Breaker, Retries, Bulkhead, Timeout, Fallback)
    around arbitrary synchronous and asynchronous workloads.
    """

    def __init__(self) -> None:
        self._circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._bulkheads: Dict[str, Bulkhead] = {}
        self._policies: Dict[str, ReliabilityPolicy] = {}

    def register_policy(self, policy: ReliabilityPolicy) -> None:
        self._policies[policy.policy_id] = policy

    def get_policy(self, policy_id: str) -> Optional[ReliabilityPolicy]:
        return self._policies.get(policy_id)

    def get_or_create_circuit_breaker(self, name: str, config: Optional[CircuitBreakerConfig] = None) -> CircuitBreaker:
        if name not in self._circuit_breakers:
            self._circuit_breakers[name] = CircuitBreaker(name, config)
        return self._circuit_breakers[name]

    def get_or_create_bulkhead(self, name: str, config: Optional[BulkheadConfig] = None) -> Bulkhead:
        if name not in self._bulkheads:
            self._bulkheads[name] = Bulkhead(name, config)
        return self._bulkheads[name]

    def execute_sync(
        self,
        target_name: str,
        operation: Callable[..., T],
        policy: Optional[ReliabilityPolicy] = None,
        fallback_fn: Optional[Callable[..., T]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> T:
        """
        Execute synchronous function wrapped in full reliability protections.
        """
        cb = self.get_or_create_circuit_breaker(target_name, policy.circuit_breaker if policy else None)
        bulkhead = self.get_or_create_bulkhead(target_name, policy.bulkhead if policy else None)
        retry_cfg = policy.retry_policy if policy else RetryPolicyConfig()
        timeout_budget = policy.timeout_budget_seconds if policy else 30.0

        if not bulkhead.acquire():
            if policy and policy.fallback_enabled and fallback_fn:
                logger.warning(f"Bulkhead full for '{target_name}', invoking fallback")
                return fallback_fn(*args, **kwargs)
            raise BulkheadFullError(f"Bulkhead '{target_name}' is saturated.")

        try:
            cb.before_call()
            start_time = time.time()
            consecutive_failures = 0
            last_exc: Optional[Exception] = None

            for attempt in range(retry_cfg.max_retries + 1):
                if time.time() - start_time > timeout_budget:
                    if policy and policy.fallback_enabled and fallback_fn:
                        logger.warning(f"Operation '{target_name}' exceeded timeout budget {timeout_budget}s, running fallback")
                        return fallback_fn(*args, **kwargs)
                    raise ReliabilityTimeoutError(f"Operation on '{target_name}' exceeded timeout budget {timeout_budget}s")

                try:
                    res = operation(*args, **kwargs)
                    cb.on_success()
                    return res
                except Exception as exc:
                    last_exc = exc
                    consecutive_failures += 1
                    cb.on_failure(exc)

                    if attempt >= retry_cfg.max_retries or not RetryEngine.is_retryable(exc, retry_cfg):
                        break

                    delay = RetryEngine.calculate_delay(attempt, retry_cfg, consecutive_failures)
                    time.sleep(delay)

            if policy and policy.fallback_enabled and fallback_fn:
                logger.warning(f"Operation '{target_name}' failed after {retry_cfg.max_retries} retries, running fallback")
                return fallback_fn(*args, **kwargs)

            if last_exc:
                raise last_exc
            raise RuntimeError(f"Operation on '{target_name}' failed without explicit exception")

        finally:
            bulkhead.release()

    async def execute_async(
        self,
        target_name: str,
        operation: Callable[..., Any],
        policy: Optional[ReliabilityPolicy] = None,
        fallback_fn: Optional[Callable[..., Any]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Execute asynchronous function wrapped in full reliability protections.
        """
        cb = self.get_or_create_circuit_breaker(target_name, policy.circuit_breaker if policy else None)
        bulkhead = self.get_or_create_bulkhead(target_name, policy.bulkhead if policy else None)
        retry_cfg = policy.retry_policy if policy else RetryPolicyConfig()
        timeout_budget = policy.timeout_budget_seconds if policy else 30.0

        if not bulkhead.acquire():
            if policy and policy.fallback_enabled and fallback_fn:
                logger.warning(f"Bulkhead full for '{target_name}', invoking fallback")
                if asyncio.iscoroutinefunction(fallback_fn):
                    return await fallback_fn(*args, **kwargs)
                return fallback_fn(*args, **kwargs)
            raise BulkheadFullError(f"Bulkhead '{target_name}' is saturated.")

        try:
            cb.before_call()
            start_time = time.time()
            consecutive_failures = 0
            last_exc: Optional[Exception] = None

            for attempt in range(retry_cfg.max_retries + 1):
                elapsed = time.time() - start_time
                if elapsed >= timeout_budget:
                    if policy and policy.fallback_enabled and fallback_fn:
                        logger.warning(f"Operation '{target_name}' exceeded timeout budget {timeout_budget}s, running fallback")
                        if asyncio.iscoroutinefunction(fallback_fn):
                            return await fallback_fn(*args, **kwargs)
                        return fallback_fn(*args, **kwargs)
                    raise ReliabilityTimeoutError(f"Operation on '{target_name}' exceeded timeout budget {timeout_budget}s")

                remaining_budget = max(0.01, timeout_budget - elapsed)
                try:
                    coro = operation(*args, **kwargs) if asyncio.iscoroutinefunction(operation) else asyncio.to_thread(operation, *args, **kwargs)
                    res = await asyncio.wait_for(coro, timeout=remaining_budget)
                    cb.on_success()
                    return res
                except (asyncio.TimeoutError, TimeoutError) as te:
                    last_exc = te
                    consecutive_failures += 1
                    cb.on_failure(te)
                    if attempt >= retry_cfg.max_retries:
                        break
                    delay = RetryEngine.calculate_delay(attempt, retry_cfg, consecutive_failures)
                    await asyncio.sleep(delay)
                except Exception as exc:
                    last_exc = exc
                    consecutive_failures += 1
                    cb.on_failure(exc)
                    if attempt >= retry_cfg.max_retries or not RetryEngine.is_retryable(exc, retry_cfg):
                        break
                    delay = RetryEngine.calculate_delay(attempt, retry_cfg, consecutive_failures)
                    await asyncio.sleep(delay)

            if policy and policy.fallback_enabled and fallback_fn:
                logger.warning(f"Operation '{target_name}' failed, running fallback")
                if asyncio.iscoroutinefunction(fallback_fn):
                    return await fallback_fn(*args, **kwargs)
                return fallback_fn(*args, **kwargs)

            if last_exc:
                raise last_exc
            raise RuntimeError(f"Operation on '{target_name}' failed without explicit exception")

        finally:
            bulkhead.release()
