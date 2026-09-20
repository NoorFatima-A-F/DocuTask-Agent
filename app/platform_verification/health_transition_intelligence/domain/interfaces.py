"""
Abstract interfaces and protocols for Part 3H.3.3.
"""
from typing import Dict, Any, List, Protocol
from app.platform_verification.health_transition_intelligence.domain.models import (
    HealthState,
    HealthEvent,
    DegradationReport,
    FlappingReport,
    CascadingProtectionReport,
    RecoveryValidationReport,
    IncidentTimeline,
    AlertingReport,
    StateMachineReport,
    SimulationReport,
    HealthIntelligenceScorecard,
)


class IHealthStateMachine(Protocol):
    def transition(self, to_state: HealthState, reason: str, trigger_signal: str) -> HealthEvent: ...
    def get_state(self) -> HealthState: ...


class IDegradationAnalyzer(Protocol):
    def analyze_trends(self, metric_series: Dict[str, List[float]]) -> DegradationReport: ...


class IFlappingDetector(Protocol):
    def record_transition(self, from_state: HealthState, to_state: HealthState) -> FlappingReport: ...


class ICascadingProtector(Protocol):
    def report_dependency_failure(self, dep_name: str) -> CascadingProtectionReport: ...


class IRecoveryOrchestrator(Protocol):
    def orchestrate_recovery(self, current_state: HealthState, failed_dep: str) -> RecoveryValidationReport: ...


class IIncidentReconstructor(Protocol):
    def reconstruct_incident(self, events: List[HealthEvent]) -> IncidentTimeline: ...


class IHealthAlertingEngine(Protocol):
    def evaluate_alerts(self, events: List[HealthEvent]) -> AlertingReport: ...


class IHealthIntelligenceScorer(Protocol):
    def compute_scorecard(
        self,
        sm_report: StateMachineReport,
        deg_report: DegradationReport,
        rec_report: RecoveryValidationReport,
        sim_report: SimulationReport,
        alert_report: AlertingReport,
        timeline: IncidentTimeline,
        flapping_report: FlappingReport,
        evidence_valid: bool,
    ) -> HealthIntelligenceScorecard: ...
