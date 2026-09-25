"""
Centralized Agent Configuration.
Provides configuration schemas for execution timeouts, retry strategies, confidence thresholds,
model selection, provider selection, and logging verbosity.
"""

from dataclasses import dataclass, field
from typing import Any, Dict
from app.agents.exceptions import ConfigurationException


@dataclass(frozen=True)
class AgentConfig:
    """Centralized execution configuration for autonomous agents."""

    retry_limit: int = 3
    timeout_seconds: float = 300.0
    confidence_threshold: float = 0.85
    parallelism: int = 4
    logging_verbosity: str = "INFO"
    model_name: str = "gemini-1.5-flash"
    provider_name: str = "gemini"
    extra_parameters: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.retry_limit < 0:
            raise ConfigurationException("retry_limit must be greater than or equal to 0.")
        if self.timeout_seconds <= 0:
            raise ConfigurationException("timeout_seconds must be greater than 0.")
        if not (0.0 <= self.confidence_threshold <= 1.0):
            raise ConfigurationException("confidence_threshold must be between 0.0 and 1.0.")
        if self.parallelism < 1:
            raise ConfigurationException("parallelism must be at least 1.")
