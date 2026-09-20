"""
Interfaces and Abstract Protocols for Backup Certification Framework (Part 3G.2G).
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from app.platform_verification.backup_certification.domain.models import (
    CollectedBackupEvidence,
    CompletenessEvaluation,
    IntegrityEvaluation,
    RestoreCapabilityEvaluation,
    OperationalReadinessEvaluation,
    RTORPOCertification,
    BackupPolicyEvaluation,
    BackupRiskRegister,
    BackupReadinessScorecard,
    BackupHealthDashboardData,
)


class IEvidenceCollector(ABC):
    @abstractmethod
    def collect_all_evidence(self) -> CollectedBackupEvidence:
        pass


class ICompletenessAnalyzer(ABC):
    @abstractmethod
    def analyze_completeness(self, evidence: CollectedBackupEvidence) -> CompletenessEvaluation:
        pass


class IIntegrityAnalyzer(ABC):
    @abstractmethod
    def analyze_integrity(self, evidence: CollectedBackupEvidence) -> IntegrityEvaluation:
        pass


class IRestoreCapabilityAnalyzer(ABC):
    @abstractmethod
    def analyze_restore_capability(self, evidence: CollectedBackupEvidence) -> RestoreCapabilityEvaluation:
        pass


class IOperationalReadinessAnalyzer(ABC):
    @abstractmethod
    def analyze_operational_readiness(self, evidence: CollectedBackupEvidence) -> OperationalReadinessEvaluation:
        pass


class IRTORPOCertifier(ABC):
    @abstractmethod
    def certify_rto_rpo(self, evidence: CollectedBackupEvidence) -> RTORPOCertification:
        pass


class IBackupPolicyValidator(ABC):
    @abstractmethod
    def validate_policies(self, evidence: CollectedBackupEvidence) -> BackupPolicyEvaluation:
        pass


class IRiskRegisterGenerator(ABC):
    @abstractmethod
    def generate_risk_register(
        self,
        completeness: CompletenessEvaluation,
        integrity: IntegrityEvaluation,
        restore: RestoreCapabilityEvaluation,
        policy: BackupPolicyEvaluation,
        operational: OperationalReadinessEvaluation,
    ) -> BackupRiskRegister:
        pass


class IBackupReadinessScoringEngine(ABC):
    @abstractmethod
    def compute_certification_score(
        self,
        completeness_score: float,
        restore_score: float,
        integrity_score: float,
        security_score: float,
        automation_score: float,
        monitoring_score: float,
        documentation_score: float,
    ) -> BackupReadinessScorecard:
        pass


class IBackupDashboardEngine(ABC):
    @abstractmethod
    def generate_dashboard(
        self,
        scorecard: BackupReadinessScorecard,
        rto_rpo: RTORPOCertification,
        evidence: CollectedBackupEvidence,
    ) -> BackupHealthDashboardData:
        pass
