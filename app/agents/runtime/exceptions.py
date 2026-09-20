"""
Runtime Kernel Exception Hierarchy.
Defines domain and operational exceptions for kernel boot, dependency graphs, service locator,
plugin validation, tenancy, and supervisor failures.
"""

from typing import Optional


class RuntimeKernelException(Exception):
    """Base exception for all platform runtime kernel failures."""

    def __init__(self, message: str, code: Optional[str] = None):
        super().__init__(message)
        self.code = code or self.__class__.__name__


class ServiceNotFoundError(RuntimeKernelException):
    """Raised when an interface cannot be resolved in the ServiceRegistry."""
    pass


class DuplicateServiceRegistrationError(RuntimeKernelException):
    """Raised when attempting to register a duplicate service without overwrite permission."""
    pass


class CyclicDependencyError(RuntimeKernelException):
    """Raised when a circular dependency is detected in the subsystem dependency graph."""
    pass


class ModuleLoadError(RuntimeKernelException):
    """Raised when a subsystem module descriptor fails to load or initialize."""
    pass


class PluginValidationError(RuntimeKernelException):
    """Raised when a plugin manifest is malformed, missing required fields, or incompatible."""
    pass


class InvalidRuntimeStateTransitionError(RuntimeKernelException):
    """Raised when an illegal lifecycle transition is attempted on the runtime kernel."""
    pass


class SubsystemCrashError(RuntimeKernelException):
    """Raised when a supervised subsystem crashes and exhausts its restart budget."""
    pass


class TenantIsolationViolationError(RuntimeKernelException):
    """Raised when a tenant attempts to access unshared resources of another tenant."""
    pass


class FeatureFlagEvaluationError(RuntimeKernelException):
    """Raised when a feature flag evaluation encounters an invalid schema or rule."""
    pass


class ConfigurationValidationError(RuntimeKernelException):
    """Raised when runtime environment configuration parameters are invalid or missing."""
    pass


class InvalidBindingError(RuntimeKernelException):
    """Raised when an implementation does not conform to the registered interface contract."""
    pass


class InvalidLifetimeDependencyError(RuntimeKernelException):
    """Raised when a longer-lived component attempts to depend on a shorter-lived component."""
    pass
