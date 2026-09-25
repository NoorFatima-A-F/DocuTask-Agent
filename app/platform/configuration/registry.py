"""
Enterprise Configuration Schema Registry.
Registers and tracks configuration schemas across all 16 domains.
"""

from typing import Dict, List, Optional
from .schema import ConfigDomain, ConfigEntrySchema


class ConfigurationRegistry:
    """Central registry of known configuration schemas across platform domains."""

    def __init__(self):
        self._schemas: Dict[str, ConfigEntrySchema] = {}
        self._register_default_schemas()

    def register_schema(self, schema: ConfigEntrySchema) -> None:
        """Register a new configuration key schema."""
        self._schemas[schema.name] = schema

    def get_schema(self, name: str) -> Optional[ConfigEntrySchema]:
        """Get schema for a configuration key."""
        return self._schemas.get(name)

    def list_schemas(self, domain: Optional[ConfigDomain] = None) -> List[ConfigEntrySchema]:
        """List all schemas, optionally filtered by domain."""
        if domain is None:
            return list(self._schemas.values())
        return [s for s in self._schemas.values() if s.domain == domain]

    def _register_default_schemas(self) -> None:
        """Initialize standard schemas across the 16 platform domains."""
        default_entries = [
            # Database
            ConfigEntrySchema(name="database.url", data_type="string", default_value="sqlite+aiosqlite:///./docutask.db", domain=ConfigDomain.DATABASE, secret=True),
            ConfigEntrySchema(name="database.pool_size", data_type="int", default_value=20, domain=ConfigDomain.DATABASE),
            ConfigEntrySchema(name="database.max_overflow", data_type="int", default_value=10, domain=ConfigDomain.DATABASE),
            # Storage
            ConfigEntrySchema(name="storage.provider", data_type="string", default_value="local", domain=ConfigDomain.STORAGE),
            ConfigEntrySchema(name="storage.bucket", data_type="string", default_value="docutask-documents", domain=ConfigDomain.STORAGE),
            # Queue
            ConfigEntrySchema(name="queue.broker_url", data_type="string", default_value="memory://", domain=ConfigDomain.QUEUE, secret=True),
            ConfigEntrySchema(name="queue.concurrency", data_type="int", default_value=10, domain=ConfigDomain.QUEUE),
            # Cache
            ConfigEntrySchema(name="cache.type", data_type="string", default_value="memory", domain=ConfigDomain.CACHE),
            ConfigEntrySchema(name="cache.ttl_seconds", data_type="int", default_value=3600, domain=ConfigDomain.CACHE),
            # Security
            ConfigEntrySchema(name="security.enable_zero_trust", data_type="bool", default_value=True, domain=ConfigDomain.SECURITY),
            ConfigEntrySchema(name="security.jwt_secret", data_type="string", default_value="default-insecure-secret-change-me", domain=ConfigDomain.SECURITY, secret=True),
            # AI
            ConfigEntrySchema(name="ai.default_model", data_type="string", default_value="gemini-1.5-flash", domain=ConfigDomain.AI),
            ConfigEntrySchema(name="ai.temperature", data_type="float", default_value=0.2, domain=ConfigDomain.AI),
            ConfigEntrySchema(name="ai.max_tokens", data_type="int", default_value=4096, domain=ConfigDomain.AI),
            # Workflow
            ConfigEntrySchema(name="workflow.max_parallel_steps", data_type="int", default_value=5, domain=ConfigDomain.WORKFLOW),
            ConfigEntrySchema(name="workflow.default_timeout_seconds", data_type="int", default_value=300, domain=ConfigDomain.WORKFLOW),
            # Agents
            ConfigEntrySchema(name="agents.max_iterations", data_type="int", default_value=10, domain=ConfigDomain.AGENTS),
            ConfigEntrySchema(name="agents.consensus_threshold", data_type="float", default_value=0.8, domain=ConfigDomain.AGENTS),
            # Logging
            ConfigEntrySchema(name="logging.level", data_type="string", default_value="INFO", domain=ConfigDomain.LOGGING),
            ConfigEntrySchema(name="logging.format", data_type="string", default_value="json", domain=ConfigDomain.LOGGING),
            # Metrics
            ConfigEntrySchema(name="metrics.enabled", data_type="bool", default_value=True, domain=ConfigDomain.METRICS),
            # Tracing
            ConfigEntrySchema(name="tracing.sample_rate", data_type="float", default_value=1.0, domain=ConfigDomain.TRACING),
        ]
        for entry in default_entries:
            self.register_schema(entry)
