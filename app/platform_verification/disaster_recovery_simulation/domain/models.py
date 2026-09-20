"""
Domain Models for Enterprise Disaster Recovery Simulation Framework (Part 3G.3).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional


class DisasterScenarioType(str, Enum):
    DATABASE_LOSS = "DATABASE_LOSS"
    DATABASE_CORRUPTION = "DATABASE_CORRUPTION"
    STORAGE_FAILURE = "STORAGE_FAILURE"
    COMPLETE_ENVIRONMENT_DESTRUCTION = "COMPLETE_ENVIRONMENT_DESTRUCTION"
    CASCADE_DEPENDENCY_FAILURE = "CASCADE_DEPENDENCY_FAILURE"


class ChaosExperimentType(str, Enum):
    CONTAINER_TERMINATION = "CONTAINER_TERMINATION"
    NETWORK_PARTITION = "NETWORK_PARTITION"
    RESOURCE_EXHAUSTION = "RESOURCE_EXHAUSTION"


class ResilienceCertificationLevel(str, Enum):
    LEVEL_4_MISSION_CRITICAL = "Level 4 — Mission Critical Ready"  # 95 - 100
    LEVEL_3_ENTERPRISE_READY = "Level 3 — Enterprise Ready"        # 90 - 94
    LEVEL_2_PRODUCTION_READY = "Level 2 — Production Ready"        # 80 - 89
    LEVEL_1_NEEDS_IMPROVEMENT = "Level 1 — Needs Improvement"      # < 80


@dataclass
class IncidentTimelineEvent:
    timestamp_iso: str
    phase: str  # DISASTER_INJECTED, DETECTED, MITIGATION_INITIATED, SERVICE_RESTORED, FULLY_OPERATIONAL
    description: str
    elapsed_seconds_from_start: float


@dataclass
class ScenarioSimulationResult:
    scenario_type: DisasterScenarioType
    scenario_name: str
    description: str
    simulation_passed: bool
    measured_rto_seconds: float
    measured_rpo_seconds: float
    data_consistency_passed: bool
    schema_intact: bool
    relations_preserved: bool
    timeline: List[IncidentTimelineEvent] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChaosExperimentResult:
    experiment_type: ChaosExperimentType
    experiment_name: str
    target_component: str
    injection_successful: bool
    recovery_detected: bool
    recovery_duration_seconds: float
    self_healing_verified: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IncidentDetectionResult:
    incident_type: str
    detection_successful: bool
    measured_mttd_seconds: float
    target_mttd_seconds: float
    mttd_met: bool
    monitoring_source: str  # Prometheus, Blackbox, CloudWatch
    alert_channel: str      # PagerDuty, Slack
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PostRecoveryValidationReport:
    api_health_verified: bool
    workers_active: bool
    frontend_reachable: bool
    database_migrations_intact: bool
    database_foreign_keys_intact: bool
    document_hashes_matched: bool
    agent_workflows_resumed: bool
    overall_validation_passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TabletopExerciseResult:
    exercise_name: str
    scenario_evaluated: str
    incident_response_team_notified: bool
    recovery_decision_time_minutes: float
    decision_quality_score: float
    communication_protocols_validated: bool
    passed: bool
    notes: List[str] = field(default_factory=list)


@dataclass
class ContinuousDRTestingSchedule:
    weekly_health_recovery: Dict[str, Any]
    monthly_restore_simulation: Dict[str, Any]
    quarterly_full_disaster_simulation: Dict[str, Any]
    annual_environment_recovery: Dict[str, Any]
    schedule_active: bool
    next_scheduled_drill_iso: str


@dataclass
class ResilienceScorecard:
    recovery_success_score: float     # Weight 30%
    rto_performance_score: float      # Weight 20%
    rpo_compliance_score: float       # Weight 20%
    automation_score: float           # Weight 15%
    detection_score: float            # Weight 10%
    documentation_score: float        # Weight 5%
    composite_score: float            # 0 - 100
    certification_level: ResilienceCertificationLevel
    passed: bool
    ci_cd_deployment_approved: bool
    measured_rto_minutes: float
    measured_rpo_minutes: float
    measured_mttr_minutes: float
    measured_mttd_minutes: float
    metadata: Dict[str, Any] = field(default_factory=dict)
