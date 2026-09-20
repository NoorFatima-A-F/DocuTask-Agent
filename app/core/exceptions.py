"""
Application Domain Exception Classes.
Decouples business logic from HTTP transport concerns.
"""

from typing import Any, Dict, Optional


class BaseAppException(Exception):
    """Base exception class for all domain application exceptions."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        errors: Optional[Any] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors


class DuplicateResourceException(BaseAppException):
    """Raised when attempting to create a resource that already exists."""

    def __init__(self, message: str, errors: Optional[Any] = None):
        super().__init__(message=message, status_code=409, errors=errors)


class InvalidCredentialsException(BaseAppException):
    """Raised when authentication credentials fail validation."""

    def __init__(self, message: str = "Invalid email/username or password", errors: Optional[Any] = None):
        super().__init__(message=message, status_code=401, errors=errors)


class TokenException(BaseAppException):
    """Raised when JWT token verification fails or is expired/invalid."""

    def __init__(self, message: str = "Could not validate credentials", status_code: int = 401, errors: Optional[Any] = None):
        super().__init__(message=message, status_code=status_code, errors=errors)


class ResourceNotFoundException(BaseAppException):
    """Raised when a requested domain resource does not exist."""

    def __init__(self, message: str = "Resource not found", errors: Optional[Any] = None):
        super().__init__(message=message, status_code=404, errors=errors)


class ValidationAppException(BaseAppException):
    """Raised when business validation rules fail."""

    def __init__(self, message: str, errors: Optional[Any] = None):
        super().__init__(message=message, status_code=422, errors=errors)


class AccessDeniedException(BaseAppException):
    """Raised when authenticated user lacks privileges."""

    def __init__(self, message: str = "Permission denied", errors: Optional[Any] = None):
        super().__init__(message=message, status_code=403, errors=errors)
