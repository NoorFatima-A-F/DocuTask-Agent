"""
Phase 3H.4.9: Enterprise Incident Recovery Verification Framework - Abstract Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    RecoveryPlan,
    RecoveryExecutionResult,
    HealthValidationReport,
    RecoveryMetricsReport,
    FailureSimulationResult,
    DataIntegrityReport,
    RollbackVerificationReport,
    RecoverySafetyReport,
    PostIncidentImprovementReport,
    RecoveryScorecard,
    IncidentType,
)


class IRecoveryArchitectureVerifier(ABC):
    @abstractmethod
    def verify_recovery_architecture(self) -> Dict[str, Any]:
        pass


class IActionMappingVerifier(ABC):
    @abstractmethod
    def generate_plan(self, incident_type: IncidentType, incident_id: str) -> RecoveryPlan:
        pass

    @abstractmethod
    def verify_action_mappings(self) -> Dict[str, Any]:
        pass


class IAutomatedRecoveryVerifier(ABC):
    @abstractmethod
    def execute_recovery(self, plan: RecoveryPlan) -> RecoveryExecutionResult:
        pass

    @abstractmethod
    def verify_automation_workflow(self) -> Dict[str, Any]:
        pass


class IHealthValidationVerifier(ABC):
    @abstractmethod
    def validate_post_recovery_health(self) -> HealthValidationReport:
        pass


class IRecoveryMetricsVerifier(ABC):
    @abstractmethod
    def compute_recovery_metrics(self) -> RecoveryMetricsReport:
        pass


class IFailureRecoverySimulator(ABC):
    @abstractmethod
    def simulate_failure_recovery_scenarios(self) -> List[FailureSimulationResult]:
        pass


class IDataIntegrityVerifier(ABC):
    @abstractmethod
    def verify_data_integrity(self) -> DataIntegrityReport:
        pass


class IRollbackVerifier(ABC):
    @abstractmethod
    def verify_rollback_mechanisms(self) -> RollbackVerificationReport:
        pass


class IRecoverySafetyVerifier(ABC):
    @abstractmethod
    def verify_safety_guardrails(self) -> RecoverySafetyReport:
        pass


class IPostIncidentImprovementVerifier(ABC):
    @abstractmethod
    def generate_post_incident_review(self, incident_id: str) -> PostIncidentImprovementReport:
        pass


class IRecoveryScorer(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        automation_result: Dict[str, Any],
        metrics_report: RecoveryMetricsReport,
        integrity_report: DataIntegrityReport,
        safety_report: RecoverySafetyReport,
        validation_report: HealthValidationReport,
        improvement_report: PostIncidentImprovementReport,
    ) -> RecoveryScorecard:
        pass


class IRecoveryEvidenceExporter(ABC):
    @abstractmethod
    def export_evidence_manifests(
        self,
        output_dir: str,
        architecture_data: Dict[str, Any],
        action_mapping_data: Dict[str, Any],
        automation_data: Dict[str, Any],
        validation_report: HealthValidationReport,
        metrics_report: RecoveryMetricsReport,
        simulations: List[FailureSimulationResult],
        integrity_report: DataIntegrityReport,
        rollback_report: RollbackVerificationReport,
        safety_report: RecoverySafetyReport,
        improvement_report: PostIncidentImprovementReport,
        scorecard: RecoveryScorecard,
    ) -> List[str]:
        pass
