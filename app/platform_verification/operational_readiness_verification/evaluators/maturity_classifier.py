"""
Phase 3H.4.11.9: Operational Maturity Classifier
"""
from typing import List
from ..domain.interfaces import IMaturityClassifier
from ..domain.models import MaturityReport, MaturityLevel, OperationalRiskReport


class MaturityClassifier(IMaturityClassifier):
    def classify_maturity(self, composite_score: float, risk_report: OperationalRiskReport) -> MaturityReport:
        criteria_met: List[str] = []
        next_reqs: List[str] = []

        if composite_score >= 95.0 and risk_report.hard_gate_passed:
            level = MaturityLevel.LEVEL_5_ENTERPRISE
            numeric = 5
            criteria_met = [
                "Self-healing automated recovery validated across all dependencies",
                "Full-stack observability with zero PII/secret leaks",
                "Automated storm-resilient alert deduplication and correlation",
                "Comprehensive Grafana multi-dashboard operational visibility",
                "Continuous automated readiness certification and telemetry pipelines",
            ]
            next_reqs = ["Maintain continuous SLA/SLO compliance and multi-region chaos verification"]
        elif composite_score >= 90.0 and risk_report.hard_gate_passed:
            level = MaturityLevel.LEVEL_4_RELIABLE
            numeric = 4
            criteria_met = [
                "Automated failure recovery and chaos tests implemented",
                "Alert correlation and multi-channel routing active",
            ]
            next_reqs = ["Achieve >=95.0% composite score across all observability dimensions"]
        elif composite_score >= 80.0:
            level = MaturityLevel.LEVEL_3_OPERATIONAL
            numeric = 3
            criteria_met = ["Alerting and incident management payloads operational"]
            next_reqs = ["Implement automated self-healing workflows and eliminate all medium risks"]
        elif composite_score >= 60.0:
            level = MaturityLevel.LEVEL_2_OBSERVABLE
            numeric = 2
            criteria_met = ["Prometheus metrics and basic dashboards operational"]
            next_reqs = ["Implement alert correlation and incident runbooks"]
        elif composite_score >= 40.0:
            level = MaturityLevel.LEVEL_1_BASIC_MONITORING
            numeric = 1
            criteria_met = ["Health and liveness endpoints functional"]
            next_reqs = ["Add full Prometheus telemetry and metric scrapers"]
        else:
            level = MaturityLevel.LEVEL_0_UNKNOWN
            numeric = 0
            criteria_met = []
            next_reqs = ["Implement baseline health checks and metric endpoints"]

        return MaturityReport(
            level=level,
            level_numeric=numeric,
            criteria_met=criteria_met,
            next_level_requirements=next_reqs,
        )
