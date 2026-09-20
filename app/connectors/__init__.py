"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Main Package.
Provides the enterprise operating system for capability-based integrations, installable connectors,
credential isolation, resilience, protocol adapters, and Model Context Protocol (MCP) gateways.
"""

from app.connectors.actions.executor import ActionExecutor
from app.connectors.adapters.base import (
    BaseProtocolAdapter,
    GraphQLAdapter,
    RESTAdapter,
    SOAPAdapter,
    gRPCAdapter,
)
from app.connectors.analytics.analytics import ConnectorAnalytics, FleetAnalyticsReport
from app.connectors.authentication.auth_manager import AuthenticationManager
from app.connectors.authentication.credential_store import CredentialStore
from app.connectors.authentication.secret_provider import (
    AWSSecretProvider,
    AzureSecretProvider,
    EnvSecretProvider,
    GCPSecretProvider,
    InMemoryVaultSecretProvider,
    SecretProvider,
)
from app.connectors.certification.framework import CertificationReport, ConnectorCertification
from app.connectors.core.exceptions import (
    ActionExecutionError,
    AuthenticationError,
    CapabilityNotFoundError,
    CertificationError,
    CircuitBreakerOpenError,
    ConnectorError,
    ConnectorNotFoundError,
    CredentialNotFoundError,
    InvalidConnectorStateError,
    MCPProtocolError,
    PolicyViolationError,
    RateLimitExceededError,
    SandboxViolationError,
    SchemaMappingError,
    TransformationError,
    WebhookVerificationError,
)
from app.connectors.core.models import (
    ActionDescriptor,
    AuthType,
    CapabilityDescriptor,
    Connector,
    ConnectorCategory,
    ConnectorHealth,
    ConnectorPolicyRule,
    ConnectorStatus,
    CredentialMetadata,
    ExecutionResult,
    NormalizedEvent,
    TriggerDescriptor,
    TriggerType,
)
from app.connectors.events.normalizer import EventNormalizer
from app.connectors.lifecycle.manager import ConnectorLifecycleEvent, ConnectorLifecycleManager
from app.connectors.mappings.schema_mapper import FieldMappingRule, SchemaMapper, SchemaMappingPlan
from app.connectors.marketplace.registry import ConnectorPackageManifest, MarketplaceRegistry
from app.connectors.mcp.gateway import MCPGateway, MCPServerRegistration
from app.connectors.observability.metrics import ConnectorMetricsSummary, ConnectorObservability
from app.connectors.policies.policy_engine import ConnectorPolicyEngine, PolicyEvaluationResult
from app.connectors.registry.capability_registry import CapabilityRegistry
from app.connectors.registry.connector_registry import ConnectorRegistry
from app.connectors.resilience.circuit_breaker import CircuitBreaker, CircuitBreakerConfig, CircuitState
from app.connectors.resilience.rate_limiter import RateLimitAlgorithm, RateLimiter, RateLimitPolicy
from app.connectors.resilience.retry_engine import (
    ConnectorFailureCategory,
    ConnectorRetryEngine,
    RetryPolicy,
)
from app.connectors.runtime.runtime import ConnectorRuntime
from app.connectors.sandbox.sandbox import ConnectorSandbox, SandboxConfig
from app.connectors.sdk.base import BaseConnector
from app.connectors.sdk.builder import ConnectorBuilder, FunctionalConnector
from app.connectors.simulation.simulator import ConnectorSimulator
from app.connectors.testing.framework import ConnectorTestFramework, TestReport
from app.connectors.triggers.engine import TriggerEngine, TriggerState, TriggerSubscription
from app.connectors.webhooks.engine import WebhookConfig, WebhookEngine

__all__ = [
    # Core Domain & Exceptions
    "Connector",
    "ConnectorCategory",
    "ConnectorStatus",
    "ConnectorHealth",
    "AuthType",
    "TriggerType",
    "CapabilityDescriptor",
    "ActionDescriptor",
    "TriggerDescriptor",
    "NormalizedEvent",
    "CredentialMetadata",
    "ExecutionResult",
    "ConnectorPolicyRule",
    "ConnectorError",
    "ConnectorNotFoundError",
    "CapabilityNotFoundError",
    "InvalidConnectorStateError",
    "AuthenticationError",
    "CredentialNotFoundError",
    "RateLimitExceededError",
    "CircuitBreakerOpenError",
    "PolicyViolationError",
    "SandboxViolationError",
    "ActionExecutionError",
    "TransformationError",
    "SchemaMappingError",
    "WebhookVerificationError",
    "CertificationError",
    "MCPProtocolError",
    # Lifecycle
    "ConnectorLifecycleManager",
    "ConnectorLifecycleEvent",
    # SDK
    "BaseConnector",
    "ConnectorBuilder",
    "FunctionalConnector",
    # Registry
    "ConnectorRegistry",
    "CapabilityRegistry",
    # Authentication & Secrets
    "AuthenticationManager",
    "CredentialStore",
    "SecretProvider",
    "InMemoryVaultSecretProvider",
    "EnvSecretProvider",
    "GCPSecretProvider",
    "AWSSecretProvider",
    "AzureSecretProvider",
    # Runtime & Actions
    "ConnectorRuntime",
    "ActionExecutor",
    # Triggers & Webhooks
    "TriggerEngine",
    "TriggerState",
    "TriggerSubscription",
    "WebhookEngine",
    "WebhookConfig",
    # Events, Transformations & Mappings
    "EventNormalizer",
    "TransformationEngine",
    "SchemaMapper",
    "FieldMappingRule",
    "SchemaMappingPlan",
    # Resilience
    "ConnectorRetryEngine",
    "ConnectorFailureCategory",
    "RetryPolicy",
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitState",
    "RateLimiter",
    "RateLimitPolicy",
    "RateLimitAlgorithm",
    # Sandbox & Policies
    "ConnectorSandbox",
    "SandboxConfig",
    "ConnectorPolicyEngine",
    "PolicyEvaluationResult",
    # Observability & Analytics
    "ConnectorObservability",
    "ConnectorMetricsSummary",
    "ConnectorAnalytics",
    "FleetAnalyticsReport",
    # Testing & Simulation
    "ConnectorTestFramework",
    "TestReport",
    "ConnectorSimulator",
    # Marketplace & Certification
    "MarketplaceRegistry",
    "ConnectorPackageManifest",
    "ConnectorCertification",
    "CertificationReport",
    # MCP & Adapters
    "MCPGateway",
    "MCPServerRegistration",
    "BaseProtocolAdapter",
    "RESTAdapter",
    "GraphQLAdapter",
    "SOAPAdapter",
    "gRPCAdapter",
]
