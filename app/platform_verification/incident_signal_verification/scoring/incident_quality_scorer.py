"""Incident Quality Scorer (3H.4.7.12).

Computes 7-category weighted composite score for enterprise incident readiness:
- Alert-to-incident accuracy (20%)
- Context completeness (20%)
- Impact analysis (15%)
- Correlation quality (15%)
- Timeline accuracy (10%)
- Response guidance (10%)
- Security (10%)
"""

from datetime import datetime, timezone
from ..domain.models import (
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
    IncidentCertificationTier,
)
from ..domain.interfaces import IIncidentQualityScorer


class IncidentQualityScorer(IIncidentQualityScorer):
    """Calculates weighted operational readiness score for incident signals."""

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
        # Category scores (0-100)
        acc_score = 100.0 if (map_rep.status == "PASS" and arch_rep.status == "PASS") else 50.0
        context_score = 100.0 if (payload_rep.status == "PASS" and dep_rep.status == "PASS") else 50.0
        impact_score = 100.0 if (impact_rep.status == "PASS" and prio_rep.status == "PASS") else 50.0
        corr_score = 100.0 if (corr_rep.status == "PASS" and corr_rep.correlation_accuracy == 100.0) else 50.0
        time_score = 100.0 if (time_rep.status == "PASS" and time_rep.mttd_seconds < 30.0) else 50.0
        guidance_score = 100.0 if (runbook_rep.status == "PASS" and auto_rep.status == "PASS") else 50.0
        sec_score = 100.0 if (sec_rep.status == "PASS" and sec_rep.zero_leak_verified) else 0.0

        # Weighted calculation
        overall = (
            acc_score * 0.20
            + context_score * 0.20
            + impact_score * 0.15
            + corr_score * 0.15
            + time_score * 0.10
            + guidance_score * 0.10
            + sec_score * 0.10
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = IncidentCertificationTier.ENTERPRISE_INCIDENT_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = IncidentCertificationTier.PRODUCTION_INCIDENT_READY
            verdict = "CONDITIONAL_PASS"
            passed = True
        elif overall >= 80.0:
            tier = IncidentCertificationTier.IMPROVEMENT_REQUIRED
            verdict = "REMEDIATION_REQUIRED"
            passed = False
        else:
            tier = IncidentCertificationTier.FAILED
            verdict = "FAILED"
            passed = False

        return IncidentQualityScorecard(
            alert_to_incident_accuracy_score=acc_score,
            context_completeness_score=context_score,
            impact_analysis_score=impact_score,
            correlation_quality_score=corr_score,
            timeline_accuracy_score=time_score,
            response_guidance_score=guidance_score,
            security_score=sec_score,
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
