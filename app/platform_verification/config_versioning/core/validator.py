"""
Configuration Schema & Policy Validator.
"""
from typing import Any, Dict, List, Tuple
from pydantic import ValidationError

class ConfigurationValidator:
    @staticmethod
    def validate_resolved_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        # Required fields check
        if "timeout_seconds" not in config:
            errors.append("Missing required configuration key: 'timeout_seconds'")
        elif config["timeout_seconds"] <= 0:
            errors.append("Invalid 'timeout_seconds': must be greater than 0")

        if "ai" in config and isinstance(config["ai"], dict):
            ai_cfg = config["ai"]
            if "temperature" in ai_cfg and not (0.0 <= ai_cfg["temperature"] <= 2.0):
                errors.append("Invalid 'ai.temperature': must be between 0.0 and 2.0")
            if "max_tokens" in ai_cfg and ai_cfg["max_tokens"] <= 0:
                errors.append("Invalid 'ai.max_tokens': must be positive")

        return len(errors) == 0, errors

configuration_validator = ConfigurationValidator()
