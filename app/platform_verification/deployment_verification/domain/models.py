"""
Domain models for Part 3D: Enterprise Deployment & Environment Verification Framework.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any
from datetime import datetime, timezone


class DeploymentCertificationTier(str, Enum):
    ENTERPRISE_DEPLOYMENT_READY = "ENTERPRISE_DEPLOYMENT_READY"
    PRODUCTION_READY = "PRODUCTION_READY"
    IMPROVEMENT_REQUIRED = "IMPROVEMENT_REQUIRED"
    FAILED = "FAILED"


DeploymentCertificationTier.__test__ = False


class DeploymentStrategy(str, Enum):
    ROLLING = "ROLLING"
    BLUE_GREEN = "BLUE_GREEN"
    CANARY = "CANARY"


class EnvironmentStage(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"


class RollbackTrigger(str, Enum):
    HEALTH_CHECK_FAILURE = "HEALTH_CHECK_FAILURE"
    MIGRATION_FAILURE = "MIGRATION_FAILURE"
    METRIC_ANOMALY = "METRIC_ANOMALY"
    MANUAL_ABORT = "MANUAL_ABORT"


@dataclass
class BuildReproducibilityReport:
    commit_sha: str
    image_digest: str
    is_reproducible: bool
    build_metadata: Dict[str, Any] = field(default_factory=dict)
    status: str = "PASS"


@dataclass
class DependencyLockReport:
    total_dependencies: int
    unpinned_dependencies: List[str] = field(default_factory=list)
    lock_files_verified: List[str] = field(default_factory=list)
    is_strictly_pinned: bool = True
    status: str = "PASS"


@dataclass
class ArtifactSecurityReport:
    image_name: str
    is_signed: bool
    is_immutable: bool
    vulnerability_scan_passed: bool
    critical_cves: int = 0
    status: str = "PASS"


@dataclass
class EnvironmentDriftReport:
    compared_environments: List[str] = field(default_factory=list)
    drift_items: List[str] = field(default_factory=list)
    missing_variables: List[str] = field(default_factory=list)
    parity_score: float = 100.0
    status: str = "PASS"


@dataclass
class IacValidationReport:
    framework: str
    is_valid: bool
    idempotent_recreation_verified: bool
    validation_issues: List[str] = field(default_factory=list)
    status: str = "PASS"


@dataclass
class DeploymentAutomationReport:
    total_steps: int
    automated_steps: int
    manual_steps_detected: List[str] = field(default_factory=list)
    automation_percentage: float = 100.0
    status: str = "PASS"


@dataclass
class ReleaseStrategyReport:
    strategy_tested: DeploymentStrategy
    zero_dropped_requests: bool = True
    canary_traffic_split_verified: bool = True
    status: str = "PASS"


@dataclass
class MigrationVerificationReport:
    forward_migration_verified: bool = True
    backward_compatibility_verified: bool = True
    rollback_tested: bool = True
    duration_seconds: float = 2.4
    status: str = "PASS"


@dataclass
class RollbackVerificationReport:
    rollback_trigger: RollbackTrigger
    rollback_successful: bool = True
    rollback_duration_seconds: float = 3.5
    data_loss_detected: bool = False
    status: str = "PASS"


@dataclass
class SecretDeploymentReport:
    secrets_in_codebase: List[str] = field(default_factory=list)
    secrets_in_build_artifacts: List[str] = field(default_factory=list)
    runtime_injection_verified: bool = True
    status: str = "PASS"


@dataclass
class ZeroDowntimeReport:
    simulated_rps: int = 100
    total_requests_sent: int = 1000
    failed_requests: int = 0
    availability_pct: float = 100.0
    status: str = "PASS"


@dataclass
class DeploymentObservabilityReport:
    lifecycle_logs_verified: bool = True
    metrics_collected: bool = True
    git_to_deployment_trace_verified: bool = True
    status: str = "PASS"


@dataclass
class DeploymentCertificationReport:
    reproducibility_score: float
    automation_score: float
    security_score: float
    reliability_score: float
    rollback_capability_score: float
    environment_consistency_score: float
    composite_score: float
    tier: DeploymentCertificationTier
    evaluation_timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class DeploymentVerificationEvidencePackage:
    package_id: str
    commit_sha: str
    scorecard: DeploymentCertificationReport
    build_report: BuildReproducibilityReport
    artifact_report: ArtifactSecurityReport
    environment_report: EnvironmentDriftReport
    iac_report: IacValidationReport
    automation_report: DeploymentAutomationReport
    release_report: ReleaseStrategyReport
    migration_report: MigrationVerificationReport
    rollback_report: RollbackVerificationReport
    secret_report: SecretDeploymentReport
    zero_downtime_report: ZeroDowntimeReport
    observability_report: DeploymentObservabilityReport
    package_sha256: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
