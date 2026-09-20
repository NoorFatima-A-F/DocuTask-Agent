"""
Enterprise Result[T, E] pattern and Error Model.
Railway-oriented programming primitives for rock-solid error handling without unhandled exceptions.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Generic, TypeVar, Union, Optional, Callable, Any, Dict, List

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")

class ErrorSeverity(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class ErrorCategory(str, Enum):
    VALIDATION = "VALIDATION"
    AUTHORIZATION = "AUTHORIZATION"
    AUTHENTICATION = "AUTHENTICATION"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    BUSINESS_RULE = "BUSINESS_RULE"
    SECURITY = "SECURITY"
    TIMEOUT = "TIMEOUT"
    DEPENDENCY = "DEPENDENCY"
    CONCURRENCY = "CONCURRENCY"
    SERIALIZATION = "SERIALIZATION"
    UNEXPECTED = "UNEXPECTED"

@dataclass(frozen=True)
class ErrorModel:
    """Rich structured error representation."""
    code: str
    message: str
    category: ErrorCategory = ErrorCategory.UNEXPECTED
    severity: ErrorSeverity = ErrorSeverity.ERROR
    details: Dict[str, Any] = field(default_factory=dict)
    retryable: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @classmethod
    def validation(cls, message: str, code: str = "ERR_VALIDATION", details: Optional[Dict[str, Any]] = None) -> "ErrorModel":
        return cls(code=code, message=message, category=ErrorCategory.VALIDATION, severity=ErrorSeverity.WARNING, details=details or {})

    @classmethod
    def authorization(cls, message: str, code: str = "ERR_UNAUTHORIZED", details: Optional[Dict[str, Any]] = None) -> "ErrorModel":
        return cls(code=code, message=message, category=ErrorCategory.AUTHORIZATION, severity=ErrorSeverity.ERROR, details=details or {})

    @classmethod
    def infrastructure(cls, message: str, code: str = "ERR_INFRASTRUCTURE", retryable: bool = True, details: Optional[Dict[str, Any]] = None) -> "ErrorModel":
        return cls(code=code, message=message, category=ErrorCategory.INFRASTRUCTURE, severity=ErrorSeverity.ERROR, retryable=retryable, details=details or {})

    @classmethod
    def business_rule(cls, message: str, code: str = "ERR_BUSINESS_RULE", details: Optional[Dict[str, Any]] = None) -> "ErrorModel":
        return cls(code=code, message=message, category=ErrorCategory.BUSINESS_RULE, severity=ErrorSeverity.ERROR, details=details or {})

    @classmethod
    def unexpected(cls, message: str, code: str = "ERR_UNEXPECTED", details: Optional[Dict[str, Any]] = None) -> "ErrorModel":
        return cls(code=code, message=message, category=ErrorCategory.UNEXPECTED, severity=ErrorSeverity.CRITICAL, details=details or {})

@dataclass(frozen=True)
class Ok(Generic[T]):
    """Successful computation outcome."""
    value: T
    is_ok: bool = True
    is_err: bool = False
    warnings: List[str] = field(default_factory=list)

    def unwrap(self) -> T:
        return self.value

    def unwrap_or(self, default: T) -> T:
        return self.value

    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        return self.value

    def map(self, fn: Callable[[T], U]) -> "Ok[U]":
        return Ok(fn(self.value), warnings=list(self.warnings))

    def map_err(self, fn: Callable[[Any], Any]) -> "Ok[T]":
        return self

    def flat_map(self, fn: Callable[[T], "Result[U, Any]"]) -> "Result[U, Any]":
        return fn(self.value)

    def and_then(self, fn: Callable[[T], "Result[U, Any]"]) -> "Result[U, Any]":
        return self.flat_map(fn)

    def match(self, on_ok: Callable[[T], U], on_err: Callable[[Any], U]) -> U:
        return on_ok(self.value)

@dataclass(frozen=True)
class Err(Generic[E]):
    """Failed computation outcome."""
    error: E
    is_ok: bool = False
    is_err: bool = True

    def unwrap(self) -> Any:
        raise ValueError(f"Called unwrap on an Err: {self.error}")

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, fn: Callable[[], T]) -> T:
        return fn()

    def map(self, fn: Callable[[Any], Any]) -> "Err[E]":
        return self

    def map_err(self, fn: Callable[[E], U]) -> "Err[U]":
        return Err(fn(self.error))

    def flat_map(self, fn: Callable[[Any], "Result[Any, Any]"]) -> "Err[E]":
        return self

    def and_then(self, fn: Callable[[Any], "Result[Any, Any]"]) -> "Err[E]":
        return self

    def match(self, on_ok: Callable[[Any], U], on_err: Callable[[E], U]) -> U:
        return on_err(self.error)

Result = Union[Ok[T], Err[E]]

# Helper factory functions
def Success(value: T, warnings: Optional[List[str]] = None) -> Ok[T]:
    return Ok(value=value, warnings=warnings or [])

def Failure(error: E) -> Err[E]:
    return Err(error=error)

def ValidationFailure(message: str, details: Optional[Dict[str, Any]] = None) -> Err[ErrorModel]:
    return Err(ErrorModel.validation(message=message, details=details))

def AuthorizationFailure(message: str, details: Optional[Dict[str, Any]] = None) -> Err[ErrorModel]:
    return Err(ErrorModel.authorization(message=message, details=details))

def InfrastructureFailure(message: str, retryable: bool = True, details: Optional[Dict[str, Any]] = None) -> Err[ErrorModel]:
    return Err(ErrorModel.infrastructure(message=message, retryable=retryable, details=details))

def BusinessRuleFailure(message: str, details: Optional[Dict[str, Any]] = None) -> Err[ErrorModel]:
    return Err(ErrorModel.business_rule(message=message, details=details))

def UnexpectedFailure(message: str, details: Optional[Dict[str, Any]] = None) -> Err[ErrorModel]:
    return Err(ErrorModel.unexpected(message=message, details=details))
