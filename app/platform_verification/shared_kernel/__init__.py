"""
Shared Kernel for Enterprise Verification Platform.
Contains reusable enterprise primitives without business domain logic.
"""
from app.platform_verification.shared_kernel.result import Result, Success, Failure, Option, Some, Empty
from app.platform_verification.shared_kernel.identifiers import (
    StronglyTypedId, CorrelationId, ExecutionId, TenantId, RunId, EntityId, DefinitionId
)
from app.platform_verification.shared_kernel.clock import ClockInterface, SystemClock, VirtualClock
from app.platform_verification.shared_kernel.pagination import PaginationQuery, PaginatedResult, PageMetadata
from app.platform_verification.shared_kernel.filtering import FilterCriteria, SortOrder, SearchQuery
from app.platform_verification.shared_kernel.exceptions import (
    PlatformVerificationException, DomainException, EntityNotFoundException,
    InvariantViolationException, ConcurrencyException, SecurityViolationException,
    ConfigurationException
)
from app.platform_verification.shared_kernel.retry import RetryPolicy, ExponentialBackoffPolicy, CircuitBreaker
from app.platform_verification.shared_kernel.flags import FeatureFlagProvider, MemoryFeatureFlagProvider
from app.platform_verification.shared_kernel.security import CryptoUtils, CanonicalHasher, HMACSigner
from app.platform_verification.shared_kernel.events import BaseEvent, DomainEvent, IntegrationEvent, EventMetadata

__all__ = [
    "Result", "Success", "Failure", "Option", "Some", "Empty",
    "StronglyTypedId", "CorrelationId", "ExecutionId", "TenantId", "RunId", "EntityId", "DefinitionId",
    "ClockInterface", "SystemClock", "VirtualClock",
    "PaginationQuery", "PaginatedResult", "PageMetadata",
    "FilterCriteria", "SortOrder", "SearchQuery",
    "PlatformVerificationException", "DomainException", "EntityNotFoundException",
    "InvariantViolationException", "ConcurrencyException", "SecurityViolationException",
    "ConfigurationException",
    "RetryPolicy", "ExponentialBackoffPolicy", "CircuitBreaker",
    "FeatureFlagProvider", "MemoryFeatureFlagProvider",
    "CryptoUtils", "CanonicalHasher", "HMACSigner",
    "BaseEvent", "DomainEvent", "IntegrationEvent", "EventMetadata"
]
