"""
Enterprise Tool Registry & Capability Resolution Layer Package.
Provides BaseTool, ToolDescriptor, ToolRegistry, CapabilityResolver, ToolSelector, and ToolFactory.
Decouples Planners from concrete provider implementations.
"""

from app.agents.tools.base import BaseTool
from app.agents.tools.cache import ToolCache
from app.agents.tools.capabilities import (
    Capability,
    CapabilityMatch,
    CapabilityRequirement,
    CapabilityScore,
)
from app.agents.tools.catalog import ToolCatalog
from app.agents.tools.context import (
    CapabilityContext,
    InvocationContext,
    ProviderContext,
    ToolExecutionContext,
)
from app.agents.tools.descriptor import (
    ToolDescriptor,
    ToolIdentity,
    ToolMetadata,
    ToolStatistics,
    ToolVersion,
)
from app.agents.tools.discovery import ToolDiscoveryEngine
from app.agents.tools.exceptions import (
    CapabilityNotFoundException,
    ProviderUnavailableException,
    RegistryException,
    SelectionException,
    ToolException,
    ToolNotFoundException,
    ToolValidationException,
    VersionConflictException,
)
from app.agents.tools.factory import ToolFactory
from app.agents.tools.health import ToolHealthMonitor, ToolHealthRecord
from app.agents.tools.interfaces import (
    ICapabilityResolver,
    IToolRegistry,
    IToolSelector,
)
from app.agents.tools.metadata import (
    CostProfile,
    LatencyProfile,
    ToolResourceRequirements,
    ToolSecurityProfile,
)
from app.agents.tools.metrics import ToolMetricsCollector
from app.agents.tools.policies import (
    FallbackPolicy,
    HealthPolicy,
    RegistrationPolicy,
    SelectionPolicy,
    SelectionStrategyEnum,
)
from app.agents.tools.provider import (
    ProviderHealth,
    ProviderMetadata,
    ProviderStatus,
    ToolProvider,
)
from app.agents.tools.registry import ToolRegistry
from app.agents.tools.resolver import CapabilityResolver
from app.agents.tools.selector import ToolSelector
from app.agents.tools.validation import ToolValidator

__all__ = [
    "BaseTool",
    "ToolDescriptor",
    "ToolIdentity",
    "ToolVersion",
    "ToolMetadata",
    "ToolStatistics",
    "CostProfile",
    "LatencyProfile",
    "ToolSecurityProfile",
    "ToolResourceRequirements",
    "Capability",
    "CapabilityRequirement",
    "CapabilityScore",
    "CapabilityMatch",
    "ProviderMetadata",
    "ProviderHealth",
    "ProviderStatus",
    "ToolProvider",
    "IToolRegistry",
    "ICapabilityResolver",
    "IToolSelector",
    "ToolRegistry",
    "CapabilityResolver",
    "ToolSelector",
    "ToolHealthMonitor",
    "ToolHealthRecord",
    "ToolCatalog",
    "ToolDiscoveryEngine",
    "ToolCache",
    "ToolValidator",
    "ToolMetricsCollector",
    "ToolFactory",
    "SelectionPolicy",
    "SelectionStrategyEnum",
    "FallbackPolicy",
    "HealthPolicy",
    "RegistrationPolicy",
    "ToolExecutionContext",
    "InvocationContext",
    "ProviderContext",
    "CapabilityContext",
    "ToolException",
    "ToolNotFoundException",
    "CapabilityNotFoundException",
    "ProviderUnavailableException",
    "VersionConflictException",
    "RegistryException",
    "SelectionException",
    "ToolValidationException",
]
