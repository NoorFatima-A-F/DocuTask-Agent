"""
Interfaces and Abstract Base Classes for Database Backup & Recovery Platform (Part 3G.2B Advanced).
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

from app.platform_verification.database_backup_verification.domain.models import (
    DatabaseInventoryReport,
    BackupCoverageReport,
    LogicalBackupReport,
    PhysicalBackupReport,
    WALVerificationReport,
    PITRReport,
    TransactionConsistencyReport,
    ReplicationVerificationReport,
    SchemaEvolutionReport,
    CorruptionClassificationReport,
    DataIntegrityReport,
    CryptographicVerificationReport,
    DatabaseSecurityReport,
    AutomatedRestoreReport,
    ForensicReport,
    ContinuousVerificationScheduleReport,
    QualityScorecard,
)


class IDatabaseInventoryEngine(ABC):
    @abstractmethod
    def discover_database_inventory(self) -> DatabaseInventoryReport:
        pass

    @abstractmethod
    def verify_backup_coverage(
        self, inventory: DatabaseInventoryReport
    ) -> BackupCoverageReport:
        pass


class ILogicalBackupVerifier(ABC):
    @abstractmethod
    def verify_logical_backup(self) -> LogicalBackupReport:
        pass


class IPhysicalBackupVerifier(ABC):
    @abstractmethod
    def verify_physical_backup(self) -> PhysicalBackupReport:
        pass


class IWALVerificationEngine(ABC):
    @abstractmethod
    def verify_wal_archive(self) -> WALVerificationReport:
        pass


class IPITRValidationEngine(ABC):
    @abstractmethod
    def run_pitr_validation(self) -> PITRReport:
        pass


class ITransactionConsistencyEngine(ABC):
    @abstractmethod
    def verify_transaction_consistency(self) -> TransactionConsistencyReport:
        pass


class IReplicationVerifier(ABC):
    @abstractmethod
    def verify_replication_subsystem(self) -> ReplicationVerificationReport:
        pass


class ISchemaEvolutionVerifier(ABC):
    @abstractmethod
    def verify_schema_evolution(self) -> SchemaEvolutionReport:
        pass


class ICorruptionClassifierEngine(ABC):
    @abstractmethod
    def classify_and_test_corruption(self) -> CorruptionClassificationReport:
        pass


class IDataIntegrityEngine(ABC):
    @abstractmethod
    def verify_data_integrity(self) -> DataIntegrityReport:
        pass

    @abstractmethod
    def verify_cryptographic_signatures(self) -> CryptographicVerificationReport:
        pass


class IDatabaseSecurityEngine(ABC):
    @abstractmethod
    def verify_database_security(self) -> DatabaseSecurityReport:
        pass


class IPerformanceBenchmarkingEngine(ABC):
    @abstractmethod
    def benchmark_performance(self) -> Any:
        pass

    @abstractmethod
    def evaluate_recovery_metrics(self) -> Any:
        pass


class IAutomatedRestoreOrchestrator(ABC):
    @abstractmethod
    def execute_automated_restore(self) -> AutomatedRestoreReport:
        pass


class IForensicVerificationEngine(ABC):
    @abstractmethod
    def generate_forensic_audit(self) -> ForensicReport:
        pass


class IContinuousVerificationEngine(ABC):
    @abstractmethod
    def evaluate_continuous_schedule(self) -> ContinuousVerificationScheduleReport:
        pass


class IQualityScoringEngine(ABC):
    @abstractmethod
    def compute_quality_scorecard(
        self,
        recoverability_score: float,
        consistency_score: float,
        integrity_score: float,
        security_score: float,
        performance_score: float,
        compatibility_score: float,
        automation_score: float,
        evidence_quality_score: float,
        execution_duration_ms: float,
    ) -> QualityScorecard:
        pass


class IEvidenceManifestEngine(ABC):
    @abstractmethod
    def export_all_evidence_artifacts(
        self,
        verification_data: Dict[str, Any],
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        pass


# ---------------------------------------------------------------------------
# Backwards Compatibility Interfaces (for legacy core engines)
# ---------------------------------------------------------------------------
class IStrategyMatrixEngine(ABC):
    @abstractmethod
    def evaluate_strategy_matrix(self) -> List[Any]:
        pass

    @abstractmethod
    def export_strategy_matrix_json(self, entries: List[Any]) -> Dict[str, Any]:
        pass


class ISchemaComparisonEngine(ABC):
    @abstractmethod
    def compare_schemas(self) -> Any:
        pass

    @abstractmethod
    def export_schema_validation_json(self, report: Any) -> Dict[str, Any]:
        pass


class IDataConsistencyValidator(ABC):
    @abstractmethod
    def validate_data_consistency(self) -> Any:
        pass

    @abstractmethod
    def export_consistency_report_json(self, report: Any) -> Dict[str, Any]:
        pass


class ICorruptionDetectionEngine(ABC):
    @abstractmethod
    def run_corruption_tests(self) -> Any:
        pass

    @abstractmethod
    def export_corruption_report_json(self, report: Any) -> Dict[str, Any]:
        pass


class IVersionMigrationVerifier(ABC):
    @abstractmethod
    def verify_version_compatibility(self) -> Any:
        pass

    @abstractmethod
    def export_migration_report_json(self, report: Any) -> Dict[str, Any]:
        pass


class IDatabaseCertificationEngine(ABC):
    @abstractmethod
    def calculate_readiness_score(self, **kwargs) -> Any:
        pass

    @abstractmethod
    def export_scorecard_json(self, scorecard: Any) -> Dict[str, Any]:
        pass


class IDatabaseEvidenceManifestEngine(ABC):
    @abstractmethod
    def export_all_evidence_artifacts(
        self,
        verification_data: Dict[str, Any],
        output_dir: Optional[str] = None,
    ) -> Dict[str, str]:
        pass

