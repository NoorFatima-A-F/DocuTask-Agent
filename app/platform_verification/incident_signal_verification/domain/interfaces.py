"""Abstract interfaces for Enterprise Incident Signal Verification sub-engines."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    IncidentArchitectureReport,
    AlertMappingReport,
    PayloadQualityReport,
    DependencyAnalysisReport,
    ImpactReport,
    PriorityReport,
    IncidentCorrelationReport,
    TimelineReport,
    RunbookReport,
    IncidentSecurityReport,
    IncidentAutomationReport,
    IncidentQualityScorecard,
)


class IIncidentArchitectureVerifier(ABC):
    """Interface for verifying incident lifecycle architecture (3H.4.7.1)."""

    @abstractmethod
    def verify_architecture(self) -> IncidentArchitectureReport:
        pass


class IAlertIncidentMappingVerifier(ABC):
    """Interface for verifying alert-to-incident transformation (3H.4.7.2)."""

    @abstractmethod
    def verify_alert_mapping(self) -> AlertMappingReport:
        pass


class IIncidentPayloadVerifier(ABC):
    """Interface for auditing incident payload completeness and diagnostic context (3H.4.7.3)."""

    @abstractmethod
    def verify_payload_quality(self) -> PayloadQualityReport:
        pass


class IDependencyBlastRadiusVerifier(ABC):
    """Interface for verifying dependency graph traversal and blast radius (3H.4.7.4)."""

    @abstractmethod
    def verify_dependency_analysis(self) -> DependencyAnalysisReport:
        pass


class IImpactAssessmentVerifier(ABC):
    """Interface for calculating user, business, and technical impact (3H.4.7.5)."""

    @abstractmethod
    def verify_impact_assessment(self) -> ImpactReport:
        pass


class IPriorityCalculatorVerifier(ABC):
    """Interface for verifying dynamic priority ranking calculation (3H.4.7.6)."""

    @abstractmethod
    def verify_priority_calculation(self) -> PriorityReport:
        pass


class IIncidentCorrelationVerifier(ABC):
    """Interface for verifying cascade symptom consolidation (3H.4.7.7)."""

    @abstractmethod
    def verify_correlation(self) -> IncidentCorrelationReport:
        pass


class IIncidentTimelineVerifier(ABC):
    """Interface for verifying incident event sequencing, MTTD, MTTA, MTTR (3H.4.7.8)."""

    @abstractmethod
    def verify_timeline(self) -> TimelineReport:
        pass


class IRunbookIntegrationVerifier(ABC):
    """Interface for verifying runbook attachments and remediation steps (3H.4.7.9)."""

    @abstractmethod
    def verify_runbooks(self) -> RunbookReport:
        pass


class IIncidentSecurityVerifier(ABC):
    """Interface for auditing incident payloads for zero secret/PII leaks (3H.4.7.10)."""

    @abstractmethod
    def verify_security(self) -> IncidentSecurityReport:
        pass


class IIncidentAutomationVerifier(ABC):
    """Interface for verifying automated self-healing triggers (3H.4.7.11)."""

    @abstractmethod
    def verify_automation(self) -> IncidentAutomationReport:
        pass


class IIncidentQualityScorer(ABC):
    """Interface for calculating 7-category weighted quality scorecard (3H.4.7.12)."""

    @abstractmethod
    def score_incidents(
        self,
        arch_rep: IncidentArchitectureReport,
        map_rep: AlertMappingReport,
        payload_rep: PayloadQualityReport,
        dep_rep: DependencyAnalysisReport,
        impact_rep: ImpactReport,
        prio_rep: PriorityReport,
        corr_rep: IncidentCorrelationReport,
        time_rep: TimelineReport,
        runbook_rep: RunbookReport,
        sec_rep: IncidentSecurityReport,
        auto_rep: IncidentAutomationReport,
    ) -> IncidentQualityScorecard:
        pass


class IIncidentEvidenceExporter(ABC):
    """Interface for exporting structured 13-manifest compliance evidence (3H.4.7.13)."""

    @abstractmethod
    def export_all(
        self,
        arch_rep: IncidentArchitectureReport,
        map_rep: AlertMappingReport,
        payload_rep: PayloadQualityReport,
        dep_rep: DependencyAnalysisReport,
        impact_rep: ImpactReport,
        prio_rep: PriorityReport,
        corr_rep: IncidentCorrelationReport,
        time_rep: TimelineReport,
        runbook_rep: RunbookReport,
        sec_rep: IncidentSecurityReport,
        auto_rep: IncidentAutomationReport,
        scorecard: IncidentQualityScorecard,
    ) -> Dict[str, str]:
        pass
