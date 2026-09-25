"""Abstract interfaces for Phase 3H.3.12 Enterprise Readiness Evidence Generation Framework."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    StandardizedEvidenceRecord,
    EvidenceMetadata,
    EvidenceIntegrityReport,
    ReadinessTimelineReport,
    FailureEvidenceReport,
    ReadinessRegressionReport,
    AuditQualityScorecard,
)


class IReadinessEvidenceCollector(ABC):
    """Interface for centralized evidence collection (3H.3.12.1)."""
    @abstractmethod
    def collect_raw_evidence(self) -> List[Dict[str, Any]]:
        pass


class IEvidenceSchemaNormalizer(ABC):
    """Interface for standardizing evidence schemas (3H.3.12.2)."""
    @abstractmethod
    def normalize_records(self, raw_records: List[Dict[str, Any]]) -> List[StandardizedEvidenceRecord]:
        pass


class IEvidenceMetadataGenerator(ABC):
    """Interface for runtime & application metadata generation (3H.3.12.4)."""
    @abstractmethod
    def generate_metadata(self) -> EvidenceMetadata:
        pass


class IEvidenceIntegrityVerifier(ABC):
    """Interface for SHA-256 integrity hash verification (3H.3.12.5)."""
    @abstractmethod
    def compute_and_verify_integrity(self, target_dir: str) -> EvidenceIntegrityReport:
        pass


class IReadinessTimelineReconstructor(ABC):
    """Interface for timeline reconstruction and TTR computation (3H.3.12.6)."""
    @abstractmethod
    def reconstruct_timeline(self) -> ReadinessTimelineReport:
        pass


class IFailureEvidenceDocumenter(ABC):
    """Interface for failure evidence documentation (3H.3.12.7)."""
    @abstractmethod
    def document_failures(self) -> FailureEvidenceReport:
        pass


class IEvidenceRegressionComparator(ABC):
    """Interface for historical comparison and regression detection (3H.3.12.8)."""
    @abstractmethod
    def compare_against_baseline(self) -> ReadinessRegressionReport:
        pass


class IEvidenceQualityScorer(ABC):
    """Interface for 6-dimension weighted evidence quality scoring (3H.3.12.11)."""
    @abstractmethod
    def calculate_scorecard(
        self,
        integrity_report: EvidenceIntegrityReport,
        timeline_report: ReadinessTimelineReport,
        failure_report: FailureEvidenceReport,
        regression_report: ReadinessRegressionReport,
        total_records: int,
    ) -> AuditQualityScorecard:
        pass


class IFinalEvidencePackageGenerator(ABC):
    """Interface for final packaging of manifests and README.md (3H.3.12.12)."""
    @abstractmethod
    def generate_package(
        self,
        metadata: EvidenceMetadata,
        integrity_report: EvidenceIntegrityReport,
        timeline_report: ReadinessTimelineReport,
        failure_report: FailureEvidenceReport,
        regression_report: ReadinessRegressionReport,
        scorecard: AuditQualityScorecard,
        target_dir: str,
    ) -> Dict[str, str]:
        pass
