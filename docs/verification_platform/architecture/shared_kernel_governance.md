# Shared Kernel Architectural Governance & Contribution Policy

## 1. Executive Vision
The **Shared Kernel** (`app/shared_kernel/`) provides the foundational, domain-agnostic, and framework-independent building blocks for the entire DocuTask Agent Enterprise Verification Platform. It enables high cohesion and loose coupling across all 12 Bounded Contexts.

---

## 2. Core Architectural Invariants

### Invariant 1 — Absolute Minimalism
The Shared Kernel must contain only abstractions that are universally applicable and stable across the entire platform. Domain-specific or context-specific concepts are strictly prohibited.

### Invariant 2 — Zero Business Logic
No business entities, calculation models, domain services, or verification rules may exist in `app/shared_kernel/`.

### Invariant 3 — Zero External Framework Dependencies
The Shared Kernel must NEVER import:
- Web frameworks (`fastapi`, `starlette`)
- ORM/Database drivers (`sqlalchemy`, `alembic`, `asyncpg`, `psycopg2`)
- Caching/Task engines (`redis`, `celery`, `temporalio`)
- Container/Infra tools (`docker`)
- External AI SDKs (`google.genai`, `openai`, `anthropic`)
- Vendor Cloud SDKs (`google.cloud`, `boto3`, `azure`)
- Observability concrete SDKs (`opentelemetry`)

### Invariant 4 — Direction of Dependencies
- **Allowed**: `app/contexts/*` $\rightarrow$ `app/shared_kernel`
- **Forbidden**: `app/shared_kernel` $\rightarrow$ `app/contexts/*`, `app/models/*`, `app/api/*`, `app/infrastructure/*`

---

## 3. Five-Question Contribution Filter
Before any new abstraction is approved for addition to the Shared Kernel, the pull request / change proposal must answer:

1. **Is it universally reusable across 3 or more bounded contexts?** (If No $\rightarrow$ Reject)
2. **Is it 100% free of verification business logic?** (If No $\rightarrow$ Reject)
3. **Is it free of third-party framework dependencies?** (If No $\rightarrow$ Reject)
4. **Is the interface stable with long-term backward compatibility guarantees?** (If No $\rightarrow$ Reject)
5. **Is code duplication in individual contexts preferable to adding coupling?** (If Yes $\rightarrow$ Reject)

---

## 4. Module Map

| Module | Architectural Scope | Primary Types / Contracts |
|---|---|---|
| `domain.py` | Core DDD primitives | `BaseEntity`, `Entity[ID]`, `AggregateRoot[ID]`, `ValueObject`, `Specification[T]`, `RepositoryContract[T, ID]`, `UnitOfWorkContract` |
| `typed_ids.py` | Strongly-typed ID system | `TypedId[T]`, `EntityId`, `ExecutionId`, `DatasetId`, `VerificationId`, `EvidenceId`, `MetricId`, `PluginId`, `ConfigurationId`, `EnvironmentId`, `AuditId`, `CertificationId`, `TenantId`, `CorrelationId`, `TraceId`, `SessionId` |
| `result.py` | Railway-oriented Result pattern | `Result[T, E]`, `Ok[T]`, `Err[E]`, `ErrorModel`, `ErrorSeverity`, `ErrorCategory`, `Success`, `Failure`, `ValidationFailure`, `InfrastructureFailure`, `BusinessRuleFailure` |
| `exceptions.py` | Platform Exception taxonomy | `PlatformException`, `DomainException`, `ApplicationException`, `InfrastructureException`, `ValidationException`, `ConfigurationException`, `SecurityException`, `TimeoutException`, `DependencyException`, `ConcurrencyException`, `SerializationException` |
| `validation.py` | Universal validation framework | `ValidationResult`, `ValidationErrorDetail`, `ValidationRule[T]`, `RequiredRule`, `LengthRule`, `RangeRule`, `RegexRule`, `EnumRule`, `PredicateRule`, `CompositeValidator[T]` |
| `clock.py` | Time & clock abstractions | `TimeProvider`, `SystemClock`, `MonotonicClock`, `VirtualClock`, `DeterministicTimeProvider`, `FrozenClock` |
| `correlation.py` | Distributed context propagation | `CorrelationContext`, `get_current_correlation()`, `set_current_correlation()`, `correlation_scope()` |
| `pagination.py` | Collections, paging, filters | `PaginationQuery`, `PaginatedResult[T]`, `CursorPaginationQuery`, `CursorPaginatedResult[T]`, `SortOrder`, `FilterCriteria`, `FilterOperator` |
| `versioning.py` | SemVer 2.0.0 & version models | `SemanticVersion`, `VersionModel`, `SchemaVersion`, `ArtifactVersion`, `ModelVersion`, `ConfigurationVersion`, `DatasetVersion`, `PluginVersion` |
| `configuration.py`| Config contracts & snapshots | `ConfigurationSource`, `ConfigurationSnapshotContract`, `ConfigurationValidatorContract`, `ConfigurationProviderContract` |
| `logging.py` | Structured logging & masking | `LogLevel`, `LogRecord`, `SensitiveDataMasker`, `StructuredLoggerContract` |
| `metrics.py` | Telemetry instrumentation ports | `MetricType`, `MetricUnit`, `CounterContract`, `GaugeContract`, `HistogramContract`, `TimerContract`, `MetricsCollectorContract` |
| `tracing.py` | Distributed tracing ports | `SpanStatus`, `SpanContextContract`, `SpanContract`, `TracerContract` |
| `events.py` | Domain/Integration events & bus | `BaseEvent`, `DomainEvent`, `ApplicationEvent`, `IntegrationEvent`, `SystemEvent`, `EventMetadata`, `EventBusContract`, `EventBus`, `get_event_bus()` |
| `serialization.py`| Serialization contracts | `SerializationFormat`, `SerializerContract`, `JsonSerializer`, `SerializationSchemaValidatorContract` |
| `security.py` | Security context, Hasher, HMAC | `PermissionContract`, `RoleContract`, `PrincipalContract`, `SecurityContext`, `Hasher` (SHA-256, SHA-512), `HmacSigner` |
| `resilience.py` | Resilience & retry contracts | `RetryStrategy`, `RetryPolicy`, `CircuitState`, `CircuitBreakerContract`, `BulkheadContract`, `RateLimiterContract` |
| `storage.py` | File & CAS storage contracts | `StorageType`, `FileMetadata`, `FileStorageContract`, `ArtifactStorageContract`, `EvidenceStorageContract`, `DatasetStorageContract` |
| `constants.py` | Platform universal constants | `ISO_8601_FORMAT`, `UTC_TIMESTAMP_FORMAT`, MIME types, encodings, hash algorithms |
| `acl_contracts.py`| External ACL boundary ports | `AiProviderContract`, `OcrProviderContract`, `MessagingProviderContract`, `EmbeddingProviderContract`, `VectorStoreContract` |
| `governance.py` | Policy checker & invariants | `SharedKernelGovernancePolicy` |

---

## 5. Automated CI Invariant Verification
All pull requests must pass:
```powershell
python tooling/governance/shared_kernel_validator.py
python -m pytest tests/platform_verification/test_shared_kernel_suite.py -v
```
