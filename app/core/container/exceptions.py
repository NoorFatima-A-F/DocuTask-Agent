"""
Dependency Injection Container Exceptions.
"""

from typing import List, Optional


class ContainerException(Exception):
    """Base exception for dependency injection errors."""
    pass


class ServiceNotFoundException(ContainerException):
    """Raised when a requested service type is not registered."""
    def __init__(self, service_type: type):
        super().__init__(f"Service not registered in container: {service_type.__name__ if hasattr(service_type, '__name__') else service_type}")
        self.service_type = service_type


class CircularDependencyException(ContainerException):
    """Raised when a circular dependency cycle is detected during resolution."""
    def __init__(self, cycle_path: List[str]):
        path_str = " -> ".join(cycle_path)
        super().__init__(f"Circular dependency cycle detected: {path_str}")
        self.cycle_path = cycle_path


class ResolutionException(ContainerException):
    """Raised when service construction or parameter injection fails."""
    def __init__(self, service_type: type, reason: str, original_exception: Optional[Exception] = None):
        super().__init__(f"Failed to resolve {service_type.__name__ if hasattr(service_type, '__name__') else service_type}: {reason}")
        self.service_type = service_type
        self.reason = reason
        self.original_exception = original_exception
