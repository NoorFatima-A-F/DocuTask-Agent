"""Prompt Template Variable Definitions & Validation (Phase 8D)."""

from __future__ import annotations

import enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class VariableType(str, enum.Enum):
    """Supported variable data types."""
    STRING = "STRING"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    JSON = "JSON"
    LIST = "LIST"


class PromptVariableDefinition(BaseModel):
    """Schema specification for a prompt template input variable."""
    name: str
    var_type: VariableType = VariableType.STRING
    description: str = ""
    required: bool = True
    default_value: Optional[Any] = None

    def validate_value(self, value: Any) -> Any:
        """Validate input value against variable type definition."""
        if value is None:
            if self.required and self.default_value is None:
                raise ValueError(f"Required variable '{self.name}' was not provided")
            return self.default_value

        if self.var_type == VariableType.STRING:
            return str(value)
        elif self.var_type == VariableType.NUMBER:
            if not isinstance(value, (int, float)):
                try:
                    return float(value)
                except (ValueError, TypeError):
                    raise ValueError(f"Variable '{self.name}' must be a number, got {type(value).__name__}")
            return value
        elif self.var_type == VariableType.BOOLEAN:
            if isinstance(value, bool):
                return value
            if str(value).lower() in ("true", "1", "yes"):
                return True
            if str(value).lower() in ("false", "0", "no"):
                return False
            raise ValueError(f"Variable '{self.name}' must be a boolean")
        elif self.var_type == VariableType.LIST:
            if not isinstance(value, list):
                raise ValueError(f"Variable '{self.name}' must be a list")
            return value
        elif self.var_type == VariableType.JSON:
            if not isinstance(value, (dict, list)):
                raise ValueError(f"Variable '{self.name}' must be a JSON object or list")
            return value

        return value
