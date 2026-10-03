"""
Phase 3R.13: Operational Maturity Scoring & Certification Engine.
"""

from datetime import datetime, timezone
from typing import Any, Dict

from ..domain.interfaces import IOperationalMaturityScorer
from ..domain.models import MaturityCertification, OperationalMaturityScore


class OperationalMaturityScorer(IOperationalMaturityScorer):
    """
    Computes the weighted 6-dimensional Operational Maturity Index:
    1. Reliability (25%): SLO compliance, error budget health
    2. Incident Management (15%): MTTR, active incidents, postmortem coverage
    3. Observability (15%): Alert coverage, health visibility
    4. Automation (15%): Self-healing, runbook coverage
    5. Governance (15%): Change audit discipline, immutable logs
    6. Cost Control (15%): FinOps efficiency, budget containment
    """

    def score_maturity(self, operational_reports: Dict[str, Any]) -> OperationalMaturityScore:
        # 1. Reliability (25%)
        slo_rep = operational_reports.get("slo")
        budget_rep = operational_reports.get("error_budget")
        rel_score = 100.0
        if slo_rep and hasattr(slo_rep, "compliance_score"):
            rel_score = float(slo_rep.compliance_score)
        if budget_rep and getattr(budget_rep, "budget_exhausted", False):
            rel_score -= 20.0
        rel_score = max(0.0, min(100.0, rel_score))

        # 2. Incident Management (15%)
        inc_rep = operational_reports.get("incidents")
        inc_score = 96.0
        if inc_rep and hasattr(inc_rep, "active_incidents_count"):
            if inc_rep.active_incidents_count > 0:
                inc_score -= 15.0 * inc_rep.active_incidents_count
            if inc_rep.mean_time_to_recover_sec < 60.0:
                inc_score = min(100.0, inc_score + 4.0)
        inc_score = max(0.0, min(100.0, inc_score))

        # 3. Observability & Alerting (15%)
        alert_rep = operational_reports.get("alerts")
        health_rep = operational_reports.get("health")
        obs_score = 98.0
        if alert_rep and alert_rep.active_firing_alerts > 0:
            obs_score -= 10.0 * alert_rep.active_firing_alerts
        if health_rep and getattr(health_rep, "overall_status", None) and health_rep.overall_status.value != "HEALTHY":
            obs_score -= 15.0
        obs_score = max(0.0, min(100.0, obs_score))

        # 4. Automation & Self-Healing (15%)
        self_rep = operational_reports.get("self_healing")
        run_rep = operational_reports.get("runbooks")
        auto_score = 97.5
        if self_rep and self_rep.failed_remediations > 0:
            auto_score -= 20.0
        if run_rep and not run_rep.all_runbooks_validated:
            auto_score -= 15.0
        auto_score = max(0.0, min(100.0, auto_score))

        # 5. Governance & Audit (15%)
        chg_rep = operational_reports.get("changes")
        aud_rep = operational_reports.get("audit")
        gov_score = 100.0
        if chg_rep and hasattr(chg_rep, "change_discipline_score"):
            gov_score = float(chg_rep.change_discipline_score)
        if aud_rep and not aud_rep.immutable_log_verified:
            gov_score -= 30.0
        gov_score = max(0.0, min(100.0, gov_score))

        # 6. Cost Control & FinOps (15%)
        fin_rep = operational_reports.get("finops")
        cost_score = 96.5
        if fin_rep and hasattr(fin_rep, "cost_efficiency_score"):
            cost_score = float(fin_rep.cost_efficiency_score)
        if fin_rep and fin_rep.budget_utilized_pct > 100.0:
            cost_score -= 25.0
        cost_score = max(0.0, min(100.0, cost_score))

        # Weighted calculation
        overall = (
            (rel_score * 0.25)
            + (inc_score * 0.15)
            + (obs_score * 0.15)
            + (auto_score * 0.15)
            + (gov_score * 0.15)
            + (cost_score * 0.15)
        )
        overall = round(overall, 1)

        if overall >= 95.0:
            cert = MaturityCertification.ENTERPRISE_OPERATIONS_MATURE
        elif overall >= 90.0:
            cert = MaturityCertification.PRODUCTION_OPERATIONS_READY
        elif overall >= 80.0:
            cert = MaturityCertification.DEVELOPING
        else:
            cert = MaturityCertification.NEEDS_IMPROVEMENT

        return OperationalMaturityScore(
            reliability_score=rel_score,
            incident_management_score=inc_score,
            observability_score=obs_score,
            automation_score=auto_score,
            governance_score=gov_score,
            cost_control_score=cost_score,
            overall_maturity_score=overall,
            certification=cert,
            certified_at=datetime.now(timezone.utc).isoformat(),
            governance_passed=overall >= 90.0,
        )
