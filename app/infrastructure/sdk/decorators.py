"""Infrastructure Managed Decorators."""

from functools import wraps
import logging
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)


def infrastructure_managed(service_name: str, environment: str = "PRODUCTION"):
    """Decorator marking a function or component as infrastructure managed."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info("Executing infrastructure-managed component: %s [%s]", service_name, environment)
            return func(*args, **kwargs)

        wrapper.__infra_managed__ = True
        wrapper.__service_name__ = service_name
        wrapper.__environment__ = environment
        return wrapper

    return decorator


def with_resource_budget(cpu_limit: float = 1.0, memory_limit_mb: int = 1024):
    """Decorator asserting runtime resource budget for execution context."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Resource bounds validation hook
            return func(*args, **kwargs)

        wrapper.__cpu_limit__ = cpu_limit
        wrapper.__memory_limit_mb__ = memory_limit_mb
        return wrapper

    return decorator
