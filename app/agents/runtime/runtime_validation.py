"""
Runtime Validation Rules & Reports.
Validates configurations, dependency DAGs, interface compliance, and plugin integrity before kernel activation.
"""

from typing import List
from pydantic import BaseModel, Field
from app.agents.runtime.configuration import PlatformRuntimeConfig
from app.agents.runtime.dependency_manager import DependencyManager
from app.agents.runtime.exceptions import ConfigurationValidationError


class RuntimeValidationReport(BaseModel):
    """Report detailing results of pre-flight kernel and subsystem validation checks."""
    is_valid: bool = True
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}


class RuntimeValidator:
    """Pre-flight validation rules executed during the startup pipeline."""

    @staticmethod
    def validate_configuration(config: PlatformRuntimeConfig) -> None:
        """Validates platform runtime configuration parameters."""
        if config.max_concurrent_sessions <= 0:
            raise ConfigurationValidationError("max_concurrent_sessions must be greater than zero.")
        if config.startup_timeout_seconds <= 0:
            raise ConfigurationValidationError("startup_timeout_seconds must be greater than zero.")

    @staticmethod
    def validate_dependencies(dep_manager: DependencyManager) -> None:
        """Ensures subsystem dependencies form a valid acyclic graph."""
        dep_manager.compute_initialization_order()
