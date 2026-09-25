"""
Enterprise Shared Kernel Package.
Minimal, framework-independent, domain-independent platform primitives.
"""
from .domain import (
    BaseEntity, Entity, AggregateRoot, ValueObject, DomainServiceMarker,
    Specification, RepositoryContract, UnitOfWorkContract
)
from .typed_ids import (
    TypedId, EntityId, ExecutionId, VerificationRunId, DatasetId,
    VerificationId, EvidenceId, MetricId, PluginId, ConfigurationId,
    EnvironmentId, AuditId, CertificationId, CertificateId, TenantId,
    CorrelationId, TraceId, RequestId, SessionId, CausationId
)
from .result import (
    Result, Ok, Err, ErrorModel, ErrorSeverity, ErrorCategory,
    Success, Failure, ValidationFailure, AuthorizationFailure,
    InfrastructureFailure, BusinessRuleFailure, UnexpectedFailure
)
from .exceptions import (
    PlatformException, PlatformVerificationError, DomainException,
    InvariantViolationError, ApplicationException, InfrastructureException,
    ValidationException, ConfigurationException, SecurityException,
    TamperDetectionError, TimeoutException, DependencyException,
    EnvironmentNotReadyError, QualityGateFailedError, ConcurrencyException,
    SerializationException
)
from .validation import (
    ValidationResult, ValidationErrorDetail, ValidationSeverity,
    ValidationRule, RequiredRule, LengthRule, RangeRule, RegexRule,
    EnumRule, PredicateRule, CompositeValidator
)
from .clock import (
    TimeProvider, SystemClock, SystemTimeProvider, MonotonicClock,
    VirtualClock, DeterministicTimeProvider, FrozenClock
)
from .correlation import (
    CorrelationContext, get_current_correlation, set_current_correlation,
    correlation_scope
)
from .pagination import (
    PaginationQuery, PaginatedResult, CursorPaginationQuery,
    CursorPaginatedResult, SortOrder, SortCriteria, FilterOperator,
    FilterCriteria
)
from .versioning import (
    SemanticVersion, VersionModel, SchemaVersion, ArtifactVersion,
    ModelVersion, ConfigurationVersion, DatasetVersion, PluginVersion,
    EnvironmentVersion
)
from .configuration import (
    ConfigurationSource, ConfigurationSnapshotContract,
    ConfigurationValidatorContract, ConfigurationLoaderContract,
    ConfigurationProviderContract
)
from .logging import (
    LogLevel, LogRecord, SensitiveDataMasker, StructuredLoggerContract
)
from .metrics import (
    MetricType, MetricUnit, CounterContract, GaugeContract,
    HistogramContract, TimerContract, DistributionSummaryContract,
    MetricsCollectorContract
)
from .tracing import (
    SpanStatus, SpanContextContract, SpanContract, TracerContract
)
from .events import (
    EventMetadata, BaseEvent, DomainEvent, ApplicationEvent,
    IntegrationEvent, SystemEvent, EventHandlerContract,
    EventBusContract, EventBus, get_event_bus
)
from .serialization import (
    SerializationFormat, SerializerContract, JsonSerializer,
    SerializationSchemaValidatorContract
)
from .security import (
    PermissionContract, RoleContract, PrincipalContract,
    SecurityContext, AuthorizationPolicyContract, Hasher, HmacSigner
)
from .resilience import (
    RetryStrategy, RetryPolicy, CircuitState, CircuitBreakerContract,
    BulkheadContract, RateLimiterContract
)
from .storage import (
    StorageType, FileMetadata, FileStorageContract, ArtifactStorageContract,
    EvidenceStorageContract, DatasetStorageContract, TemporaryStorageContract
)
from .constants import (
    ISO_8601_FORMAT, UTC_TIMESTAMP_FORMAT, DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE, MIME_JSON, MIME_YAML, MIME_OCTET_STREAM,
    MIME_TEXT_PLAIN, MIME_PDF, MIME_PNG, HASH_SHA256, HASH_SHA512,
    HMAC_SHA256, ENCODING_UTF8, ENCODING_ASCII, ENCODING_BASE64,
    SEMVER_REGEX_PATTERN
)
from .acl_contracts import (
    AiPromptRequest, AiInferenceResult, AiProviderContract,
    OcrRequest, OcrExtractionData, OcrProviderContract,
    MessagingProviderContract, EmbeddingProviderContract,
    VectorStoreContract
)
from .governance import SharedKernelGovernancePolicy

