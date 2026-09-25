"""
Enterprise Configuration Validator.
"""

from typing import Any, List, Optional
from .schema import ConfigEntrySchema


class ConfigurationValidationError(Exception):
    """Raised when configuration values fail validation rules."""
    def __init__(self, message: str, errors: Optional[List[str]] = None):
        super().__init__(message)
        self.errors = errors or []


class ConfigurationValidator:
    """Validates configuration values against domain schemas and constraints."""

    @staticmethod
    def validate_type(key: str, value: Any, expected_type: str) -> None:
        """Validate data type of value."""
        if value is None:
            return

        if expected_type == "int":
            if not isinstance(value, int) or isinstance(value, bool):
                try:
                    int(value)
                except (ValueError, TypeError):
                    raise ConfigurationValidationError(f"Configuration key '{key}' expects int, got {type(value).__name__}")
        elif expected_type == "float":
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                try:
                    float(value)
                except (ValueError, TypeError):
                    raise ConfigurationValidationError(f"Configuration key '{key}' expects float, got {type(value).__name__}")
        elif expected_type == "bool":
            if not isinstance(value, bool):
                if isinstance(value, str) and value.lower() in ("true", "false", "1", "0", "yes", "no"):
                    return
                raise ConfigurationValidationError(f"Configuration key '{key}' expects bool, got {type(value).__name__}")
        elif expected_type == "list":
            if not isinstance(value, (list, tuple)):
                raise ConfigurationValidationError(f"Configuration key '{key}' expects list, got {type(value).__name__}")
        elif expected_type == "dict":
            if not isinstance(value, dict):
                raise ConfigurationValidationError(f"Configuration key '{key}' expects dict, got {type(value).__name__}")

    @classmethod
    def validate_entry(cls, schema: ConfigEntrySchema, value: Any) -> Any:
        """Validate and cast a configuration entry according to its schema."""
        if value is None:
            if schema.required and schema.default_value is None:
                raise ConfigurationValidationError(f"Required configuration key '{schema.name}' is missing")
            return schema.default_value

        cls.validate_type(schema.name, value, schema.data_type)

        # Type coercion
        if schema.data_type == "int" and not isinstance(value, int):
            return int(value)
        elif schema.data_type == "float" and not isinstance(value, float):
            return float(value)
        elif schema.data_type == "bool" and not isinstance(value, bool):
            return str(value).lower() in ("true", "1", "yes")
        elif schema.data_type == "string":
            return str(value)

        return value
