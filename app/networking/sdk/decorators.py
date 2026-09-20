"""Decorators for Service Mesh Endpoints and Resilience."""

from __future__ import annotations

import functools
from typing import Any, Callable, Optional

from ..resilience.circuit_breaker import CircuitBreaker, CircuitBreakerConfig
from ..resilience.retry import RetryPolicy, RetryPolicyEngine


def mesh_service(name: str, namespace: str = "default", mtls: bool = True):
    """Class decorator to tag a class as a mesh-managed service."""
    def decorator(cls):
        setattr(cls, "__mesh_service_name__", name)
        setattr(cls, "__mesh_namespace__", namespace)
        setattr(cls, "__mesh_mtls__", mtls)
        return cls
    return decorator


def mesh_endpoint(action: str, method: str = "POST", path: Optional[str] = None):
    """Method decorator to expose a handler as a mesh-callable RPC/HTTP action."""
    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        setattr(wrapper, "__mesh_action__", action)
        setattr(wrapper, "__mesh_method__", method)
        setattr(wrapper, "__mesh_path__", path or f"/{action}")
        return wrapper
    return decorator


def circuit_protected(service_name: str, config: Optional[CircuitBreakerConfig] = None):
    """Function decorator applying circuit breaker protection around a call."""
    cb = CircuitBreaker(service_name=service_name, config=config)

    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not cb.can_execute():
                raise RuntimeError(f"Circuit breaker for {service_name} is OPEN")
            try:
                res = func(*args, **kwargs)
                cb.record_result(is_failure=False)
                return res
            except Exception:
                cb.record_result(is_failure=True)
                raise
        return wrapper
    return decorator


def with_retry(max_attempts: int = 3, initial_backoff_ms: float = 50.0):
    """Function decorator applying exponential retry logic."""
    policy = RetryPolicy(max_attempts=max_attempts, initial_backoff_ms=initial_backoff_ms)
    engine = RetryPolicyEngine(default_policy=policy)

    def decorator(func: Callable[..., Any]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt >= max_attempts:
                        raise
                    delay_ms = engine.calculate_backoff(attempt, policy)
                    import time
                    time.sleep(delay_ms / 1000.0)
                    attempt += 1
        return wrapper
    return decorator
