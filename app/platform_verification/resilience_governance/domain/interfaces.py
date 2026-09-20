"""
Interfaces and Abstract Protocols for Disaster Recovery Governance Framework (Part 3G.4).
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from app.platform_verification.resilience_governance.domain.models import (
    OwnershipValidationReport,
    PolicyValidationReport,
    RecoveryChangeImpactReport,
    DocumentationDriftReport,
    ResilienceMaturityScore,
    PostmortemSectionReport,
    ContinuousResilienceMetricsReport,
    GovernanceScorecard,
)


class IOwnershipValidator(ABC):
    @abstractmethod
    def validate_ownership(self) -> OwnershipValidationReport:
        pass


class IPolicyManager(ABC):
    @abstractmethod
    def validate_policies(self) -> PolicyValidationReport:
        pass


class IChangeImpactAnalyzer(ABC):
    @abstractmethod
    def analyze_change_impact(self) -> RecoveryChangeImpactReport:
        pass


class IDocumentationDriftDetector(ABC):
    @abstractmethod
    def detect_documentation_drift(self) -> DocumentationDriftReport:
        pass


class IMaturityAssessmentEngine(ABC):
    @abstractmethod
    def assess_maturity(
        self,
        ownership: OwnershipValidationReport,
        policies: PolicyValidationReport,
        drift: DocumentationDriftReport,
        postmortem: PostmortemSectionReport,
        metrics: ContinuousResilienceMetricsReport,
    ) -> ResilienceMaturityScore:
        pass
