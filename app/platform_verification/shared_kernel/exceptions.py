"""
Strongly-Typed Exception Hierarchy.
"""
from typing import Any, Dict, Optional

class PlatformVerificationException(Exception):
    def __init__(self, message: str, code: str = "VERIFICATION_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class DomainException(PlatformVerificationException):
    def __init__(self, message: str, code: str = "DOMAIN_ERROR", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code=code, details=details)


class EntityNotFoundException(DomainException):
    def __init__(self, entity_name: str, entity_id: str):
        super().__init__(
            f"Entity '{entity_name}' with ID '{entity_id}' was not found.",
            code="ENTITY_NOT_FOUND",
            details={"entity_name": entity_name, "entity_id": entity_id}
        )


class InvariantViolationException(DomainException):
    def __init__(self, invariant_name: str, reason: str):
        super().__init__(
            f"Domain invariant '{invariant_name}' violated: {reason}",
            code="INVARIANT_VIOLATION",
            details={"invariant_name": invariant_name, "reason": reason}
        )


class ConcurrencyException(DomainException):
    def __init__(self, message: str = "Optimistic locking concurrency conflict detected."):
        super().__init__(message, code="CONCURRENCY_CONFLICT")


class SecurityViolationException(PlatformVerificationException):
    def __init__(self, message: str, policy_name: Optional[str] = None):
        super().__init__(
            message,
            code="SECURITY_VIOLATION",
            details={"policy_name": policy_name} if policy_name else {}
        )


class ConfigurationException(PlatformVerificationException):
    def __init__(self, message: str, scope: Optional[str] = None):
        super().__init__(
            message,
            code="CONFIGURATION_ERROR",
            details={"scope": scope} if scope else {}
        )
