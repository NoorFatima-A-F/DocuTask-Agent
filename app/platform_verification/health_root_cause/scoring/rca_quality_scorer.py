"""Health Root Cause Quality Scorer (3H.4.2.14).

Computes 6-dimension weighted diagnosis quality score:
- Root Cause Accuracy (30%)
- Dependency Analysis (20%)
- Impact Prediction (15%)
- Event Correlation (15%)
- False Positive Control (10%)
- Evidence Quality (10%)

Awards Certification Tier:
- 95-100: Enterprise Incident Diagnosis Ready
- 90-94.99: Production Ready
- 80-89.99: Needs Improvement
- <80: Failed
"""

from datetime import datetime, timezone
from ..domain.models import (
    DependencyGraphReport,
    EventCorrelationReport,
    RootCauseReport,
    ImpactAnalysisReport,
    IncidentTimelineReport,
    CascadeDetectionReport,
    FalsePositiveAuditReport,
    IncidentMemoryReport,
    HealthRootCauseScorecard,
    RCATier,
)
from ..domain.interfaces import IHealthRootCauseScorer


class HealthRootCauseScorer(IHealthRootCauseScorer):
    """Calculates weighted operational diagnosis quality scores and assigns tiers."""

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
        # 1. Root cause accuracy (30%)
        rc_acc = 100.0 if rc_rep.primary_root_cause.confidence >= 0.90 else 85.0

        # 2. Dependency analysis (20%)
        dep_score = 100.0 if dep_rep.total_nodes >= 6 and casc_rep.cascade_prevented else 85.0

        # 3. Impact prediction (15%)
        imp_score = 100.0 if imp_rep.total_assessments >= 1 else 80.0

        # 4. Event correlation (15%)
        corr_score = round(corr_rep.avg_correlation_confidence * 100.0, 2)

        # 5. False positive control (10%)
        fp_score = 100.0 if fp_rep.false_positive_rate_pct == 0.0 else 80.0

        # 6. Evidence quality (10%)
        ev_score = 100.0 if time_rep.timeline_duration_seconds > 0 and mem_rep.total_known_signatures >= 4 else 85.0

        # Weighted calculation
        overall = (
            (rc_acc * 0.30)
            + (dep_score * 0.20)
            + (imp_score * 0.15)
            + (corr_score * 0.15)
            + (fp_score * 0.10)
            + (ev_score * 0.10)
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = RCATier.ENTERPRISE_INCIDENT_DIAGNOSIS_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = RCATier.PRODUCTION_READY
            verdict = "CONDITIONALLY CERTIFIED"
            passed = True
        elif overall >= 80.0:
            tier = RCATier.NEEDS_IMPROVEMENT
            verdict = "NEEDS IMPROVEMENT"
            passed = False
        else:
            tier = RCATier.FAILED
            verdict = "FAILED"
            passed = False

        return HealthRootCauseScorecard(
            root_cause_accuracy_score=round(rc_acc, 2),
            dependency_analysis_score=round(dep_score, 2),
            impact_prediction_score=round(imp_score, 2),
            event_correlation_score=round(corr_score, 2),
            false_positive_control_score=round(fp_score, 2),
            evidence_quality_score=round(ev_score, 2),
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
