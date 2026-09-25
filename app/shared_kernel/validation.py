"""
Universal Validation Framework.
Provides reusable rule, validator, and composable validation primitives without domain coupling.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Generic, TypeVar, List, Optional, Pattern, Set, Callable
import re

T = TypeVar("T")

class ValidationSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

@dataclass(frozen=True)
class ValidationErrorDetail:
    field_name: str
    message: str
    code: str = "VAL_ERR"
    severity: ValidationSeverity = ValidationSeverity.ERROR
    actual_value: Optional[Any] = None

@dataclass
class ValidationResult:
    is_valid: bool = True
    errors: List[ValidationErrorDetail] = field(default_factory=list)

    def add_error(self, field_name: str, message: str, code: str = "VAL_ERR", actual_value: Optional[Any] = None) -> None:
        self.is_valid = False
        self.errors.append(ValidationErrorDetail(field_name, message, code, ValidationSeverity.ERROR, actual_value))

    def add_warning(self, field_name: str, message: str, code: str = "VAL_WARN", actual_value: Optional[Any] = None) -> None:
        self.errors.append(ValidationErrorDetail(field_name, message, code, ValidationSeverity.WARNING, actual_value))

    def merge(self, other: "ValidationResult") -> "ValidationResult":
        merged = ValidationResult(is_valid=self.is_valid and other.is_valid)
        merged.errors = list(self.errors) + list(other.errors)
        return merged

class ValidationRule(ABC, Generic[T]):
    """Abstract validation rule."""
    @abstractmethod
    def validate(self, field_name: str, value: T) -> ValidationResult:
        pass

class RequiredRule(ValidationRule[Any]):
    def validate(self, field_name: str, value: Any) -> ValidationResult:
        res = ValidationResult()
        if value is None or (isinstance(value, str) and not value.strip()):
            res.add_error(field_name, f"Field '{field_name}' is required and cannot be empty.", "VAL_REQUIRED", value)
        return res

class LengthRule(ValidationRule[str]):
    def __init__(self, min_len: int = 0, max_len: Optional[int] = None):
        self.min_len = min_len
        self.max_len = max_len

    def validate(self, field_name: str, value: str) -> ValidationResult:
        res = ValidationResult()
        if value is None:
            return res
        length = len(value)
        if length < self.min_len:
            res.add_error(field_name, f"Field '{field_name}' length ({length}) is less than minimum {self.min_len}.", "VAL_MIN_LENGTH", value)
        if self.max_len is not None and length > self.max_len:
            res.add_error(field_name, f"Field '{field_name}' length ({length}) exceeds maximum {self.max_len}.", "VAL_MAX_LENGTH", value)
        return res

class RangeRule(ValidationRule[float]):
    def __init__(self, min_val: Optional[float] = None, max_val: Optional[float] = None):
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, field_name: str, value: float) -> ValidationResult:
        res = ValidationResult()
        if value is None:
            return res
        if self.min_val is not None and value < self.min_val:
            res.add_error(field_name, f"Field '{field_name}' value ({value}) is less than minimum {self.min_val}.", "VAL_MIN_VAL", value)
        if self.max_val is not None and value > self.max_val:
            res.add_error(field_name, f"Field '{field_name}' value ({value}) exceeds maximum {self.max_val}.", "VAL_MAX_VAL", value)
        return res

class RegexRule(ValidationRule[str]):
    def __init__(self, pattern: str, description: str = "pattern match"):
        self.pattern: Pattern[str] = re.compile(pattern)
        self.description = description

    def validate(self, field_name: str, value: str) -> ValidationResult:
        res = ValidationResult()
        if value is None:
            return res
        if not self.pattern.match(value):
            res.add_error(field_name, f"Field '{field_name}' does not match required format ({self.description}).", "VAL_REGEX", value)
        return res

class EnumRule(ValidationRule[Any]):
    def __init__(self, allowed_values: Set[Any]):
        self.allowed_values = allowed_values

    def validate(self, field_name: str, value: Any) -> ValidationResult:
        res = ValidationResult()
        if value is None:
            return res
        if value not in self.allowed_values:
            res.add_error(field_name, f"Field '{field_name}' value '{value}' not in allowed set: {self.allowed_values}.", "VAL_ENUM", value)
        return res

class PredicateRule(ValidationRule[T]):
    def __init__(self, predicate: Callable[[T], bool], error_message: str, error_code: str = "VAL_PREDICATE"):
        self.predicate = predicate
        self.error_message = error_message
        self.error_code = error_code

    def validate(self, field_name: str, value: T) -> ValidationResult:
        res = ValidationResult()
        if not self.predicate(value):
            res.add_error(field_name, self.error_message, self.error_code, value)
        return res

class CompositeValidator(ABC, Generic[T]):
    """Reusable composite validator orchestrator."""
    def __init__(self):
        self._rules: List[ValidationRule[Any]] = []

    def add_rule(self, rule: ValidationRule[Any]) -> "CompositeValidator[T]":
        self._rules.append(rule)
        return self

    @abstractmethod
    def validate(self, candidate: T) -> ValidationResult:
        pass
