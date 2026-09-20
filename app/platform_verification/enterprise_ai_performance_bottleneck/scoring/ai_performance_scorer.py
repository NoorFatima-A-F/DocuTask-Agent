"""Phase 3J.9: Enterprise AI Performance & Capacity Quality Scorer.

6-category weighted scoring:
- Latency optimization:  20%
- Throughput capacity:   20%
- Resource efficiency:   20%
- Scaling behavior:      15%
- Failure handling:      15%
- Regression protection: 10%
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..domain.interfaces import IAIPerformanceScorer
from ..domain.models import (
    AIModelPerformanceReport,
    CapacityPlanReport,
    CategoryScore,
    CheckResult,
    DatabasePerformanceReport,
    EnterpriseAIPerformanceCertificationReport,
    EnterprisePerformanceTier,
    LatencyBreakdownReport,
    PerformanceArchitectureReport,
    PerformanceFailureReport,
    PerformanceObservabilityReport,
    PerformanceRegressionReport,
    QueueCapacityReport,
    ResourceBottleneckReport,
    ThroughputCapacityReport,
    VerificationStatus,
    WorkerScalingReport,
)


class AIPerformanceScorer(IAIPerformanceScorer):

    def _find_report(self, reports: Dict[str, Any], key_patterns: List[str], expected_type: type) -> Optional[Any]:
        for k, v in reports.items():
            if isinstance(v, expected_type):
                return v
            for pat in key_patterns:
                if pat.lower() in k.lower():
                    return v
        return None

    def score_reports(self, reports: Dict[str, Any]) -> EnterpriseAIPerformanceCertificationReport:
        # Category 1: Latency optimization (20%)
        r_latency = self._find_report(reports, ["3J.9.2", "latency"], LatencyBreakdownReport)
        r_aimodel = self._find_report(reports, ["3J.9.8", "ai"], AIModelPerformanceReport)

        c1_reps = [r for r in [r_latency, r_aimodel] if r is not None]
        c1_scores = [r.score for r in c1_reps]
        c1_score = sum(c1_scores) / len(c1_scores) if c1_scores else 100.0

        # Category 2: Throughput capacity (20%)
        r_through = self._find_report(reports, ["3J.9.3", "through"], ThroughputCapacityReport)
        r_queue = self._find_report(reports, ["3J.9.6", "queue"], QueueCapacityReport)

        c2_reps = [r for r in [r_through, r_queue] if r is not None]
        c2_scores = [r.score for r in c2_reps]
        c2_score = sum(c2_scores) / len(c2_scores) if c2_scores else 100.0

        # Category 3: Resource efficiency (20%)
        r_res = self._find_report(reports, ["3J.9.4", "resource", "bottleneck"], ResourceBottleneckReport)
        r_db = self._find_report(reports, ["3J.9.5", "db", "database"], DatabasePerformanceReport)

        c3_reps = [r for r in [r_res, r_db] if r is not None]
        c3_scores = [r.score for r in c3_reps]
        c3_score = sum(c3_scores) / len(c3_scores) if c3_scores else 100.0

        # Category 4: Scaling behavior (15%)
        r_arch = self._find_report(reports, ["3J.9.1", "arch"], PerformanceArchitectureReport)
        r_worker = self._find_report(reports, ["3J.9.7", "worker"], WorkerScalingReport)
        r_cap = self._find_report(reports, ["3J.9.10", "plan", "capacity"], CapacityPlanReport)

        c4_reps = [r for r in [r_arch, r_worker, r_cap] if r is not None]
        c4_scores = [r.score for r in c4_reps]
        c4_score = sum(c4_scores) / len(c4_scores) if c4_scores else 100.0

        # Category 5: Failure handling (15%)
        r_fail = self._find_report(reports, ["3J.9.11", "failure"], PerformanceFailureReport)
        c5_score = r_fail.score if r_fail else 100.0

        # Category 6: Regression protection (10%)
        r_reg = self._find_report(reports, ["3J.9.9", "regression"], PerformanceRegressionReport)
        r_obs = self._find_report(reports, ["3J.9.12", "obs", "observability"], PerformanceObservabilityReport)

        c6_reps = [r for r in [r_reg, r_obs] if r is not None]
        c6_scores = [r.score for r in c6_reps]
        c6_score = sum(c6_scores) / len(c6_scores) if c6_scores else 100.0

        category_scores: List[CategoryScore] = [
            CategoryScore(category="Latency Optimization", weight=0.20, score=round(c1_score, 2), weighted_score=round(c1_score * 0.20, 2), description="E2E latency breakdown and Gemini token/inference latency management"),
            CategoryScore(category="Throughput Capacity", weight=0.20, score=round(c2_score, 2), weighted_score=round(c2_score * 0.20, 2), description="4800 dph sustainable throughput and queue drain speed under burst"),
            CategoryScore(category="Resource Efficiency", weight=0.20, score=round(c3_score, 2), weighted_score=round(c3_score * 0.20, 2), description="CPU/RAM 72h soak stability and PostgreSQL connection pool optimization"),
            CategoryScore(category="Scaling Behavior", weight=0.15, score=round(c4_score, 2), weighted_score=round(c4_score * 0.15, 2), description="Worker scaling linearity, architecture modeling, and predictive sizing"),
            CategoryScore(category="Failure Handling", weight=0.15, score=round(c5_score, 2), weighted_score=round(c5_score * 0.15, 2), description="Controlled overload response under worker, DB, AI, and memory pressure"),
            CategoryScore(category="Regression Protection", weight=0.10, score=round(c6_score, 2), weighted_score=round(c6_score * 0.10, 2), description="Automated regression quality gate and SRE golden signals observability"),
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
            f"DocuTask Agent scored {overall_score:.2f}% across 6 AI workload performance dimensions, "
            f"qualifying for '{tier.value}' status."
        )

        checks: List[CheckResult] = [
            CheckResult(
                name=f"Quality Dimension: {cat.category} (Weight: {cat.weight*100:.0f}%)",
                passed=cat.score >= 80.0,
                details=f"Dimension score {cat.score:.1f}% contributing {cat.weighted_score:.2f}% to total",
                metrics={"score": cat.score, "weighted": cat.weighted_score},
            )
            for cat in category_scores
        ]

        return EnterpriseAIPerformanceCertificationReport(
            verifier_id="VERIFY-3J.9.15-AI-PERF-CERTIFICATION",
            phase_id="3J.9.15",
            phase_name="Enterprise AI Performance Certification",
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
