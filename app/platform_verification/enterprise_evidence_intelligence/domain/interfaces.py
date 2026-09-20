"""
Phase 3P: Enterprise Verification Evidence Intelligence System — Interfaces.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from .models import (
    ComplianceReport,
    EngineeringAuditReport,
    ExecutiveCertificationReport,
    FailureEvidenceReport,
    PortfolioEvidenceBundle,
    StandardizedEvidenceItem,
)


class IEvidenceCollector(ABC):
    @property
    @abstractmethod
    def collector_name(self) -> str: pass

    @property
    @abstractmethod
    def category(self) -> str: pass

    @abstractmethod
    def collect(self) -> List[StandardizedEvidenceItem]: pass


class IEvidenceValidator(ABC):
    @abstractmethod
    def validate(self, item: StandardizedEvidenceItem) -> bool: pass


class IComplianceMapper(ABC):
    @abstractmethod
    def map_to_frameworks(self, items: List[StandardizedEvidenceItem]) -> ComplianceReport: pass


class IFailureEvidenceManager(ABC):
    @abstractmethod
    def analyze_failures(self, items: List[StandardizedEvidenceItem]) -> FailureEvidenceReport: pass


class IExecutiveReportGenerator(ABC):
    @abstractmethod
    def generate(self, items: List[StandardizedEvidenceItem], score: float) -> ExecutiveCertificationReport: pass


class IEngineeringAuditGenerator(ABC):
    @abstractmethod
    def generate(self, items: List[StandardizedEvidenceItem]) -> EngineeringAuditReport: pass


class IPortfolioLayerGenerator(ABC):
    @abstractmethod
    def generate(self, items: List[StandardizedEvidenceItem], score: float) -> PortfolioEvidenceBundle: pass
