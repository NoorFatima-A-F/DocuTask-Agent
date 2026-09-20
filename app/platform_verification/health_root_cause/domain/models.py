"""Domain models and data structures for Phase 3H.4.2 - Health Root Cause Analysis & Failure Attribution Framework.

Defines Dependency Graph Nodes/Edges, Correlated Events, Failure Categories, Severity Levels,
Causal Hypotheses, Cascade Chains, Impact Assessments, Timelines, and 6-Dimension Certification Scorecards.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone


class FailureCategory(str, Enum):
    """Categorization of operational failures (3H.4.2.3)."""
    INFRASTRUCTURE = "infrastructure"
    DEPENDENCY = "dependency"
    APPLICATION = "application"
    EXTERNAL_SERVICE = "external_service"
    PERFORMANCE_DEGRADATION = "performance_degradation"


class IncidentSeverity(str, Enum):
    """Incident severity classification (3H.4.2.6)."""
    SEV_1_CRITICAL = "SEV-1 Critical"   # System down / DB down / zero throughput
    SEV_2_MAJOR = "SEV-2 Major"         # Worker pool degraded / high queue backlog
    SEV_3_MINOR = "SEV-3 Minor"         # Single instance failure / isolated errors
    SEV_4_WARNING = "SEV-4 Warning"     # Latency increase / transient spike


class ComponentCriticality(str, Enum):
    """Criticality level of platform components in the topology."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class DiagnosisConfidenceTier(str, Enum):
    """Confidence tiers for root cause attribution."""
    HIGH = "high"          # >= 0.90
    MEDIUM = "medium"      # 0.70 - 0.89
    LOW = "low"            # < 0.70
    UNCONFIRMED = "unconfirmed"


class RCATier(str, Enum):
    """Certification tiers for operational diagnosis readiness (3H.4.2.14)."""
    ENTERPRISE_INCIDENT_DIAGNOSIS_READY = "Enterprise Incident Diagnosis Ready"  # 95 - 100%
    PRODUCTION_READY = "Production Ready"                                        # 90 - 94.99%
    NEEDS_IMPROVEMENT = "Needs Improvement"                                      # 80 - 89.99%
    FAILED = "Failed"                                                            # < 80%


# ---------------------------------------------------------------------------
# 3H.4.2.1 Dependency Graph Models
# ---------------------------------------------------------------------------
@dataclass
class DependencyNode:
    """Represents a component in the platform runtime DAG."""
    name: str
    component_type: str  # api_gateway, database, queue, worker, ai_provider, storage
    criticality: ComponentCriticality
    depends_on: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)
    healthy: bool = True


@dataclass
class DependencyGraphReport:
    """Report of the runtime dependency graph topology."""
    total_nodes: int
    critical_path_nodes: List[str]
    nodes: Dict[str, DependencyNode] = field(default_factory=dict)
    cascading_risk_score: float = 85.0
    status: str = "PASS"


# ---------------------------------------------------------------------------
# 3H.4.2.2 Health Event Correlation Models
# ---------------------------------------------------------------------------
@dataclass
class RawTelemetrySignal:
    """An individual signal from metrics, logs, traces, or health states."""
    signal_id: str
    source_component: str
    signal_type: str  # metric_breach, error_log, trace_latency, state_change
    description: str
    value: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class CorrelatedEventCluster:
    """Cluster of correlated telemetry signals pointing to a common incident."""
    cluster_id: str
    correlated_signals_count: int
    primary_component: str
    signals: List[RawTelemetrySignal] = field(default_factory=list)
    correlation_score: float = 0.94
    summary: str = ""


@dataclass
class EventCorrelationReport:
    """Report of multi-signal event correlation results."""
    total_clusters: int
    clusters: List[CorrelatedEventCluster] = field(default_factory=list)
    avg_correlation_confidence: float = 0.94
    status: str = "PASS"


# ---------------------------------------------------------------------------
# 3H.4.2.3 & 3H.4.2.4 Root Cause Scoring & Classification Models
# ---------------------------------------------------------------------------
@dataclass
class RootCauseHypothesis:
    """A scored causal hypothesis for a diagnosed failure."""
    component: str
    reason: str
    category: FailureCategory
    confidence: float
    signal_strength: float
    topological_score: float
    historical_match_score: float
    temporal_precedence_score: float
    evidence_summary: str
    recommended_action: str


