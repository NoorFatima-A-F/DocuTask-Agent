"""
Phase 3H.5.12: Domain Interfaces for Health Recovery Verification Framework
"""
from abc import ABC, abstractmethod
from .models import (
    HealthStateTransitionReport,
    FailureDetectionReport,
    RecoveryPolicyReport,
    ComponentRecoveryReport,
    RecoverySafetyReport,
    SelfHealingReport,
    RecoveryChaosReport,
    RecoveryValidationReport,
    RecoveryObservabilityReport,
    RecoverySecurityReport,
    HealthRecoveryScorecard,
)


class IHealthStateVerifier(ABC):
    @abstractmethod
    def verify_state_transitions(self) -> HealthStateTransitionReport:
        pass


class IFailureDetectionVerifier(ABC):
    @abstractmethod
    def verify_failure_detection(self) -> FailureDetectionReport:
        pass


class IRecoveryPolicyVerifier(ABC):
    @abstractmethod
    def verify_recovery_policies(self) -> RecoveryPolicyReport:
        pass


class IComponentRecoveryVerifier(ABC):
    @abstractmethod
    def verify_component_recovery(self) -> ComponentRecoveryReport:
        pass


class IRecoverySafetyVerifier(ABC):
    @abstractmethod
    def verify_recovery_safety(self) -> RecoverySafetyReport:
        pass


class ISelfHealingVerifier(ABC):
    @abstractmethod
    def verify_self_healing_workflow(self) -> SelfHealingReport:
        pass


class IRecoveryChaosVerifier(ABC):
    @abstractmethod
    def execute_chaos_testing(self) -> RecoveryChaosReport:
        pass


class IRecoveryValidationVerifier(ABC):
    @abstractmethod
    def verify_recovery_validation(self) -> RecoveryValidationReport:
        pass


class IRecoveryObservabilityVerifier(ABC):
    @abstractmethod
    def verify_recovery_observability(self) -> RecoveryObservabilityReport:
        pass


class IRecoverySecurityVerifier(ABC):
    @abstractmethod
    def verify_recovery_security(self) -> RecoverySecurityReport:
        pass


class IHealthRecoveryScorer(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        transition_report: HealthStateTransitionReport,
        detection_report: FailureDetectionReport,
        policy_report: RecoveryPolicyReport,
        component_report: ComponentRecoveryReport,
        safety_report: RecoverySafetyReport,
        self_healing_report: SelfHealingReport,
        chaos_report: RecoveryChaosReport,
        validation_report: RecoveryValidationReport,
        observability_report: RecoveryObservabilityReport,
        security_report: RecoverySecurityReport,
    ) -> HealthRecoveryScorecard:
        pass
