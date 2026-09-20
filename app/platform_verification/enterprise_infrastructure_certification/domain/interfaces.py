"""
Phase 3O: Enterprise Infrastructure Quality Scoring, Certification & Readiness Assessment — Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from .models import (
    CertificationDecision,
    MaturityAssessment,
    NormalizedEvidenceItem,
    QualityRegressionReport,
    QualityScorecard,
    RawEvidenceBundle,
    RiskAssessmentReport,
)


class IEvidenceCollector(ABC):
    @abstractmethod
    def collect_all_evidence(self, search_paths: Optional[List[str]] = None) -> List[RawEvidenceBundle]:
        pass


class IEvidenceNormalizer(ABC):
    @abstractmethod
    def normalize(self, bundles: List[RawEvidenceBundle]) -> List[NormalizedEvidenceItem]:
        pass


class IInfrastructureQualityScorer(ABC):
    @abstractmethod
    def calculate_score(
        self,
        evidence_items: List[NormalizedEvidenceItem],
        execution_time_seconds: float = 0.0,
    ) -> QualityScorecard:
        pass


class IInfrastructureRiskAnalyzer(ABC):
    @abstractmethod
    def assess_risks(
        self,
        scorecard: QualityScorecard,
        evidence_items: List[NormalizedEvidenceItem],
    ) -> RiskAssessmentReport:
        pass


class IInfrastructureCertifier(ABC):
    @abstractmethod
    def evaluate_certification(
        self,
        scorecard: QualityScorecard,
        risk_report: RiskAssessmentReport,
    ) -> CertificationDecision:
        pass


class IMaturityEvaluator(ABC):
    @abstractmethod
    def assess_maturity(
        self,
        scorecard: QualityScorecard,
        risk_report: RiskAssessmentReport,
    ) -> MaturityAssessment:
        pass


class IQualityRegressionDetector(ABC):
    @abstractmethod
    def detect_regressions(
        self,
        current_scorecard: QualityScorecard,
        previous_data: Optional[Dict[str, Any]] = None,
    ) -> QualityRegressionReport:
        pass
