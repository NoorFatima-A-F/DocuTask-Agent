"""
Platform Kernel Exception Hierarchy.
Provides base exceptions, error codes, and correlation tracking.
"""

from typing import Any, Dict, Optional
import uuid


class PlatformKernelException(Exception):
    """Base exception for all Platform Kernel operational and domain errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "PLATFORM_KERNEL_ERROR",
        correlation_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """Serialize exception to structured dictionary."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "correlation_id": self.correlation_id,
            "details": self.details,
        }


class BootstrapException(PlatformKernelException):
    """Raised when runtime bootstrap or initialization sequence fails."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="KERNEL_BOOTSTRAP_ERROR", details=details)


class LifecycleException(PlatformKernelException):
    """Raised when an invalid lifecycle transition or lifecycle hook failure occurs."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="KERNEL_LIFECYCLE_ERROR", details=details)


class ConfigurationException(PlatformKernelException):
    """Raised when configuration validation, precedence resolution, or schema fails."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="KERNEL_CONFIG_ERROR", details=details)


class DependencyResolutionException(PlatformKernelException):
    """Raised when the dependency injection container fails to resolve a dependency or encounters a circular cycle."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="KERNEL_DI_RESOLUTION_ERROR", details=details)


class ModuleLoadException(PlatformKernelException):
    """Raised when a module fails to load, validate, or satisfy dependencies."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="KERNEL_MODULE_LOAD_ERROR", details=details)


class PluginException(PlatformKernelException):
    """Raised when a plugin manifest is invalid, corrupted, or violates permission policy."""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, error_code="KERNEL_PLUGIN_ERROR", details=details)
