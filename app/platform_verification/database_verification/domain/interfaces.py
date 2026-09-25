"""
Abstract interfaces for Part 2F: Enterprise Database Architecture Verification Framework.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from app.platform_verification.database_verification.domain.models import (
    TableSchemaDefinition,
    DatabaseBoundaryReport,
    SchemaQualityReport,
    MigrationStep,
    MigrationSafetyReport,
    TransactionSafetyReport,
    QueryPerformanceReport,
    TenantIsolationReport,
    DatabaseSecurityReport,
    BackupRecoveryReport,
    DatabaseQualityScorecard,
    DatabaseVerificationEvidencePackage,
)


class ISchemaAnalyzer(ABC):
    @abstractmethod
    def analyze_schemas(self, tables: Dict[str, TableSchemaDefinition]) -> SchemaQualityReport:
        """Analyzes tables for constraints, primary/foreign keys, naming, and 3NF normalization."""
        pass


class IDatabaseBoundaryVerifier(ABC):
    @abstractmethod
    def verify_boundaries(self, source_paths: List[str]) -> DatabaseBoundaryReport:
        """Verifies ORM models and repository separation from business/AI logic."""
        pass


class IMigrationSafetyValidator(ABC):
    @abstractmethod
    def validate_migrations(self, migrations: List[MigrationStep]) -> MigrationSafetyReport:
        """Validates forward and rollback migration steps for reversibility and safety."""
        pass


class ITransactionSafetyEngine(ABC):
    @abstractmethod
    def evaluate_transaction_safety(self, workflows: List[Dict[str, Any]]) -> TransactionSafetyReport:
        """Tests ACID rollback semantics, optimistic locking, and concurrency protection."""
        pass


class IQueryPerformanceAnalyzer(ABC):
    @abstractmethod
    def analyze_queries(self, queries: List[Dict[str, Any]], schemas: Dict[str, TableSchemaDefinition]) -> QueryPerformanceReport:
        """Evaluates query execution plans, missing indexes, and sequential scan hazards."""
        pass


class ITenantIsolationValidator(ABC):
    @abstractmethod
    def validate_isolation(self, queries: List[Dict[str, Any]]) -> TenantIsolationReport:
        """Ensures all entity queries enforce tenant filtering and detects data leaks."""
        pass


class IDatabaseSecurityEvaluator(ABC):
    @abstractmethod
    def evaluate_security(self, query_patterns: List[str], repo_code: List[str]) -> DatabaseSecurityReport:
        """Detects SQL injection patterns, plaintext credentials, and missing field encryption."""
        pass


class IBackupRecoveryValidator(ABC):
    @abstractmethod
    def validate_backup_recovery(self, backup_metadata: Dict[str, Any]) -> BackupRecoveryReport:
        """Validates backup integrity, RPO/RTO parameters, and restoration simulation."""
        pass


class IDatabaseScoringEngine(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        schema: SchemaQualityReport,
        tx: TransactionSafetyReport,
        perf: QueryPerformanceReport,
        security: DatabaseSecurityReport,
        isolation: TenantIsolationReport,
        migration: MigrationSafetyReport,
        recovery: BackupRecoveryReport,
    ) -> DatabaseQualityScorecard:
        """Computes weighted composite score and assigns certification tier."""
        pass


class IDatabaseEvidenceStore(ABC):
    @abstractmethod
    def seal_and_store_evidence(self, package: DatabaseVerificationEvidencePackage) -> str:
        """Persists and seals verification evidence package with SHA-256."""
        pass

    @abstractmethod
    def retrieve_evidence(self, package_id: str) -> Optional[DatabaseVerificationEvidencePackage]:
        """Retrieves stored evidence package."""
        pass
