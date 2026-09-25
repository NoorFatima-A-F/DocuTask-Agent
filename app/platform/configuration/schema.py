"""
Enterprise Configuration Schema Specifications.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class ConfigSource(str, Enum):
    """11-tier hierarchical configuration sources in ascending precedence order."""
    DEFAULTS = "DEFAULTS"                      # Priority 1 (Lowest)
    YAML_FILE = "YAML_FILE"                    # Priority 2
    ENVIRONMENT = "ENVIRONMENT"                # Priority 3
    CLOUD_CONFIG = "CLOUD_CONFIG"              # Priority 4
    SECRETS_MANAGER = "SECRETS_MANAGER"        # Priority 5
    RUNTIME_OVERRIDE = "RUNTIME_OVERRIDE"      # Priority 6
    FEATURE_FLAG = "FEATURE_FLAG"              # Priority 7
    ORGANIZATION = "ORGANIZATION"              # Priority 8
    WORKSPACE = "WORKSPACE"                    # Priority 9
    WORKFLOW = "WORKFLOW"                      # Priority 10
    EXECUTION_OVERRIDE = "EXECUTION_OVERRIDE"  # Priority 11 (Highest)


class ConfigDomain(str, Enum):
    """16 standard enterprise platform configuration domains."""
    DATABASE = "database"
    STORAGE = "storage"
    QUEUE = "queue"
    CACHE = "cache"
    SECURITY = "security"
    AUTHENTICATION = "authentication"
    AI = "ai"
    WORKFLOW = "workflow"
    AGENTS = "agents"
    LOGGING = "logging"
    METRICS = "metrics"
    TRACING = "tracing"
    PLUGINS = "plugins"
    CONNECTORS = "connectors"
    SCHEDULER = "scheduler"
    NOTIFICATIONS = "notifications"


@dataclass(frozen=True)
class ConfigEntrySchema:
    """Definition of a single configuration setting."""
    name: str
    data_type: str = "string"  # string, int, float, bool, list, dict
    default_value: Any = None
    description: str = ""
    domain: ConfigDomain = ConfigDomain.DATABASE
    version: str = "1.0.0"
    deprecated: bool = False
    deprecation_message: Optional[str] = None
    required: bool = False
    secret: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.data_type,
            "default": self.default_value,
            "description": self.description,
            "domain": self.domain.value,
            "version": self.version,
            "deprecated": self.deprecated,
            "deprecation_message": self.deprecation_message,
            "required": self.required,
            "secret": self.secret,
        }


@dataclass
class ResolvedConfigValue:
    """A resolved configuration value with origin attribution."""
    key: str
    value: Any
    source: ConfigSource
    domain: ConfigDomain
    schema: Optional[ConfigEntrySchema] = None
