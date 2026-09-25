"""
Backward compatible alias module for errors/exceptions.
"""
from .exceptions import (
    PlatformException,
    PlatformVerificationError,
    DomainException,
    InvariantViolationError,
    EnvironmentNotReadyError,
    QualityGateFailedError,
    TamperDetectionError,
    ApplicationException,
    InfrastructureException,
    ValidationException,
    ConfigurationException,
    SecurityException,
    TimeoutException,
    DependencyException,
    ConcurrencyException,
    SerializationException
)

__all__ = [
    "PlatformException",
    "PlatformVerificationError",
    "DomainException",
    "InvariantViolationError",
    "EnvironmentNotReadyError",
    "QualityGateFailedError",
    "TamperDetectionError",
    "ApplicationException",
    "InfrastructureException",
    "ValidationException",
    "ConfigurationException",
    "SecurityException",
    "TimeoutException",
    "DependencyException",
    "ConcurrencyException",
    "SerializationException"
]
