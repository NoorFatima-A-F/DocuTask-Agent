"""Abstract interfaces for Health Root Cause Analysis sub-engines."""

from abc import ABC, abstractmethod
from typing import Dict
from .models import (
    DependencyGraphReport,
    EventCorrelationReport,
    RootCauseReport,
    ImpactAnalysisReport,
    IncidentTimelineReport,
    CascadeDetectionReport,
    FalsePositiveAuditReport,
    IncidentMemoryReport,
    HealthRootCauseScorecard,
)


class IDependencyGraph(ABC):
    """Interface for platform runtime dependency graph modeling (3H.4.2.1)."""

    @abstractmethod
    def build_graph_report(self) -> DependencyGraphReport:
        pass


class IHealthEventCorrelator(ABC):
    """Interface for multi-signal health event correlation (3H.4.2.2)."""

    @abstractmethod
    def correlate_events(self) -> EventCorrelationReport:
        pass


class IRootCauseScorer(ABC):
    """Interface for root cause identification and scoring (3H.4.2.4)."""

    @abstractmethod
    def diagnose_root_cause(self, incident_id: str) -> RootCauseReport:
        pass


class IImpactAnalyzer(ABC):
    """Interface for business service impact and blast radius assessment (3H.4.2.5)."""

    @abstractmethod
    def analyze_impact(self, component: str) -> ImpactAnalysisReport:
        pass


class IIncidentTimelineReconstructor(ABC):
    """Interface for failure timeline reconstruction (3H.4.2.7)."""

    @abstractmethod
    def reconstruct_timeline(self, incident_id: str) -> IncidentTimelineReport:
        pass


class ICascadeDetector(ABC):
    """Interface for cascading failure isolation (3H.4.2.8)."""

    @abstractmethod
    def detect_cascade(self, incident_id: str) -> CascadeDetectionReport:
        pass


class IFalsePositiveFilter(ABC):
    """Interface for multi-signal false positive reduction (3H.4.2.9)."""

    @abstractmethod
    def audit_false_positive_control(self) -> FalsePositiveAuditReport:
        pass


class IIncidentMemory(ABC):
    """Interface for historical failure pattern memory and learning (3H.4.2.10)."""

    @abstractmethod
    def get_memory_report(self) -> IncidentMemoryReport:
        pass


class IHealthRootCauseScorer(ABC):
    """Interface for 6-dimension weighted quality scoring (3H.4.2.14)."""

    @abstractmethod
    def score_rca(
        self,
        dep_rep: DependencyGraphReport,
        corr_rep: EventCorrelationReport,
        rc_rep: RootCauseReport,
        imp_rep: ImpactAnalysisReport,
        time_rep: IncidentTimelineReport,
        casc_rep: CascadeDetectionReport,
        fp_rep: FalsePositiveAuditReport,
        mem_rep: IncidentMemoryReport,
    ) -> HealthRootCauseScorecard:
        pass


class IRCAEvidenceExporter(ABC):
    """Interface for exporting structured audit manifests (3H.4.2.13)."""

    @abstractmethod
    def export_all(
        self,
        dep_rep: DependencyGraphReport,
        corr_rep: EventCorrelationReport,
        rc_rep: RootCauseReport,
        imp_rep: ImpactAnalysisReport,
        time_rep: IncidentTimelineReport,
        casc_rep: CascadeDetectionReport,
        fp_rep: FalsePositiveAuditReport,
        mem_rep: IncidentMemoryReport,
        scorecard: HealthRootCauseScorecard,
    ) -> Dict[str, str]:
        pass
