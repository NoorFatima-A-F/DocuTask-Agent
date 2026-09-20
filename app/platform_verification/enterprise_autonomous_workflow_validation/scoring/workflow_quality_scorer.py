"""Multi-Dimensional Quality Scorer for Phase 5 Autonomous Workflows."""

from datetime import datetime, timezone
from typing import Any, Dict, List
from ..domain.interfaces import IAutonomousWorkflowQualityScorer
from ..domain.models import (
    AutonomousWorkflowQualityScore,
    CategoryScore,
    CertificationTier,
    VerificationStatus,
)


class AutonomousWorkflowQualityScorer(IAutonomousWorkflowQualityScorer):
    """Calculates weighted enterprise certification score across 7 business pillars."""

    PILLAR_WEIGHTS = {
        "Business Process Execution & Scenario Breadth": 0.20,
        "Autonomous Decision & AI Quality": 0.15,
        "Human-in-the-Loop & Governance Enforcement": 0.15,
        "Multi-Agent & Organizational Coordination": 0.15,
        "Resilience, Exception Recovery & Long-Running State": 0.15,
        "Business Value, KPIs & Cost Economics": 0.10,
        "Scalability, Audit & Executive Readiness": 0.10,
    }

    PILLAR_REPORT_MAPPINGS = {
        "Business Process Execution & Scenario Breadth": ["scenario_library", "complete_execution", "enterprise_dataset"],
        "Autonomous Decision & AI Quality": ["decision_quality", "explainability", "optimization"],
        "Human-in-the-Loop & Governance Enforcement": ["human_in_the_loop", "business_rules", "compliance"],
        "Multi-Agent & Organizational Coordination": ["multi_agent_collaboration", "organizational_workflow"],
        "Resilience, Exception Recovery & Long-Running State": ["exception_workflow", "autonomous_recovery", "long_running"],
        "Business Value, KPIs & Cost Economics": ["business_kpi", "cost_validation", "business_value"],
        "Scalability, Audit & Executive Readiness": ["audit_trail", "scalability", "executive_readiness"],
    }

    def calculate_score(self, reports: Dict[str, Any]) -> AutonomousWorkflowQualityScore:
        categories: List[CategoryScore] = []
        total_weighted_score = 0.0

        for pillar_name, weight in self.PILLAR_WEIGHTS.items():
            report_keys = self.PILLAR_REPORT_MAPPINGS.get(pillar_name, [])
            pillar_scores = []
            total_checks = 0
            passed_checks = 0

            for key in report_keys:
                rep = reports.get(key)
                if rep:
                    score_val = getattr(rep, "score", None) if hasattr(rep, "score") else rep.get("score", 0.0)
                    pillar_scores.append(float(score_val))

                    checks = getattr(rep, "checks", None) if hasattr(rep, "checks") else rep.get("checks", [])
                    for chk in checks:
                        total_checks += 1
                        st = getattr(chk, "status", None) if hasattr(chk, "status") else chk.get("status")
                        if str(st) in ("VerificationStatus.PASSED", "PASSED"):
                            passed_checks += 1

            cat_avg_score = (sum(pillar_scores) / len(pillar_scores)) if pillar_scores else 100.0
            weighted_contribution = cat_avg_score * weight
            total_weighted_score += weighted_contribution

            cat_status = VerificationStatus.PASSED if cat_avg_score >= 80.0 else VerificationStatus.FAILED

            categories.append(
                CategoryScore(
                    name=pillar_name,
                    weight=weight,
                    score=round(cat_avg_score, 2),
                    weighted_score=round(weighted_contribution, 2),
                    checks_total=total_checks,
                    checks_passed=passed_checks,
                    status=cat_status,
                )
            )

        overall = round(total_weighted_score, 2)

        if overall >= 95.0:
            tier = CertificationTier.ENTERPRISE_AUTONOMOUS_BUSINESS_READY
            status = VerificationStatus.PASSED
        elif overall >= 90.0:
            tier = CertificationTier.HIGH_OPERATIONAL_MATURITY
            status = VerificationStatus.PASSED
        elif overall >= 80.0:
            tier = CertificationTier.CONDITIONALLY_CERTIFIED
            status = VerificationStatus.WARNING
        else:
            tier = CertificationTier.CERTIFICATION_FAILED
            status = VerificationStatus.FAILED

        return AutonomousWorkflowQualityScore(
            overall_score=overall,
            certification_tier=tier,
            verification_status=status,
            categories=categories,
            calculated_at=datetime.now(timezone.utc).isoformat(),
        )
