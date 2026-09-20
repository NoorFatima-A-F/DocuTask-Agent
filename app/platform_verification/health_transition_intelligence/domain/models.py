"""
Domain Models for Health State Transition & Service Recovery Intelligence (Part 3H.3.3).
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional


class HealthState(str, Enum):
    STARTING = "STARTING"
    READY = "READY"
    DEGRADED = "DEGRADED"
    NOT_READY = "NOT_READY"
    RECOVERING = "RECOVERING"


class DegradationSeverity(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"


class RecoveryActionType(str, Enum):
    RESTART_WORKER = "RESTART_WORKER"
    PAUSE_QUEUE = "PAUSE_QUEUE"
    THROTTLE_TRAFFIC = "THROTTLE_TRAFFIC"
    ENABLE_FALLBACK = "ENABLE_FALLBACK"
    RECONNECT_POOL = "RECONNECT_POOL"
    NONE = "NONE"


class HealthTier(str, Enum):
    FAILED = "Failed"                                         # < 80
    NEEDS_IMPROVEMENT = "Improvement Required"               # 80 - 89
    PRODUCTION_READY = "Production Ready"                     # 90 - 94
    ENTERPRISE_READY = "Enterprise Health Intelligence Ready"  # 95 - 100


@dataclass
class HealthEvent:
    event_id: str
    service_name: str
    previous_state: HealthState
    new_state: HealthState
    reason: str
    trigger_signal: str
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthSignal:
    source: str
    metric_name: str
    value: float
    unit: str
    timestamp: str
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class DegradationReport:
    condition: str
    severity: DegradationSeverity
    confidence: float
    slope_rate: float
    detected_metric: str
    reason: str
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FlappingReport:
    service: str
    flapping_detected: bool
    transition_count: int
    window_seconds: int
    dampening_active: bool
    suppressed_restart_count: int
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CascadingProtectionReport:
    circuit_breaker_state: str  # CLOSED, OPEN, HALF_OPEN
    consecutive_failures: int
    rate_dampened: bool
    fallback_engaged: bool
    cascading_prevented: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RecoveryValidationReport:
    service: str
    initial_state: HealthState
    recovery_state_reached: bool
    final_state: HealthState
    all_prerequisites_met: bool
    recovery_duration_seconds: float
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IncidentTimelineEntry:
    timestamp: str
    phase: str
    event: str
    impact: str
    action_taken: str


@dataclass
class IncidentTimeline:
    incident_id: str
    service_name: str
    start_time: str
    end_time: str
    root_cause: str
    total_duration_seconds: float
    timeline_entries: List[IncidentTimelineEntry]
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AlertItem:
    alert_name: str
    severity: str  # CRITICAL, WARNING, RECOVERY
    service: str
    summary: str
    description: str
    timestamp: str


@dataclass
class AlertingReport:
    total_alerts_generated: int
    critical_alerts_count: int
    warning_alerts_count: int
    recovery_alerts_count: int
    alerts: List[AlertItem]
    prometheus_alertmanager_compatible: bool
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StateMachineReport:
    total_states: int
    states: List[str]
    transition_matrix_valid: bool
    all_deterministic: bool
    total_transitions_logged: int
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulationScenarioResult:
    scenario_id: str
    name: str
    injected_condition: str
    transition_sequence: List[str]
    recovery_action_executed: str
    final_state: HealthState
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimulationReport:
    total_scenarios: int
    passed_scenarios: int
    all_scenarios_passed: bool
    scenarios: List[SimulationScenarioResult]
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthIntelligenceScorecard:
    state_accuracy_score: float         # Weight 25%
    transition_logic_score: float       # Weight 20%
    failure_detection_score: float      # Weight 20%
    recovery_validation_score: float    # Weight 15%
    alerting_score: float               # Weight 10%
    evidence_quality_score: float       # Weight 10%
    overall_score: float                # Composite 0 - 100
    certification_tier: HealthTier
    certification_verdict: str          # CERTIFIED / REJECTED
    passed: bool
    details: Dict[str, Any] = field(default_factory=dict)
