"""
Domain Models for Enterprise Verification Environment Strategy & Infrastructure Architecture.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import hashlib
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field
import uuid


class EnvironmentClassification(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    INTEGRATION = "INTEGRATION"
    STAGING = "STAGING"
    PRODUCTION_SHADOW = "PRODUCTION_SHADOW"
    PRODUCTION = "PRODUCTION"
    CHAOS = "CHAOS"
    SECURITY_LAB = "SECURITY_LAB"
    RESEARCH = "RESEARCH"


class EnvironmentHealthState(str, Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    DEGRADED = "DEGRADED"
    CRITICAL = "CRITICAL"
    UNAVAILABLE = "UNAVAILABLE"


class EnvironmentSecurityLevel(str, Enum):
    LOCAL_PERMISSIVE = "LOCAL_PERMISSIVE"
    ISOLATED_TEST = "ISOLATED_TEST"
    STAGING_CONTROLLED = "STAGING_CONTROLLED"
    SHADOW_ANONYMIZED = "SHADOW_ANONYMIZED"
    PRODUCTION_HARDENED = "PRODUCTION_HARDENED"
    ADVERSARIAL_SANDBOX = "ADVERSARIAL_SANDBOX"


class DataClassificationPolicy(str, Enum):
    SYNTHETIC_ONLY = "SYNTHETIC_ONLY"
    BENCHMARK_CURATED = "BENCHMARK_CURATED"
    REGRESSION_HISTORICAL = "REGRESSION_HISTORICAL"
    PRODUCTION_ANONYMIZED = "PRODUCTION_ANONYMIZED"
    PRODUCTION_LIVE = "PRODUCTION_LIVE"


class DeploymentStrategyType(str, Enum):
    BLUE_GREEN = "BLUE_GREEN"
    CANARY = "CANARY"
    ROLLING = "ROLLING"
    RECREATE = "RECREATE"


class ChaosFailureType(str, Enum):
    PROCESS_KILL = "PROCESS_KILL"
    LATENCY_INJECTION = "LATENCY_INJECTION"
    PACKET_LOSS = "PACKET_LOSS"
    CPU_PRESSURE = "CPU_PRESSURE"
    MEMORY_PRESSURE = "MEMORY_PRESSURE"
    DEPENDENCY_OUTAGE = "DEPENDENCY_OUTAGE"
    STORAGE_EXHAUSTION = "STORAGE_EXHAUSTION"


class SecurityAttackVector(str, Enum):
    PROMPT_INJECTION = "PROMPT_INJECTION"
    JAILBREAK_EVASION = "JAILBREAK_EVASION"
    PII_EXTRACTION = "PII_EXTRACTION"
    PRIVILEGE_ESCALATION = "PRIVILEGE_ESCALATION"
    API_FUZZING = "API_FUZZING"
    DENIAL_OF_SERVICE = "DENIAL_OF_SERVICE"


class EnvironmentDefinition(BaseModel):
    environment_id: str
    name: str
    classification: EnvironmentClassification
    purpose: str
    security_level: EnvironmentSecurityLevel
    data_policy: DataClassificationPolicy
    deployment_strategy: DeploymentStrategyType = DeploymentStrategyType.BLUE_GREEN
    min_cpu_cores: int = 4
    min_memory_gb: float = 16.0
    is_ephemeral: bool = False
    allowed_verification_types: List[str] = Field(default_factory=lambda: ["ALL"])
    network_isolation_enabled: bool = True
    audit_logging_strict: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EnvironmentProvisioningRequest(BaseModel):
    request_id: str = Field(default_factory=lambda: f"req_{uuid.uuid4().hex[:8]}")
    environment_classification: EnvironmentClassification
    target_cluster: str = "k8s-platform-us-central1"
    config_overrides: Dict[str, Any] = Field(default_factory=dict)
    requester: str = "SRE Automation Platform"
    requested_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EnvironmentProvisioningResult(BaseModel):
    provisioning_id: str = Field(default_factory=lambda: f"prv_{uuid.uuid4().hex[:8]}")
    environment_id: str
    classification: EnvironmentClassification
    is_success: bool
    status: str = "READY"
    endpoint_url: str
    allocated_resources: Dict[str, Any] = Field(default_factory=dict)
    infrastructure_digest: str
    provisioned_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ChaosExperimentSpec(BaseModel):
    experiment_id: str = Field(default_factory=lambda: f"chaos_{uuid.uuid4().hex[:8]}")
    name: str
    target_component: str
    failure_type: ChaosFailureType
    duration_seconds: int = 30
    intensity_percentage: int = 50
    latency_ms: Optional[int] = None
    expected_recovery_time_seconds: int = 60
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ChaosExperimentResult(BaseModel):
    experiment_id: str
    target_component: str
    failure_type: ChaosFailureType
    is_resilient: bool
    recovery_time_ms: float
    blast_radius_contained: bool
    observed_behavior: str
    evidence_package_hash: str
    completed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SecurityLabExperimentSpec(BaseModel):
    experiment_id: str = Field(default_factory=lambda: f"sec_{uuid.uuid4().hex[:8]}")
    attack_vector: SecurityAttackVector
    target_endpoint: str
    payload: str
    expected_block: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SecurityLabExperimentResult(BaseModel):
    experiment_id: str
    attack_vector: SecurityAttackVector
    is_blocked: bool
    vulnerability_detected: bool
    leak_detected: bool
    sanitized_response: str
    evidence_hash: str
    completed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EnvironmentQualityGateResult(BaseModel):
    gate_id: str = Field(default_factory=lambda: f"gate_{uuid.uuid4().hex[:8]}")
    from_environment: EnvironmentClassification
    to_environment: EnvironmentClassification
    is_passed: bool
    score: float
    evaluated_criteria: Dict[str, bool] = Field(default_factory=dict)
    blockers: List[str] = Field(default_factory=list)
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DeploymentPromotionRecord(BaseModel):
    promotion_id: str = Field(default_factory=lambda: f"prm_{uuid.uuid4().hex[:8]}")
    version: str
    from_environment: EnvironmentClassification
    to_environment: EnvironmentClassification
    strategy: DeploymentStrategyType
    is_successful: bool
    gate_result: EnvironmentQualityGateResult
    executed_by: str = "Release Orchestration Pipeline"
    executed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EnvironmentMetadataRecord(BaseModel):
    environment_id: str
    classification: EnvironmentClassification
    version: str = "1.0.0"
    configuration_hash: str
    infrastructure_version: str
    deployment_version: str
    owner: str = "Enterprise Platform SRE"
    health_state: EnvironmentHealthState = EnvironmentHealthState.HEALTHY
    active_workloads_count: int = 0
    last_validated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
