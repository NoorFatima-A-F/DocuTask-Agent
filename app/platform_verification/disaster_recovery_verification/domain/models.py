"""
Domain models for Enterprise Disaster Recovery Architecture Verification (Part 3G.1).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional


class DRMaturityLevel(str, Enum):
    LEVEL_0_NO_RECOVERY = "LEVEL_0_NO_RECOVERY"
    LEVEL_1_BACKUP_EXISTS = "LEVEL_1_BACKUP_EXISTS"
    LEVEL_2_RESTORE_VERIFIED = "LEVEL_2_RESTORE_VERIFIED"
    LEVEL_3_AUTOMATED_RECOVERY = "LEVEL_3_AUTOMATED_RECOVERY"
    LEVEL_4_TESTED_DR = "LEVEL_4_TESTED_DR"
    LEVEL_5_RESILIENT_ARCH = "LEVEL_5_RESILIENT_ARCH"


class ComponentTier(str, Enum):
    TIER_0_MISSION_CRITICAL = "TIER_0_MISSION_CRITICAL"  # Complete business outage (Postgres, Storage, Auth, Agent State)
    TIER_1_CRITICAL = "TIER_1_CRITICAL"  # Major degradation (Queue, Workers, Knowledge)
    TIER_2_IMPORTANT = "TIER_2_IMPORTANT"  # Analytics, Dashboards
    TIER_3_NON_CRITICAL = "TIER_3_NON_CRITICAL"  # Caches, Temp files


class DRScenarioType(str, Enum):
    DATABASE_DESTRUCTION = "DATABASE_DESTRUCTION"
    STORAGE_LOSS = "STORAGE_LOSS"
    QUEUE_FAILURE = "QUEUE_FAILURE"
    COMPLETE_ENVIRONMENT_LOSS = "COMPLETE_ENVIRONMENT_LOSS"
    CORRUPTED_DEPLOYMENT = "CORRUPTED_DEPLOYMENT"


class DRCertificationTier(str, Enum):
    ENTERPRISE_DR_READY = "ENTERPRISE_DR_READY"  # 95-100
    PRODUCTION_RECOVERY_READY = "PRODUCTION_RECOVERY_READY"  # 90-94
    PARTIAL_RECOVERY_CAPABILITY = "PARTIAL_RECOVERY_CAPABILITY"  # 80-89
    INSUFFICIENT = "INSUFFICIENT"  # < 80


@dataclass
class DRServiceInventory:
    services: List[str]
    critical_components: List[str]
    backup_dependencies: List[str]
    recovery_dependencies: List[str]


@dataclass
class ComponentCriticalityEntry:
    component_name: str
    tier: ComponentTier
    impact_description: str
    recovery_priority: int
    max_tolerable_downtime_minutes: int
    max_tolerable_data_loss_minutes: int


@dataclass
class BusinessImpactAnalysisEntry:
    business_function: str
    impact: str
    max_downtime: str
    max_data_loss: str
    recovery_priority: int


@dataclass
class RecoveryDependencyGraph:
    topological_order: List[str]
    edges: Dict[str, List[str]]
    valid_order: bool


@dataclass
class BackupPolicy:
    component: str
    backup_interval_minutes: int
    retention_days: int
    automated_restore: bool
    checksum_validation: bool


@dataclass
class DataRecoveryValidationReport:
    original_sha256: str
    recovered_sha256: str
    integrity_verified: bool
    expected_document_count: int
    recovered_document_count: int
    completeness_verified: bool
    referential_consistency_verified: bool
    tenant_isolation_preserved: bool
    passed: bool


@dataclass
class DRTestScenarioResult:
    __test__ = False
    scenario: DRScenarioType
    rto_seconds: float
    rpo_seconds: float
    data_loss_detected: bool
    status: str
    automated_steps_percent: float


@dataclass
class DRSecurityValidationReport:
    backup_encryption_at_rest_verified: bool
    backup_encryption_in_transit_verified: bool
    unauthorized_access_prevented: bool
    secret_exposure_prevented: bool
    backup_poisoning_rejected: bool
    passed: bool


@dataclass
class DRCertificationScorecard:
    recovery_capability_score: float  # 30%
    backup_reliability_score: float   # 20%
    data_integrity_score: float       # 20%
    automation_score: float           # 15%
    security_score: float             # 10%
    documentation_score: float        # 5%
    composite_score: float
    maturity_level: DRMaturityLevel
    certification_tier: DRCertificationTier
    passed: bool


@dataclass
class DRMetadata:
    system: str
    version: str
    commit: str
    environment: str
    timestamp: str
    tester: str
