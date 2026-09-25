"""
Reliability Domain Models & Enums.

Defines the core data structures, severity levels, reliability states,
RTO/RPO objectives, fault domains, and reliability targets for DocuTask Agent.
"""

from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SeverityLevel(str, enum.Enum):
    """Incident & failure severity classification."""
    INFO = "INFO"
    WARNING = "WARNING"
    MINOR = "MINOR"
    MAJOR = "MAJOR"
    CRITICAL = "CRITICAL"
    CATASTROPHIC = "CATASTROPHIC"


class ReliabilityState(str, enum.Enum):
    """Component, service, or regional reliability state lifecycle."""
    OPTIMAL = "OPTIMAL"
    DEGRADED = "DEGRADED"
    FAILING = "FAILING"
    PARTIALLY_FAILED = "PARTIALLY_FAILED"
    RECOVERING = "RECOVERING"
    RECOVERED = "RECOVERED"
    OUTAGE = "OUTAGE"


class FaultDomain(str, enum.Enum):
    """Categorization of failure boundaries."""
    NODE = "NODE"
    RACK = "RACK"
    CLUSTER = "CLUSTER"
    ZONE = "ZONE"
    REGION = "REGION"
    PROVIDER = "PROVIDER"
    SERVICE = "SERVICE"
    STORAGE = "STORAGE"
    DATABASE = "DATABASE"
    QUEUE = "QUEUE"
    AI_PROVIDER = "AI_PROVIDER"


class RetryStrategy(str, enum.Enum):
    """Supported retry backoff algorithms."""
    IMMEDIATE = "IMMEDIATE"
    LINEAR = "LINEAR"
    EXPONENTIAL = "EXPONENTIAL"
    RANDOMIZED_JITTER = "RANDOMIZED_JITTER"
    ADAPTIVE = "ADAPTIVE"


class CircuitBreakerState(str, enum.Enum):
    """Three-state circuit breaker state model."""
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class RTOObjective(BaseModel):
    """Recovery Time Objective specification."""
    target_seconds: float = Field(default=300.0, ge=0.0, description="Target RTO in seconds")
    max_acceptable_seconds: float = Field(default=900.0, ge=0.0, description="Max acceptable RTO before SLA breach")
    critical_path: bool = Field(default=True, description="Whether this component is on the critical path")


class RPOObjective(BaseModel):
    """Recovery Point Objective specification."""
    target_seconds: float = Field(default=60.0, ge=0.0, description="Target RPO in seconds (maximum tolerable data loss)")
    max_acceptable_seconds: float = Field(default=300.0, ge=0.0, description="Max acceptable RPO before SLA breach")
    allow_data_loss: bool = Field(default=False, description="Whether any data loss is tolerable")


class ReliabilityTarget(BaseModel):
    """Composite availability and recovery target."""
    target_id: str = Field(..., description="Unique identifier for target")
    component_name: str = Field(..., description="Target component or service name")
    availability_sla_percent: float = Field(default=99.99, ge=0.0, le=100.0, description="Target SLA uptime percentage")
    rto: RTOObjective = Field(default_factory=RTOObjective)
    rpo: RPOObjective = Field(default_factory=RPOObjective)
    fault_domain: FaultDomain = Field(default=FaultDomain.SERVICE)
    tags: Dict[str, str] = Field(default_factory=dict)


class CircuitBreakerConfig(BaseModel):
    """Circuit breaker configuration parameters."""
    failure_threshold: int = Field(default=5, ge=1, description="Number of consecutive failures to open breaker")
    failure_rate_threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Failure rate threshold (0-1)")
    recovery_timeout_seconds: float = Field(default=30.0, ge=0.1, description="Cooldown seconds before moving to HALF_OPEN")
    half_open_success_threshold: int = Field(default=3, ge=1, description="Consecutive successes in HALF_OPEN to close breaker")
    half_open_max_requests: int = Field(default=5, ge=1, description="Max trial requests allowed in HALF_OPEN")


class RetryPolicyConfig(BaseModel):
    """Retry policy configuration."""
    strategy: RetryStrategy = Field(default=RetryStrategy.EXPONENTIAL)
    max_retries: int = Field(default=3, ge=0)
    initial_interval_seconds: float = Field(default=0.5, ge=0.01)
    max_interval_seconds: float = Field(default=10.0, ge=0.1)
    backoff_multiplier: float = Field(default=2.0, ge=1.0)
    jitter_factor: float = Field(default=0.2, ge=0.0, le=1.0)
    retryable_exceptions: List[str] = Field(default_factory=lambda: ["TimeoutError", "ConnectionError", "ServiceUnavailable"])


class BulkheadConfig(BaseModel):
    """Bulkhead concurrency isolation config."""
    max_concurrent_calls: int = Field(default=100, ge=1)
    max_wait_queue_size: int = Field(default=50, ge=0)
    wait_timeout_seconds: float = Field(default=5.0, ge=0.0)


class ReliabilityPolicy(BaseModel):
    """Unified reliability policy definition."""
    policy_id: str = Field(..., description="Unique policy identifier")
    name: str = Field(..., description="Descriptive policy name")
    enabled: bool = Field(default=True)
    circuit_breaker: CircuitBreakerConfig = Field(default_factory=CircuitBreakerConfig)
    retry_policy: RetryPolicyConfig = Field(default_factory=RetryPolicyConfig)
    bulkhead: BulkheadConfig = Field(default_factory=BulkheadConfig)
    timeout_budget_seconds: float = Field(default=30.0, ge=0.1)
    fallback_enabled: bool = Field(default=True)
    fallback_action: Optional[str] = Field(default="degraded_cache")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ReliabilityTransitionRecord(BaseModel):
    """Audit record for reliability state changes."""
    component_id: str
    from_state: ReliabilityState
    to_state: ReliabilityState
    reason: str
    trigger_source: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