__all__ = [
    # domain
    "BaseEntity", "Entity", "AggregateRoot", "ValueObject", "DomainServiceMarker",
    "Specification", "RepositoryContract", "UnitOfWorkContract",
    # typed_ids
    "TypedId", "EntityId", "ExecutionId", "VerificationRunId", "DatasetId",
    "VerificationId", "EvidenceId", "MetricId", "PluginId", "ConfigurationId",
    "EnvironmentId", "AuditId", "CertificationId", "CertificateId", "TenantId",
    "CorrelationId", "TraceId", "RequestId", "SessionId", "CausationId",
    # result
    "Result", "Ok", "Err", "ErrorModel", "ErrorSeverity", "ErrorCategory",
    "Success", "Failure", "ValidationFailure", "AuthorizationFailure",
    "InfrastructureFailure", "BusinessRuleFailure", "UnexpectedFailure",
    # exceptions
    "PlatformException", "PlatformVerificationError", "DomainException",
    "InvariantViolationError", "ApplicationException", "InfrastructureException",
    "ValidationException", "ConfigurationException", "SecurityException",
    "TamperDetectionError", "TimeoutException", "DependencyException",
    "EnvironmentNotReadyError", "QualityGateFailedError", "ConcurrencyException",
    "SerializationException",
    # validation
    "ValidationResult", "ValidationErrorDetail", "ValidationSeverity",
    "ValidationRule", "RequiredRule", "LengthRule", "RangeRule", "RegexRule",
    "EnumRule", "PredicateRule", "CompositeValidator",
    # clock
    "TimeProvider", "SystemClock", "SystemTimeProvider", "MonotonicClock",
    "VirtualClock", "DeterministicTimeProvider", "FrozenClock",
    # correlation
    "CorrelationContext", "get_current_correlation", "set_current_correlation",
    "correlation_scope",
    # pagination
    "PaginationQuery", "PaginatedResult", "CursorPaginationQuery",
    "CursorPaginatedResult", "SortOrder", "SortCriteria", "FilterOperator",
    "FilterCriteria",
    # versioning
    "SemanticVersion", "VersionModel", "SchemaVersion", "ArtifactVersion",
    "ModelVersion", "ConfigurationVersion", "DatasetVersion", "PluginVersion",
    "EnvironmentVersion",
    # configuration
    "ConfigurationSource", "ConfigurationSnapshotContract",
    "ConfigurationValidatorContract", "ConfigurationLoaderContract",
    "ConfigurationProviderContract",
    # logging
    "LogLevel", "LogRecord", "SensitiveDataMasker", "StructuredLoggerContract",
    # metrics
    "MetricType", "MetricUnit", "CounterContract", "GaugeContract",
    "HistogramContract", "TimerContract", "DistributionSummaryContract",
    "MetricsCollectorContract",
    # tracing
    "SpanStatus", "SpanContextContract", "SpanContract", "TracerContract",
    # events
    "EventMetadata", "BaseEvent", "DomainEvent", "ApplicationEvent",
    "IntegrationEvent", "SystemEvent", "EventHandlerContract",
    "EventBusContract", "EventBus", "get_event_bus",
    # serialization
    "SerializationFormat", "SerializerContract", "JsonSerializer",
    "SerializationSchemaValidatorContract",
    # security
    "PermissionContract", "RoleContract", "PrincipalContract",
    "SecurityContext", "AuthorizationPolicyContract", "Hasher", "HmacSigner",
    # resilience
    "RetryStrategy", "RetryPolicy", "CircuitState", "CircuitBreakerContract",
    "BulkheadContract", "RateLimiterContract",
    # storage
    "StorageType", "FileMetadata", "FileStorageContract", "ArtifactStorageContract",
    "EvidenceStorageContract", "DatasetStorageContract", "TemporaryStorageContract",
    # constants
    "ISO_8601_FORMAT", "UTC_TIMESTAMP_FORMAT", "DEFAULT_PAGE_SIZE",
    "MAX_PAGE_SIZE", "MIME_JSON", "MIME_YAML", "MIME_OCTET_STREAM",
    "MIME_TEXT_PLAIN", "MIME_PDF", "MIME_PNG", "HASH_SHA256", "HASH_SHA512",
    "HMAC_SHA256", "ENCODING_UTF8", "ENCODING_ASCII", "ENCODING_BASE64",
    "SEMVER_REGEX_PATTERN",
    # acl_contracts
    "AiPromptRequest", "AiInferenceResult", "AiProviderContract",
    "OcrRequest", "OcrExtractionData", "OcrProviderContract",
    "MessagingProviderContract", "EmbeddingProviderContract",
    "VectorStoreContract",
    # governance
    "SharedKernelGovernancePolicy"
]
