"""Dashboard Quality Scorer (3H.4.4.11).

Computes weighted composite score across 7 key operational dimensions and assigns certification tier:
- System visibility: 20%
- AI workload visibility: 20%
- Infrastructure visibility: 15%
- Incident usefulness: 15%
- Provisioning quality: 10%
- Performance: 10%
- Security: 10%
"""

from datetime import datetime, timezone
from ..domain.models import (
    ConfigurationReport,
    ProvisioningReport,
    DashboardValidationReport,
    UsabilityAuditReport,
    PerformanceBenchmarkReport,
    SecurityAuditReport,
    OperationalDashboardScorecard,
    DashboardCertificationTier,
)
from ..domain.interfaces import IOperationalDashboardScorer


class DashboardQualityScorer(IOperationalDashboardScorer):
    """Calculates weighted operational readiness score for Grafana dashboard suite."""

    def score_dashboards(
        self,
        config_rep: ConfigurationReport,
        prov_rep: ProvisioningReport,
        system_rep: DashboardValidationReport,
        ai_rep: DashboardValidationReport,
        agent_rep: DashboardValidationReport,
        infra_rep: DashboardValidationReport,
        incident_rep: DashboardValidationReport,
        usability_rep: UsabilityAuditReport,
        perf_rep: PerformanceBenchmarkReport,
        sec_rep: SecurityAuditReport,
    ) -> OperationalDashboardScorecard:
        # Category scores (0-100)
        sys_vis = 100.0 if system_rep.status == "PASS" else 50.0
        ai_vis = 100.0 if (ai_rep.status == "PASS" and agent_rep.status == "PASS") else 50.0
        infra_vis = 100.0 if infra_rep.status == "PASS" else 50.0
        inc_use = 100.0 if (incident_rep.status == "PASS" and usability_rep.status == "PASS") else 50.0
        prov_qual = 100.0 if (prov_rep.status == "PASS" and config_rep.status == "PASS") else 50.0
        perf = 100.0 if perf_rep.status == "PASS" else 50.0
        sec = 100.0 if sec_rep.status == "PASS" else 0.0

        # Weighted calculation
        overall = (
            sys_vis * 0.20
            + ai_vis * 0.20
            + infra_vis * 0.15
            + inc_use * 0.15
            + prov_qual * 0.10
            + perf * 0.10
            + sec * 0.10
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = DashboardCertificationTier.ENTERPRISE_DASHBOARD_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = DashboardCertificationTier.PRODUCTION_READY
            verdict = "CONDITIONAL_PASS"
            passed = True
        elif overall >= 80.0:
            tier = DashboardCertificationTier.IMPROVEMENT_REQUIRED
            verdict = "REMEDIATION_REQUIRED"
            passed = False
        else:
            tier = DashboardCertificationTier.FAILED
            verdict = "FAILED"
            passed = False

        return OperationalDashboardScorecard(
            system_visibility_score=sys_vis,
            ai_workload_visibility_score=ai_vis,
            infrastructure_visibility_score=infra_vis,
            incident_usefulness_score=inc_use,
            provisioning_quality_score=prov_qual,
            performance_score=perf,
            security_score=sec,
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
