"""Portfolio Certification Scorer across 6 Core AI Product Dimensions."""

from datetime import datetime, timezone
from typing import Any, Dict, List
from ..domain.interfaces import IPortfolioCertificationScorer
from ..domain.models import (
    CategoryScore,
    CertificationTier,
    EvaluationStatus,
    PlatformCertificationScore,
)


class PortfolioCertificationScorer(IPortfolioCertificationScorer):
    """Calculates weighted certification score across 6 core AI platform evaluation pillars."""

    PILLAR_WEIGHTS = {
        "AI Quality & Accuracy": 0.25,
        "System Reliability & Fault Tolerance": 0.20,
        "Security & Tenant Isolation": 0.20,
        "System Performance & Latency": 0.15,
        "Business Value & Unit Economics": 0.15,
        "Explainability & Human Experience": 0.05,
    }

    PILLAR_REPORT_MAPPINGS = {
        "AI Quality & Accuracy": ["ai_capability", "llm_evaluation", "agent_evaluation", "rag_evaluation"],
        "System Reliability & Fault Tolerance": ["reliability"],
        "Security & Tenant Isolation": ["security"],
        "System Performance & Latency": ["performance"],
        "Business Value & Unit Economics": ["cost_business"],
        "Explainability & Human Experience": ["explainability", "human_experience"],
    }

    def calculate_score(self, reports: Dict[str, Any]) -> PlatformCertificationScore:
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
                        if str(st) in ("EvaluationStatus.PASSED", "PASSED"):
                            passed_checks += 1

            cat_avg_score = (sum(pillar_scores) / len(pillar_scores)) if pillar_scores else 100.0
            weighted_contribution = cat_avg_score * weight
            total_weighted_score += weighted_contribution

            cat_status = EvaluationStatus.PASSED if cat_avg_score >= 80.0 else EvaluationStatus.FAILED

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
            tier = CertificationTier.ENTERPRISE_AI_PLATFORM_CERTIFIED
            status = EvaluationStatus.PASSED
        elif overall >= 90.0:
            tier = CertificationTier.HIGH_PERFORMANCE_AI_SYSTEM
            status = EvaluationStatus.PASSED
        elif overall >= 80.0:
            tier = CertificationTier.QUALIFIED_AI_SYSTEM
            status = EvaluationStatus.WARNING
        else:
            tier = CertificationTier.REMEDIATION_REQUIRED
            status = EvaluationStatus.FAILED

        return PlatformCertificationScore(
            overall_score=overall,
            certification_tier=tier,
            evaluation_status=status,
            categories=categories,
            calculated_at=datetime.now(timezone.utc).isoformat(),
        )
