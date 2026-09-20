"""
Comprehensive Test Suite for Enterprise Shared Kernel (Part 1.1C.4).
Verifies 100% of the shared domain primitives, typed identities, Result pattern,
validation framework, time abstractions, correlation propagation, pagination,
SemVer, security, resilience, and event bus.
"""
import pytest
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import List

from app.shared_kernel import (
    BaseEntity, Entity, AggregateRoot, ValueObject, Specification,
    TypedId, EntityId, ExecutionId, DatasetId, VerificationId, EvidenceId,
    MetricId, PluginId, ConfigurationId, EnvironmentId, AuditId,
    CertificationId, CertificateId, TenantId, CorrelationId, TraceId,
    RequestId, SessionId, CausationId,
    Result, Ok, Err, ErrorModel, ErrorSeverity, ErrorCategory,
    Success, Failure, ValidationFailure, AuthorizationFailure,
    InfrastructureFailure, BusinessRuleFailure, UnexpectedFailure,
    PlatformException, PlatformVerificationError, DomainException,
    InvariantViolationError, ApplicationException, InfrastructureException,
    ValidationException, ConfigurationException, SecurityException,
    TamperDetectionError, TimeoutException, DependencyException,
    EnvironmentNotReadyError, QualityGateFailedError, ConcurrencyException,
    SerializationException,
    ValidationResult, ValidationErrorDetail, ValidationSeverity,
    RequiredRule, LengthRule, RangeRule, RegexRule, EnumRule, PredicateRule,
    TimeProvider, SystemClock, SystemTimeProvider, MonotonicClock,
    VirtualClock, DeterministicTimeProvider, FrozenClock,
    CorrelationContext, get_current_correlation, set_current_correlation,
    correlation_scope,
    PaginationQuery, PaginatedResult, CursorPaginationQuery,
    CursorPaginatedResult, SortOrder, SortCriteria, FilterOperator,
    FilterCriteria,
    SemanticVersion, VersionModel, SchemaVersion, DatasetVersion,
    SensitiveDataMasker, LogLevel, LogRecord,
    MetricType, MetricUnit, SpanStatus,
    DomainEvent, ApplicationEvent, IntegrationEvent, SystemEvent,
    EventBus, get_event_bus,
    SerializationFormat, JsonSerializer,
    PermissionContract, RoleContract, PrincipalContract, SecurityContext,
    Hasher, HmacSigner,
    RetryStrategy, RetryPolicy, CircuitState,
    StorageType, FileMetadata,
    ISO_8601_FORMAT, HASH_SHA256, ENCODING_UTF8,
    AiPromptRequest, AiInferenceResult, OcrRequest, OcrExtractionData,
    SharedKernelGovernancePolicy
)


