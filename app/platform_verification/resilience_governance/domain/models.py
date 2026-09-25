"""
Domain Models for Disaster Recovery Governance & Operational Resilience Framework (Part 3G.4).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any


class ResilienceMaturityTier(str, Enum):
    LEVEL_0_UNDEFINED = "Level 0 — Undefined"
    LEVEL_1_DOCUMENTED = "Level 1 — Documented"
    LEVEL_2_TESTED = "Level 2 — Tested"
    LEVEL_3_AUTOMATED = "Level 3 — Automated"
    LEVEL_4_RESILIENT = "Level 4 — Resilient"      # >= 90%
    LEVEL_5_ADAPTIVE = "Level 5 — Adaptive"        # >= 95%


class GovernanceRiskSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class ComponentOwnershipItem:
    component_name: str
    owner_role: str
    team_name: str
    escalation_tier_1: str
    escalation_tier_2: str
    runbook_reference: str
    status: str = "OWNED"


@dataclass
class OwnershipValidationReport:
    total_components: int
    owned_components: int
    missing_owner: int
    components: List[ComponentOwnershipItem] = field(default_factory=list)
    passed: bool = True
    status: str = "PASS"
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PolicyValidationReport:
    policies_evaluated: int
    backup_policy_compliant: bool
    restore_policy_compliant: bool
    incident_policy_compliant: bool
    testing_policy_compliant: bool
    all_policies_enforced: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChangeImpactItem:
    change_type: str  # service_addition, schema_migration, dependency_update
    resource_name: str
    impact_level: str
    recovery_dependency_missing: bool
    remediation_required: str


@dataclass
class RecoveryChangeImpactReport:
    total_changes_scanned: int
    uncovered_dependencies_count: int
    changes: List[ChangeImpactItem] = field(default_factory=list)
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentationDriftItem:
    doc_file: str
    element_type: str
    documented_state: str
    actual_system_state: str
    drift_detected: bool
    remediation: str


@dataclass
class DocumentationDriftReport:
    total_documents_scanned: int
    drifts_detected_count: int
    drift_items: List[DocumentationDriftItem] = field(default_factory=list)
    passed: bool = True
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResilienceMaturityScore:
    maturity_level: ResilienceMaturityTier
    maturity_score: float  # 0 - 100
    level_numeric: int     # 0 to 5
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    passed: bool = True
    target_tier: ResilienceMaturityTier = ResilienceMaturityTier.LEVEL_4_RESILIENT
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IncidentRecord:
    incident_id: str
    severity: str
    downtime_minutes: float
    root_cause: str
    corrective_action: str
    postmortem_completed: bool
    preventive_controls_implemented: bool


@dataclass
class PostmortemSectionReport:
    summary_valid: bool
    timeline_valid: bool
    root_cause_valid: bool
    impact_valid: bool
    action_items_valid: bool
    postmortem_quality_score: float
    passed: bool
    action_items: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ContinuousResilienceMetricsReport:
    rto_average_minutes: float
    rpo_average_minutes: float
    mttr_average_minutes: float
    restore_success_rate_pct: float
    open_risks_count: int
    overdue_actions_count: int
    metrics_health_verdict: str
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GovernanceScorecard:
    ownership_score: float           # Weight 20%
    policy_governance_score: float   # Weight 15%
    change_drift_score: float        # Weight 20%
    maturity_score: float            # Weight 20%
    incident_learning_score: float   # Weight 15%
    audit_readiness_score: float     # Weight 10%
    overall_governance_score: float  # Composite 0 - 100
    certification_status: str        # CERTIFIED / REJECTED
    ci_cd_deployment_approved: bool
    passed: bool
    evaluation_metadata: Dict[str, Any] = field(default_factory=dict)