@dataclass
class RootCauseReport:
    """Comprehensive failure attribution report."""
    incident_id: str
    primary_root_cause: RootCauseHypothesis
    secondary_hypotheses: List[RootCauseHypothesis] = field(default_factory=list)
    confidence_tier: DiagnosisConfidenceTier = DiagnosisConfidenceTier.HIGH
    status: str = "PASS"


# ---------------------------------------------------------------------------
# 3H.4.2.5 Impact Analysis Models
# ---------------------------------------------------------------------------
@dataclass
class ImpactAssessment:
    """Assesses operational blast radius and affected user services."""
    impact_id: str
    root_cause_component: str
    severity: IncidentSeverity
    affected_services: List[str]
    unaffected_services: List[str]
    business_impact: str
    estimated_blast_radius_pct: float


@dataclass
class ImpactAnalysisReport:
    """Report of platform impact analysis."""
    total_assessments: int
    assessments: List[ImpactAssessment] = field(default_factory=list)
    status: str = "PASS"


# ---------------------------------------------------------------------------
# 3H.4.2.7 Failure Timeline Models
# ---------------------------------------------------------------------------
@dataclass
class TimelineMilestone:
    """Milestone in the failure evolution timeline."""
    time_offset: str
    event: str
    component: str
    severity: str
    state_change: str


@dataclass
class IncidentTimelineReport:
    """Chronological reconstruction of failure onset, propagation, and recovery."""
    incident_id: str
    timeline_duration_seconds: float
    milestones: List[TimelineMilestone] = field(default_factory=list)
    status: str = "PASS"


# ---------------------------------------------------------------------------
# 3H.4.2.8 Cascading Failure Models
# ---------------------------------------------------------------------------
@dataclass
class CascadeNodeResult:
    """Node in a cascade propagation chain."""
    step_order: int
    component: str
    is_primary_root_cause: bool
    symptom: str


@dataclass
class CascadeDetectionReport:
    """Report of cascading failure isolation."""
    incident_id: str
    primary_origin_component: str
    propagation_depth: int
    cascade_chain: List[CascadeNodeResult] = field(default_factory=list)
    cascade_prevented: bool = True
    status: str = "PASS"


# ---------------------------------------------------------------------------
# 3H.4.2.9 False Positive Reduction Models
# ---------------------------------------------------------------------------
@dataclass
class FalsePositiveAuditReport:
    """Results of false positive damping and multi-signal confirmation tests."""
    total_signals_evaluated: int = 150
    transient_spikes_damped: int = 12
    multi_signal_confirmed_count: int = 4
    false_positive_rate_pct: float = 0.0
    status: str = "PASS"


# ---------------------------------------------------------------------------
# 3H.4.2.10 Historical Incident Memory Models
# ---------------------------------------------------------------------------
@dataclass
class HistoricalIncidentSignature:
    """Known historical failure pattern signature."""
    signature_id: str
    failure_pattern: str
    root_cause: str
    historical_occurrences: int
    matching_indicators: List[str]


@dataclass
class IncidentMemoryReport:
    """Knowledge base report of historical operational failure signatures."""
    total_known_signatures: int
    signatures: List[HistoricalIncidentSignature] = field(default_factory=list)
    status: str = "PASS"


# ---------------------------------------------------------------------------
# 3H.4.2.11 Extended Diagnosis Payload
# ---------------------------------------------------------------------------
@dataclass
class HealthDiagnosisResponse:
    """Response returned by GET /health/diagnosis."""
    state: str
    severity: IncidentSeverity
    root_cause: RootCauseHypothesis
    impact: ImpactAssessment
    timeline: IncidentTimelineReport
    cascade: CascadeDetectionReport
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ---------------------------------------------------------------------------
# 3H.4.2.14 Quality Scorecard Model
# ---------------------------------------------------------------------------
@dataclass
class HealthRootCauseScorecard:
    """Composite Weighted Diagnosis Quality Scorecard (3H.4.2.14)."""
    root_cause_accuracy_score: float = 100.0       # Weight: 30%
    dependency_analysis_score: float = 100.0       # Weight: 20%
    impact_prediction_score: float = 100.0         # Weight: 15%
    event_correlation_score: float = 100.0         # Weight: 15%
    false_positive_control_score: float = 100.0    # Weight: 10%
    evidence_quality_score: float = 100.0          # Weight: 10%
    overall_score: float = 100.0
    certification_tier: RCATier = RCATier.ENTERPRISE_INCIDENT_DIAGNOSIS_READY
    certification_verdict: str = "CERTIFIED"
    passed: bool = True
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