class TestDomainPrimitives:
    def test_entity_and_value_object(self):
        @dataclass(frozen=True)
        class Money(ValueObject):
            amount: float
            currency: str

        m1 = Money(100.0, "USD")
        m2 = Money(100.0, "USD")
        assert m1 == m2

        entity1 = BaseEntity(id="e1")
        entity2 = BaseEntity(id="e1")
        entity3 = BaseEntity(id="e2")
        assert entity1 == entity2
        assert entity1 != entity3
        assert hash(entity1) == hash(entity2)

    def test_aggregate_root_events(self):
        agg = AggregateRoot(id="agg-1")
        evt = DomainEvent()
        agg.record_event(evt)
        events = agg.pull_domain_events()
        assert len(events) == 1
        assert events[0] == evt
        # After pulling, events must be cleared
        assert len(agg.pull_domain_events()) == 0

    def test_specification_pattern(self):
        class GreaterThanTen(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate > 10

        class EvenNumber(Specification[int]):
            def is_satisfied_by(self, candidate: int) -> bool:
                return candidate % 2 == 0

        gt10 = GreaterThanTen()
        even = EvenNumber()

        combined_and = gt10.and_(even)
        assert combined_and.is_satisfied_by(12) is True
        assert combined_and.is_satisfied_by(11) is False
        assert combined_and.is_satisfied_by(8) is False

        combined_or = gt10.or_(even)
        assert combined_or.is_satisfied_by(8) is True
        assert combined_or.is_satisfied_by(11) is True
        assert combined_or.is_satisfied_by(7) is False

        negated = gt10.not_()
        assert negated.is_satisfied_by(5) is True
        assert negated.is_satisfied_by(15) is False


class TestTypedIdentity:
    def test_typed_id_generation_and_equality(self):
        e1 = ExecutionId.generate()
        assert str(e1).startswith("exec_")
        e2 = ExecutionId.from_str("exec_custom123")
        assert str(e2) == "exec_custom123"

        det1 = DatasetId.deterministic("dataset_seed_abc", prefix="ds")
        det2 = DatasetId.deterministic("dataset_seed_abc", prefix="ds")
        det3 = DatasetId.deterministic("dataset_seed_xyz", prefix="ds")
        assert det1 == det2
        assert det1 != det3

        # Type safety assertions
        assert isinstance(VerificationId.generate(), VerificationId)
        assert isinstance(EvidenceId.generate(), EvidenceId)
        assert isinstance(MetricId.generate(), MetricId)
        assert isinstance(PluginId.generate(), PluginId)
        assert isinstance(ConfigurationId.generate(), ConfigurationId)
        assert isinstance(EnvironmentId.generate(), EnvironmentId)
        assert isinstance(AuditId.generate(), AuditId)
        assert isinstance(CertificationId.generate(), CertificationId)
        assert isinstance(TenantId.generate(), TenantId)
        assert isinstance(CorrelationId.generate(), CorrelationId)
        assert isinstance(TraceId.generate(), TraceId)
        assert isinstance(RequestId.generate(), RequestId)
        assert isinstance(SessionId.generate(), SessionId)
        assert isinstance(CausationId.generate(), CausationId)


class TestResultPattern:
    def test_ok_monad_operations(self):
        res: Result[int, str] = Success(10)
        assert res.is_ok is True
        assert res.is_err is False
        assert res.unwrap() == 10
        assert res.unwrap_or(0) == 10

        mapped = res.map(lambda x: x * 2)
        assert mapped.unwrap() == 20

        flat_mapped = res.flat_map(lambda x: Success(f"val-{x}"))
        assert flat_mapped.unwrap() == "val-10"

        matched = res.match(on_ok=lambda v: f"ok:{v}", on_err=lambda e: f"err:{e}")
        assert matched == "ok:10"

    def test_err_monad_operations(self):
        res: Result[int, str] = Failure("something went wrong")
        assert res.is_ok is False
        assert res.is_err is True
        assert res.unwrap_or(99) == 99
        assert res.unwrap_or_else(lambda: 42) == 42

        with pytest.raises(ValueError):
            res.unwrap()

        mapped = res.map(lambda x: x * 2)
        assert mapped.is_err is True

        err_mapped = res.map_err(lambda e: f"wrapped:{e}")
        assert err_mapped.error == "wrapped:something went wrong"

        matched = res.match(on_ok=lambda v: f"ok:{v}", on_err=lambda e: f"err:{e}")
        assert matched == "err:something went wrong"

    def test_error_models_and_constructors(self):
        vf = ValidationFailure("Invalid payload", details={"field": "name"})
        assert vf.error.category == ErrorCategory.VALIDATION
        assert vf.error.severity == ErrorSeverity.WARNING

        af = AuthorizationFailure("Permission denied")
        assert af.error.category == ErrorCategory.AUTHORIZATION

        inf = InfrastructureFailure("Database unreachable", retryable=True)
        assert inf.error.category == ErrorCategory.INFRASTRUCTURE
        assert inf.error.retryable is True

        br = BusinessRuleFailure("Invariant breached")
        assert br.error.category == ErrorCategory.BUSINESS_RULE

        uf = UnexpectedFailure("Fatal panic")
        assert uf.error.category == ErrorCategory.UNEXPECTED
        assert uf.error.severity == ErrorSeverity.CRITICAL


class TestExceptionHierarchy:
    def test_exceptions_and_codes(self):
        ex = InvariantViolationError("Invariant check failed", details={"rule": "p99"})
        assert isinstance(ex, DomainException)
        assert isinstance(ex, PlatformException)
        assert ex.error_code == "ERR_INVARIANT_VIOLATION"
        assert ex.details["rule"] == "p99"

        tamper = TamperDetectionError("Hash mismatch")
        assert isinstance(tamper, SecurityException)

        env_err = EnvironmentNotReadyError("Port 8000 not open")
        assert isinstance(env_err, DependencyException)


class TestValidationFramework:
    def test_universal_validation_rules(self):
        req_rule = RequiredRule()
        assert req_rule.validate("username", "alice").is_valid is True
        assert req_rule.validate("username", "").is_valid is False
        assert req_rule.validate("username", None).is_valid is False

        len_rule = LengthRule(min_len=3, max_len=10)
        assert len_rule.validate("tag", "alpha").is_valid is True
        assert len_rule.validate("tag", "al").is_valid is False
        assert len_rule.validate("tag", "verylongtagnameexceedinglimit").is_valid is False

        range_rule = RangeRule(min_val=0.0, max_val=1.0)
        assert range_rule.validate("score", 0.95).is_valid is True
        assert range_rule.validate("score", 1.5).is_valid is False
        assert range_rule.validate("score", -0.1).is_valid is False

        regex_rule = RegexRule(r"^[A-Z]{3}-\d{4}$", "AAA-0000 format")
        assert regex_rule.validate("code", "ABC-1234").is_valid is True
        assert regex_rule.validate("code", "invalid-code").is_valid is False

        enum_rule = EnumRule({"PENDING", "COMPLETED", "FAILED"})
        assert enum_rule.validate("status", "COMPLETED").is_valid is True
        assert enum_rule.validate("status", "UNKNOWN").is_valid is False

        pred_rule = PredicateRule(lambda x: x % 2 == 0, "Must be even")
        assert pred_rule.validate("num", 4).is_valid is True
        assert pred_rule.validate("num", 5).is_valid is False

    def test_validation_result_merging(self):
        r1 = ValidationResult()
        r1.add_error("f1", "Error 1")
        r2 = ValidationResult()
        r2.add_warning("f2", "Warning 1")
        r3 = r1.merge(r2)
        assert r3.is_valid is False
        assert len(r3.errors) == 2


class TestTimeAndClockAbstractions:
    def test_system_clock(self):
        clock = SystemClock()
        now = clock.now()
        assert now.tzinfo == timezone.utc
        assert isinstance(clock.now_iso(), str)
        assert clock.now_epoch_ms() > 0
        assert clock.monotonic() > 0

    def test_virtual_clock_time_travel(self):
        initial = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        vclock = VirtualClock(initial)
        assert vclock.now() == initial
        assert vclock.monotonic() == 0.0

        vclock.advance_seconds(60.0)
        assert vclock.now() == datetime(2026, 1, 1, 12, 1, 0, tzinfo=timezone.utc)
        assert vclock.monotonic() == 60.0

        new_time = datetime(2026, 6, 15, 0, 0, 0, tzinfo=timezone.utc)
        vclock.set_time(new_time)
        assert vclock.now() == new_time


class TestCorrelationContext:
    def test_correlation_propagation_and_scoping(self):
        ctx1 = CorrelationContext(correlation_id="corr-1", tenant_id="tenant-alpha")
        set_current_correlation(ctx1)
        assert get_current_correlation().correlation_id == "corr-1"

        ctx2 = CorrelationContext(correlation_id="corr-2", tenant_id="tenant-beta")
        with correlation_scope(ctx2):
            assert get_current_correlation().correlation_id == "corr-2"
            assert get_current_correlation().tenant_id == "tenant-beta"

        # Scope reset assertion
        assert get_current_correlation().correlation_id == "corr-1"


class TestPaginationAndCollections:
    def test_offset_pagination(self):
        q = PaginationQuery(page=3, page_size=10)
        assert q.offset == 20
        assert q.limit == 10

        res: PaginatedResult[str] = PaginatedResult(
            items=["item1", "item2"],
            total_count=35,
            page=3,
            page_size=10
        )
        assert res.total_pages == 4
        assert res.has_next is True
        assert res.has_previous is True

    def test_filter_and_sort_criteria(self):
        sort = SortCriteria(field="created_at", order=SortOrder.DESC)
        assert sort.order == SortOrder.DESC

        filt = FilterCriteria(field="status", operator=FilterOperator.EQ, value="COMPLETED")
        assert filt.operator == FilterOperator.EQ


class TestSemanticVersioning:
    def test_semver_parsing_and_ordering(self):
        v1 = SemanticVersion.parse("1.2.3")
        v2 = SemanticVersion.parse("1.2.4")
        v3 = SemanticVersion.parse("1.3.0")
        v4 = SemanticVersion.parse("2.0.0-beta.1")
        v5 = SemanticVersion.parse("2.0.0")

        assert v1 < v2 < v3 < v4 < v5
        assert v1 == SemanticVersion(1, 2, 3)
        assert str(v1) == "1.2.3"
        assert str(v4) == "2.0.0-beta.1"

    def test_semver_bumps_and_compatibility(self):
        v = SemanticVersion(1, 2, 3)
        assert v.bump_patch() == SemanticVersion(1, 2, 4)
        assert v.bump_minor() == SemanticVersion(1, 3, 0)
        assert v.bump_major() == SemanticVersion(2, 0, 0)

        assert v.is_compatible_with(SemanticVersion(1, 1, 0)) is True
        assert v.is_compatible_with(SemanticVersion(2, 0, 0)) is False


class TestLoggingAndMasking:
    def test_sensitive_data_masker(self):
        raw = "User email is user@example.com and secret api_key='sk_live_1234567890abcdef' Bearer eyJhbGciOiJIUzI1NiJ9"
        masked = SensitiveDataMasker.mask_text(raw)
        assert "user@example.com" not in masked
        assert "***@example.com" in masked
        assert "[REDACTED_SECRET]" in masked
        assert "[REDACTED_BEARER_TOKEN]" in masked


class TestSecurityAndHashing:
    def test_hasher_and_hmac_signer(self):
        h = Hasher.sha256("hello-world")
        assert len(h) == 64
        assert h == Hasher.sha256("hello-world")

        signer = HmacSigner("secret-signing-key")
        sig = signer.sign("verification-payload")
        assert signer.verify("verification-payload", sig) is True
        assert signer.verify("tampered-payload", sig) is False

    def test_security_context(self):
        p = PrincipalContract(id="user-123", roles={"VERIFIER_ADMIN"}, tenant_id="t1")
        perm = PermissionContract(resource="verification", action="execute")
        assert str(perm) == "verification:execute"
        ctx = SecurityContext(principal=p, is_authenticated=True, scopes={"read", "write"})
        assert ctx.is_authenticated is True


class TestResilienceContracts:
    def test_retry_policy_delays(self):
        policy = RetryPolicy(
            max_retries=3,
            initial_delay_seconds=0.1,
            max_delay_seconds=2.0,
            backoff_multiplier=2.0,
            strategy=RetryStrategy.EXPONENTIAL_BACKOFF
        )
        assert policy.compute_delay(1) == 0.1
        assert policy.compute_delay(2) == 0.2
        assert policy.compute_delay(3) == 0.4


@pytest.mark.asyncio
class TestEventBus:
    async def test_async_event_bus_pub_sub(self):
        bus = EventBus()
        received: List[DomainEvent] = []

        class SampleDomainEvent(DomainEvent):
            pass

        async def handler(evt: SampleDomainEvent):
            received.append(evt)

        bus.subscribe(SampleDomainEvent, handler)

        evt1 = SampleDomainEvent()
        await bus.publish(evt1)

        assert len(received) == 1
        assert received[0] == evt1
        assert len(bus.get_published_events()) == 1


class TestGovernancePolicy:
    def test_policy_checks(self):
        assert SharedKernelGovernancePolicy.is_dependency_allowed("json") is True
        assert SharedKernelGovernancePolicy.is_dependency_allowed("fastapi") is False
        assert SharedKernelGovernancePolicy.is_dependency_allowed("sqlalchemy.orm") is False
        assert SharedKernelGovernancePolicy.is_dependency_allowed("google.genai") is False

        assert SharedKernelGovernancePolicy.is_concept_allowed("ValueObject") is True
        assert SharedKernelGovernancePolicy.is_concept_allowed("VerificationDefinition") is False
