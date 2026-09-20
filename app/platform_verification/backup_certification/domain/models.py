"""
Domain Models for Enterprise Backup Certification Framework (Part 3G.2G).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional


class BackupCertificationTier(str, Enum):
    LEVEL_1_BASIC_READY = "Level 1 — Basic Backup Ready"             # 70 - 79
    LEVEL_2_PRODUCTION_READY = "Level 2 — Production Backup Ready"   # 80 - 89
    LEVEL_3_ENTERPRISE_READY = "Level 3 — Enterprise Backup Ready"   # 90 - 94
    LEVEL_4_MISSION_CRITICAL_READY = "Level 4 — Mission Critical Ready" # 95 - 100
    UNCERTIFIED_FAILED = "Uncertified — Failed"                     # < 70


class RiskSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class VerificationScheduleFrequency(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"


@dataclass
class CollectedBackupEvidence:
    backup_inventory: Dict[str, Any]
    restore_test_report: Dict[str, Any]
    integrity_report: Dict[str, Any]
    security_validation: Dict[str, Any]
    config_secrets_validation: Dict[str, Any]
    timestamp_iso: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CompletenessEvaluation:
    database_verified: bool
    documents_verified: bool
    ocr_outputs_verified: bool
    extraction_results_verified: bool
    metadata_verified: bool
    configuration_verified: bool
    secrets_verified: bool
    infrastructure_state_verified: bool
    completeness_score: float
    passed: bool
    missing_assets: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IntegrityEvaluation:
    checksum_validation: str  # PASS / FAIL
    corruption_detected: bool
    bit_flip_resilience_verified: bool
    digital_signatures_valid: bool
    integrity_score: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RestoreCapabilityEvaluation:
    restore_success: bool
    restore_duration_seconds: float
    rto_target_seconds: float
    rto_met: bool
    recovered_data_accuracy_pct: float
    dependency_recovery_verified: bool
    restore_capability_score: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OperationalReadinessEvaluation:
    automation_enabled: bool
    monitoring_configured: bool
    alerts_configured: bool
    documentation_complete: bool
    ownership_assigned: bool
    operational_readiness_score: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RTORPOCertification:
    measured_rto_minutes: float
    target_rto_minutes: float
    rto_status: str
    measured_rpo_minutes: float
    target_rpo_minutes: float
    rpo_status: str
    rto_rpo_certified: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BackupPolicyEvaluation:
    database_frequency_compliant: bool
    database_retention_compliant: bool
    documents_frequency_compliant: bool
    documents_retention_compliant: bool
    restore_test_frequency_compliant: bool
    policy_compliance_score: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BackupRiskItem:
    risk: str
    severity: RiskSeverity
    category: str
    impact: str
    recommendation: str
    remediation_owner: str
    mitigated: bool = False


@dataclass
class BackupRiskRegister:
    total_risks_identified: int
    critical_risks_count: int
    high_risks_count: int
    medium_risks_count: int
    low_risks_count: int
    risks: List[BackupRiskItem] = field(default_factory=list)
    passed: bool = True
    summary: str = ""


@dataclass
class ContinuousVerificationSchedule:
    daily_existence_check: Dict[str, Any]
    weekly_integrity_validation: Dict[str, Any]
    monthly_restore_test: Dict[str, Any]
    quarterly_disaster_simulation: Dict[str, Any]
    schedule_active: bool
    last_refresh_iso: str
    next_scheduled_refresh_iso: str


@dataclass
class BackupReadinessScorecard:
    backup_completeness: float    # Weight: 20%
    restore_success: float        # Weight: 25%
    integrity: float              # Weight: 15%
    security: float               # Weight: 15%
    automation: float             # Weight: 10%
    monitoring: float             # Weight: 10%
    documentation: float          # Weight: 5%
    overall_score: float          # Sum of weighted scores (0 - 100)
    certification_level: BackupCertificationTier
    passed: bool
    ci_cd_deployment_approved: bool
    evaluation_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BackupHealthDashboardData:
    system_name: str
    certification_tier: str
    overall_score: float
    backup_health: Dict[str, Any]
    recovery_metrics: Dict[str, Any]
    storage_metrics: Dict[str, Any]
    alerts_status: List[Dict[str, Any]]
    last_certified_timestamp: str
