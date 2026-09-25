"""
Abstract Interfaces for Enterprise Automated Restore Verification System (Part 3G.2E).
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from app.platform_verification.restore_verification.domain.models import (
    RestoreExecutionPlan,
    RecoveryEnvironmentReport,
    BackupCatalogReport,
    DatabaseRestoreValidationReport,
    DocumentRestoreValidationReport,
    ConfigurationRestoreValidationReport,
    SecretRestoreValidationReport,
    ServiceStartupReport,
    FunctionalRecoveryReport,
    IntegrityValidationReport,
    RTORPOReport,
    FailureSimulationReport,
    RestoreQualityScorecard,
)


class IRestoreOrchestrator(ABC):
    @abstractmethod
    def generate_restore_plan(self) -> RestoreExecutionPlan:
        pass


class IRecoveryEnvironmentManager(ABC):
    @abstractmethod
    def provision_recovery_environment(self) -> RecoveryEnvironmentReport:
        pass

    @abstractmethod
    def teardown_recovery_environment(self) -> bool:
        pass


class IBackupDiscoveryEngine(ABC):
    @abstractmethod
    def discover_and_catalog_backups(self) -> BackupCatalogReport:
        pass


class IRestoreExecutionEngine(ABC):
    @abstractmethod
    def execute_ordered_restore(
        self, plan: RestoreExecutionPlan
    ) -> Dict[str, Any]:
        pass


class IDatabaseRestoreValidator(ABC):
    @abstractmethod
    def validate_database_restore(self) -> DatabaseRestoreValidationReport:
        pass


class IDocumentRestoreValidator(ABC):
    @abstractmethod
    def validate_document_restore(self) -> DocumentRestoreValidationReport:
        pass


class IConfigSecretValidator(ABC):
    @abstractmethod
    def validate_configuration_and_secrets(
        self,
    ) -> tuple[ConfigurationRestoreValidationReport, SecretRestoreValidationReport]:
        pass


class IIntegrityChecker(ABC):
    @abstractmethod
    def verify_triple_checksum_integrity(self) -> IntegrityValidationReport:
        pass


class IServiceStartupValidator(ABC):
    @abstractmethod
    def validate_service_health_and_readiness(
        self,
    ) -> ServiceStartupReport:
        pass


class ISyntheticWorkflowRunner(ABC):
    @abstractmethod
    def execute_synthetic_business_workflows(
        self,
    ) -> FunctionalRecoveryReport:
        pass


class IRestoreFailureSimulator(ABC):
    @abstractmethod
    def simulate_failure_scenarios_and_rollbacks(
        self,
    ) -> FailureSimulationReport:
        pass


class IRTORPOBenchmarkingEngine(ABC):
    @abstractmethod
    def measure_rto_rpo_performance(self) -> RTORPOReport:
        pass


class IContinuousRecoveryScheduler(ABC):
    @abstractmethod
    def configure_recovery_drills(self) -> Dict[str, Any]:
        pass


class IRestoreQualityScoringEngine(ABC):
    @abstractmethod
    def compute_quality_scorecard(
        self,
        backup_recovery_success_score: float,
        data_integrity_score: float,
        service_recovery_score: float,
        functional_validation_score: float,
        security_validation_score: float,
        recovery_speed_score: float,
        execution_duration_ms: float,
    ) -> RestoreQualityScorecard:
        pass


class IRestoreEvidenceManifestEngine(ABC):
    @abstractmethod
    def export_all_evidence_artifacts(
        self,
        verification_data: Dict[str, Any],
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        pass
