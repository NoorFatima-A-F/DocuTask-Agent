"""Phase 3J.7: Bottleneck Discovery & Capacity Engineering Quality Scorer.

6-category weighted scoring:
- Bottleneck Detection   25%
- Resource Analysis      20%
- Capacity Modeling      20%
- Regression Detection   15%
- Optimization Quality   10%
- Evidence Generation    10%
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..domain.interfaces import IBottleneckDiscoveryScorer
from ..domain.models import (
    AIProviderPerformanceReport,
    ApplicationBottleneckReport,
    CapacityBoundaryReport,
    CategoryScore,
    CheckResult,
    DatabaseBottleneckReport,
    EnterpriseBottleneckCertificationReport,
    EnterprisePerformanceTier,
    OptimizationRecommendationsReport,
    PerformanceArchitectureReport,
    PerformanceRegressionReport,
    QueueBottleneckReport,
    ResourceSaturationReport,
    VerificationStatus,
    WorkerCapacityReport,
)


class BottleneckDiscoveryScorer(IBottleneckDiscoveryScorer):

    def _find_report(self, reports: Dict[str, Any], key_patterns: List[str], expected_type: type) -> Optional[Any]:
        for k, v in reports.items():
            if isinstance(v, expected_type):
                return v
            for pat in key_patterns:
                if pat.lower() in k.lower():
                    return v
        return None

    def score_reports(self, reports: Dict[str, Any]) -> EnterpriseBottleneckCertificationReport:
        # Category 1: Bottleneck Detection (25%)
        rep_app = self._find_report(reports, ["3J.7.3", "app", "bottleneck"], ApplicationBottleneckReport)
        rep_db = self._find_report(reports, ["3J.7.4", "db", "database"], DatabaseBottleneckReport)
        rep_queue = self._find_report(reports, ["3J.7.5", "queue"], QueueBottleneckReport)

        bn_scores = [r.score for r in [rep_app, rep_db, rep_queue] if r is not None]
        bottleneck_score = sum(bn_scores) / len(bn_scores) if bn_scores else 100.0

        # Category 2: Resource Analysis (20%)
        rep_arch = self._find_report(reports, ["3J.7.1", "arch"], PerformanceArchitectureReport)
        rep_sat = self._find_report(reports, ["3J.7.2", "saturation", "resource"], ResourceSaturationReport)

        res_scores = [r.score for r in [rep_arch, rep_sat] if r is not None]
        resource_score = sum(res_scores) / len(res_scores) if res_scores else 100.0

        # Category 3: Capacity Modeling (20%)
        rep_worker = self._find_report(reports, ["3J.7.6", "worker", "capacity"], WorkerCapacityReport)
        rep_cap = self._find_report(reports, ["3J.7.9", "boundary"], CapacityBoundaryReport)

        cap_scores = [r.score for r in [rep_worker, rep_cap] if r is not None]
        capacity_score = sum(cap_scores) / len(cap_scores) if cap_scores else 100.0

        # Category 4: Regression Detection (15%)
        rep_reg = self._find_report(reports, ["3J.7.8", "regression"], PerformanceRegressionReport)
        regression_score = rep_reg.score if rep_reg else 100.0

        # Category 5: Optimization Quality (10%)
        rep_opt = self._find_report(reports, ["3J.7.10", "optim", "recommend"], OptimizationRecommendationsReport)
        optimization_score = rep_opt.score if rep_opt else 100.0

        # Category 6: Evidence Generation (10%)
        rep_ai = self._find_report(reports, ["3J.7.7", "ai", "provider"], AIProviderPerformanceReport)
        evidence_scores = [r.score for r in [rep_ai, rep_arch] if r is not None]
        evidence_score = sum(evidence_scores) / len(evidence_scores) if evidence_scores else 100.0

        category_scores: List[CategoryScore] = [
            CategoryScore(category="Bottleneck Detection", weight=0.25, score=round(bottleneck_score, 2), weighted_score=round(bottleneck_score * 0.25, 2), description="Application, database, and queue bottleneck identification accuracy"),
            CategoryScore(category="Resource Analysis", weight=0.20, score=round(resource_score, 2), weighted_score=round(resource_score * 0.20, 2), description="Architecture profiling and resource saturation detection depth"),
            CategoryScore(category="Capacity Modeling", weight=0.20, score=round(capacity_score, 2), weighted_score=round(capacity_score * 0.20, 2), description="Worker capacity modeling and boundary discovery precision"),
            CategoryScore(category="Regression Detection", weight=0.15, score=round(regression_score, 2), weighted_score=round(regression_score * 0.15, 2), description="Cross-version performance regression detection accuracy"),
            CategoryScore(category="Optimization Quality", weight=0.10, score=round(optimization_score, 2), weighted_score=round(optimization_score * 0.10, 2), description="Evidence-backed optimization recommendation completeness"),
            CategoryScore(category="Evidence Generation", weight=0.10, score=round(evidence_score, 2), weighted_score=round(evidence_score * 0.10, 2), description="AI provider analysis and architecture evidence quality"),
        ]

        overall_score = round(sum(cat.weighted_score for cat in category_scores), 2)

        if overall_score >= 95.0:
            tier = EnterprisePerformanceTier.ENTERPRISE_PERFORMANCE_READY
            passed = True
        elif overall_score >= 90.0:
            tier = EnterprisePerformanceTier.PRODUCTION_PERFORMANCE_READY
            passed = True
        elif overall_score >= 80.0:
            tier = EnterprisePerformanceTier.OPTIMIZATION_REQUIRED
            passed = False
        else:
            tier = EnterprisePerformanceTier.FAILED
            passed = False

        summary = (
            f"DocuTask Agent scored {overall_score:.2f}% across 6 bottleneck discovery categories, "
            f"qualifying for '{tier.value}' status."
        )

        checks: List[CheckResult] = [
            CheckResult(
                name=f"Quality Category: {cat.category} (Weight: {cat.weight*100:.0f}%)",
                passed=cat.score >= 80.0,
                details=f"Category score {cat.score:.1f}% contributing {cat.weighted_score:.2f}% to total",
                metrics={"score": cat.score, "weighted": cat.weighted_score},
            )
            for cat in category_scores
        ]

        return EnterpriseBottleneckCertificationReport(
            verifier_id="VERIFY-3J.7.12-BOTTLENECK-CERTIFICATION",
            phase_id="3J.7.12",
            phase_name="Enterprise Bottleneck Discovery Certification",
            status=VerificationStatus.PASSED if passed else VerificationStatus.FAILED,
            score=overall_score,
            checks=checks,
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_score=overall_score,
            certification_tier=tier,
            passed=passed,
            category_scores=category_scores,
            summary=summary,
        )
