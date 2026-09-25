"""Domain Models for Phase 3H.3.8: AI Provider Health Verification Framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class AIProviderHealthState(str, Enum):
    UNKNOWN = "UNKNOWN"
    INITIALIZING = "INITIALIZING"
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    RATE_LIMITED = "RATE_LIMITED"
    UNAVAILABLE = "UNAVAILABLE"
    RECOVERING = "RECOVERING"


class AIFailureCategory(str, Enum):
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"       # HTTP 500, 503 -> Retry
    AUTHENTICATION_FAILURE = "AUTHENTICATION_FAILURE"   # HTTP 401 -> Alert & Pause
    QUOTA_EXHAUSTION = "QUOTA_EXHAUSTION"               # HTTP 429 -> Backoff & Queue
    INVALID_RESPONSE = "INVALID_RESPONSE"               # Schema failure -> Fallback/Retry


class AIQualityCertificationTier(str, Enum):
    FAILED = "Failed"                                         # < 80%
    IMPROVEMENT_REQUIRED = "Improvement Required"             # 80 - 89%
    PRODUCTION_AI_READY = "Production AI Ready"               # 90 - 94%
    AI_RELIABILITY_CERTIFIED = "AI Reliability Certified"     # 95 - 100%


@dataclass
class AIProviderHealthStatus:
    provider: str
    status: AIProviderHealthState
    latency_ms: float
    authentication: str  # VALID / INVALID / EXPIRED
    quota_status: str   # AVAILABLE / THROTTLED / EXHAUSTED
    model: str
    timestamp: str
    failure_count_24h: int = 0
    last_successful_request: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIProviderHealthReport:
    total_providers_monitored: int
    primary_provider: str
    primary_status: AIProviderHealthState
    providers: List[AIProviderHealthStatus]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIAuthVerificationItem:
    provider: str
    key_format_valid: bool
    permissions_sufficient: bool
    expiration_detected: bool
    authenticated: bool
    status: str
    details: str


@dataclass
class AIAuthReport:
    total_providers_checked: int
    all_authenticated: bool
    checks: List[AIAuthVerificationItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIConnectivityItem:
    provider: str
    endpoint: str
    dns_resolved: bool
    tls_handshake_ms: float
    connection_success_rate_pct: float
    timeout_count: int
    passed: bool


@dataclass
class AIConnectivityReport:
    total_endpoints_tested: int
    avg_connection_success_rate_pct: float
    endpoints: List[AIConnectivityItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AILatencyItem:
    provider: str
    model: str
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    threshold_p95_ms: float
    degraded: bool


@dataclass
class AILatencyReport:
    total_models_measured: int
    all_within_thresholds: bool
    latencies: List[AILatencyItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIQuotaItem:
    provider: str
    requests_per_minute_limit: int
    current_rpm_utilization_pct: float
    tokens_per_minute_limit: int
    current_tpm_utilization_pct: float
    rate_limit_429_count: int
    backoff_strategy_verified: bool
    queue_preserved_under_burst: bool


@dataclass
class AIQuotaReport:
    total_providers_tracked: int
    quota_exhaustion_detected: bool
    rate_limit_handling_verified: bool
    quotas: List[AIQuotaItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIResponseIntegrityItem:
    sample_id: str
    provider: str
    schema_compliant: bool
    json_valid: bool
    required_fields_present: bool
    confidence_score: float
    hallucination_detected: bool
    passed: bool


@dataclass
class AIResponseIntegrityReport:
    total_samples_evaluated: int
    schema_compliance_rate_pct: float
    avg_confidence_score: float
    invalid_response_rate_pct: float
    samples: List[AIResponseIntegrityItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AITimeoutItem:
    scenario: str
    configured_timeout_seconds: float
    elapsed_seconds: float
    timeout_triggered: bool
    cancellation_clean: bool
    task_state_preserved: bool
    retry_policy_evaluated: bool


@dataclass
class AITimeoutReport:
    total_timeout_tests: int
    all_timeouts_handled_safely: bool
    tests: List[AITimeoutItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIFailureClassificationItem:
    error_signature: str
    http_status_code: int
    category: AIFailureCategory
    prescribed_action: str
    queue_impact: str
    operator_alert_required: bool


@dataclass
class AIFailureClassificationReport:
    total_failure_patterns_classified: int
    all_categories_covered: bool
    classifications: List[AIFailureClassificationItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIDegradedModeReport:
    graceful_degradation_active: bool
    task_persistence_verified: bool
    fallback_routing_ready: bool
    user_alerting_verified: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIFailoverItem:
    failover_id: str
    from_provider: str
    to_provider: str
    trigger_reason: str
    failover_latency_ms: float
    success_rate_pct: float
    data_consistency_verified: bool


@dataclass
class AIFailoverReport:
    total_failover_scenarios: int
    avg_failover_latency_ms: float
    failovers: List[AIFailoverItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIMonitoringReport:
    prometheus_metrics_exposed: int
    alert_rules_configured: int
    opentelemetry_traces_active: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AISecurityCheckItem:
    check_id: str
    name: str
    api_key_redacted: bool
    prompt_sanitized: bool
    pii_scrubbed: bool
    passed: bool
    details: str


@dataclass
class AISecurityReport:
    total_checks: int
    sensitive_data_exposed: bool
    checks: List[AISecurityCheckItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIFailureSimulationItem:
    scenario_id: str
    name: str
    injected_fault: str
    expected_behavior: str
    observed_behavior: str
    recovered_successfully: bool
    passed: bool


@dataclass
class AIFailureSimulationReport:
    total_simulations: int
    all_recovered: bool
    simulations: List[AIFailureSimulationItem]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIHealthQualityScorecard:
    availability_score: float      # Weight 20%
    authentication_score: float    # Weight 15%
    latency_score: float           # Weight 15%
    failure_handling_score: float  # Weight 20%
    response_quality_score: float  # Weight 15%
    security_score: float          # Weight 15%
    overall_score: float           # Composite 0 - 100
    certification_tier: AIQualityCertificationTier
    certification_verdict: str     # CERTIFIED / CONDITIONAL_APPROVAL / REJECTED
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)
