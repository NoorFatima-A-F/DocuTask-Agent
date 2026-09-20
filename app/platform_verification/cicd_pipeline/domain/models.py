"""
Domain models for Enterprise Continuous Verification CI/CD Pipeline (PART 7).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
import hashlib
import json
from typing import Any, Dict, List, Optional, Set, Tuple, Union


class PipelineStageType(str, Enum):
    STAGE_1_SOURCE_VALIDATION = "STAGE_1_SOURCE_VALIDATION"
    STAGE_2_BUILD_VERIFICATION = "STAGE_2_BUILD_VERIFICATION"
    STAGE_3_UNIT_VERIFICATION = "STAGE_3_UNIT_VERIFICATION"
    STAGE_4_COMPONENT_VERIFICATION = "STAGE_4_COMPONENT_VERIFICATION"
    STAGE_5_INTEGRATION_VERIFICATION = "STAGE_5_INTEGRATION_VERIFICATION"
    STAGE_6_AI_EVALUATION = "STAGE_6_AI_EVALUATION"
    STAGE_7_SECURITY_VERIFICATION = "STAGE_7_SECURITY_VERIFICATION"
    STAGE_8_PERFORMANCE_VERIFICATION = "STAGE_8_PERFORMANCE_VERIFICATION"
    STAGE_9_CERTIFICATION_VALIDATION = "STAGE_9_CERTIFICATION_VALIDATION"


class StageExecutionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    BLOCKED = "BLOCKED"


class PipelineExecutionStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ROLLBACK_TRIGGERED = "ROLLBACK_TRIGGERED"


class PipelineChangeType(str, Enum):
    CODE = "CODE"
    PROMPT = "PROMPT"
    MODEL = "MODEL"
    DATASET = "DATASET"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    CONFIGURATION = "CONFIGURATION"
    DOCUMENTATION = "DOCUMENTATION"


class ChangeRiskLevel(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class TargetEnvironment(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    INTEGRATION = "INTEGRATION"
    STAGING = "STAGING"
    PRODUCTION_SHADOW = "PRODUCTION_SHADOW"
    PRODUCTION = "PRODUCTION"


class PromotionStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PROMOTED = "PROMOTED"
    ROLLED_BACK = "ROLLED_BACK"


class RollbackTriggerReason(str, Enum):
    QUALITY_DEGRADATION = "QUALITY_DEGRADATION"
    ERROR_SPIKE = "ERROR_SPIKE"
    SECURITY_FAILURE = "SECURITY_FAILURE"
    PERFORMANCE_REGRESSION = "PERFORMANCE_REGRESSION"
    MANUAL_OPERATOR = "MANUAL_OPERATOR"


@dataclass
class ChangedFile:
    """Individual file change in commit/PR."""
    file_path: str
    change_type: PipelineChangeType
    lines_added: int = 0
    lines_deleted: int = 0


@dataclass
class PipelineChangeContext:
    """Analyzed change payload driving adaptive verification."""
    change_id: str
    commit_sha: str
    branch: str
    author: str
    primary_change_type: PipelineChangeType
    changed_files: List[ChangedFile]
    risk_level: ChangeRiskLevel
    affected_components: List[str]
    required_stages: List[PipelineStageType]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class StageExecutionRecord:
    """Execution status and metric output of a single pipeline stage."""
    stage_id: str
    stage_type: PipelineStageType
    stage_name: str
    status: StageExecutionStatus
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    duration_seconds: float = 0.0
    metrics: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    artifacts: List[str] = field(default_factory=list)


@dataclass
class PipelineExecutionRecord:
    """Full lifecycle execution trace of a continuous verification pipeline run."""
    pipeline_id: str
    pipeline_name: str
    target_environment: TargetEnvironment
    change_context: PipelineChangeContext
    status: PipelineExecutionStatus
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    duration_seconds: float = 0.0
    stage_records: List[StageExecutionRecord] = field(default_factory=list)
    evidence_package_id: Optional[str] = None
    certification_id: Optional[str] = None
    deployment_decision: str = "PENDING"
    explainable_summary: List[str] = field(default_factory=list)


@dataclass
class PipelineArtifactMetadata:
    """Artifact stored and verified in artifact registry."""
    artifact_id: str
    name: str
    version: str
    artifact_type: str  # "BUILD" | "MODEL" | "CONTAINER" | "DATASET"
    sha256_checksum: str
    size_bytes: int
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    verified: bool = False
    certification_status: str = "PENDING"
    uri: str = ""


@dataclass
class SupplyChainSecurityReport:
    """Supply chain security scan report."""
    scan_id: str
    pipeline_id: str
    dependency_vulnerabilities_count: int = 0
    license_violations_count: int = 0
    container_cve_critical_count: int = 0
    exposed_secrets_count: int = 0
    sbom_signature_valid: bool = True
    passed: bool = True
    findings: List[str] = field(default_factory=list)


@dataclass
class EnvironmentPromotionRecord:
    """Audit record for environment promotion progression."""
    promotion_id: str
    pipeline_id: str
    source_env: TargetEnvironment
    target_env: TargetEnvironment
    status: PromotionStatus
    certification_level_required: str
    actual_certification_level: str
    approved_by: str
    promoted_at: Optional[str] = None
    rejection_reason: Optional[str] = None


@dataclass
class RollbackEventRecord:
    """Audit record of automated deployment rollback."""
    rollback_id: str
    pipeline_id: str
    target_environment: TargetEnvironment
    trigger_reason: RollbackTriggerReason
    previous_stable_version: str
    failed_version: str
    incident_evidence_id: str
    triggered_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    invalidated_certification_id: Optional[str] = None
    status: str = "COMPLETED"


@dataclass
class PipelineObservabilityMetrics:
    """Consolidated CI/CD pipeline reliability and DORA metrics."""
    total_pipeline_runs: int = 0
    successful_runs: int = 0
    failed_runs: int = 0
    avg_duration_seconds: float = 0.0
    deployment_frequency_per_day: float = 0.0
    change_failure_rate: float = 0.0
    rollback_frequency: int = 0
    mean_time_to_restore_minutes: float = 0.0
    ai_regression_rate: float = 0.0
