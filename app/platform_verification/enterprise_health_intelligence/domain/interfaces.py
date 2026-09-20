"""
Phase 3H.5: Domain Interfaces for Enterprise Health Intelligence
"""
from abc import ABC, abstractmethod
from .models import (
    HealthEventArchitectureReport,
    FailureClassificationReport,
    EventCorrelationReport,
    RCAReport,
    RemediationDecisionReport,
    RecoveryExecutionReport,
    SelfHealingValidationReport,
    RemediationSecurityReport,
    HealthDashboardReport,
    ChaosHealthReport,
    HealthIntelligenceScorecard,
)


class IHealthEventArchitectureVerifier(ABC):
    @abstractmethod
    def verify_event_architecture(self) -> HealthEventArchitectureReport:
        pass


class IFailureClassificationEngine(ABC):
    @abstractmethod
    def classify_failures(self) -> FailureClassificationReport:
        pass


class IHealthSignalCorrelationEngine(ABC):
    @abstractmethod
    def correlate_signals(self) -> EventCorrelationReport:
        pass


class IRootCauseAnalysisVerifier(ABC):
    @abstractmethod
    def verify_rca(self) -> RCAReport:
        pass


class IRemediationDecisionEngine(ABC):
    @abstractmethod
    def generate_remediation_decisions(self) -> RemediationDecisionReport:
        pass


class IRecoveryExecutionVerifier(ABC):
    @abstractmethod
    def verify_recovery_execution(self) -> RecoveryExecutionReport:
        pass


class ISelfHealingValidator(ABC):
    @abstractmethod
    def validate_self_healing_lifecycle(self) -> SelfHealingValidationReport:
        pass


class IRemediationSafetyVerifier(ABC):
    @abstractmethod
    def verify_remediation_safety(self) -> RemediationSecurityReport:
        pass


class IHealthObservabilityVerifier(ABC):
    @abstractmethod
    def verify_observability_dashboards(self) -> HealthDashboardReport:
        pass


class IChaosIntelligenceValidator(ABC):
    @abstractmethod
    def run_chaos_validation(self) -> ChaosHealthReport:
        pass


class IHealthIntelligenceScorer(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        event_report: HealthEventArchitectureReport,
        class_report: FailureClassificationReport,
        corr_report: EventCorrelationReport,
        rca_report: RCAReport,
        remed_report: RemediationDecisionReport,
        recov_report: RecoveryExecutionReport,
        self_heal_report: SelfHealingValidationReport,
        safety_report: RemediationSecurityReport,
        obs_report: HealthDashboardReport,
        chaos_report: ChaosHealthReport,
    ) -> HealthIntelligenceScorecard:
        pass
