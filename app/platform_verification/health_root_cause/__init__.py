"""Enterprise Health Root Cause Analysis & Failure Attribution Framework.

Part 3H.4.2 for DocuTask Agent.
"""

from .runtime.health_root_cause_runtime import HealthRootCauseRuntime
from .domain.models import (
    FailureCategory,
    IncidentSeverity,
    ComponentCriticality,
    DiagnosisConfidenceTier,
    RCATier,
    DependencyNode,
    DependencyGraphReport,
    RawTelemetrySignal,
    CorrelatedEventCluster,
    EventCorrelationReport,
    RootCauseHypothesis,
    RootCauseReport,
    ImpactAssessment,
    ImpactAnalysisReport,
    TimelineMilestone,
    IncidentTimelineReport,
    CascadeNodeResult,
    CascadeDetectionReport,
    FalsePositiveAuditReport,
    HistoricalIncidentSignature,
    IncidentMemoryReport,
    HealthDiagnosisResponse,
    HealthRootCauseScorecard,
)

__all__ = [
    "HealthRootCauseRuntime",
    "FailureCategory",
    "IncidentSeverity",
    "ComponentCriticality",
    "DiagnosisConfidenceTier",
    "RCATier",
    "DependencyNode",
    "DependencyGraphReport",
    "RawTelemetrySignal",
    "CorrelatedEventCluster",
    "EventCorrelationReport",
    "RootCauseHypothesis",
    "RootCauseReport",
    "ImpactAssessment",
    "ImpactAnalysisReport",
    "TimelineMilestone",
    "IncidentTimelineReport",
    "CascadeNodeResult",
    "CascadeDetectionReport",
    "FalsePositiveAuditReport",
    "HistoricalIncidentSignature",
    "IncidentMemoryReport",
    "HealthDiagnosisResponse",
    "HealthRootCauseScorecard",
]
