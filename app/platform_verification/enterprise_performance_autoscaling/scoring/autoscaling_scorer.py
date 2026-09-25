"""Phase 3J.8: Autoscaling & Elastic Capacity Quality Scorer.

6-category weighted scoring:
- Scaling Correctness      25%
- Performance Preservation 20%
- Failure Safety           20%
- Cost Efficiency          15%
- Cloud Readiness          10%
- Evidence Quality         10%
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..domain.interfaces import IAutoscalingScorer
from ..domain.models import (
    AIScalingReport,
    APIScalingReport,
    AutoscalingArchitectureReport,
    CategoryScore,
    CheckResult,
    CloudScalingReport,
    CostScalingReport,
    DatabaseScalingImpactReport,
    EnterpriseAutoscalingCertificationReport,
    EnterprisePerformanceTier,
    K8sScalingReadinessReport,
    QueueAutoscalingReport,
    ScaleDownSafetyReport,
    ScaleUpValidationReport,
    ScalingFailureReport,
    ScalingMetricsReport,
    ScalingPolicyReport,
    VerificationStatus,
    WorkerScalingReport,
)


class AutoscalingScorer(IAutoscalingScorer):

    def _find_report(self, reports: Dict[str, Any], key_patterns: List[str], expected_type: type) -> Optional[Any]:
        for k, v in reports.items():
            if isinstance(v, expected_type):
                return v
            for pat in key_patterns:
                if pat.lower() in k.lower():
                    return v
        return None

    def score_reports(self, reports: Dict[str, Any]) -> EnterpriseAutoscalingCertificationReport:
        # Category 1: Scaling Correctness (25%)
        r_arch = self._find_report(reports, ["3J.8.1", "arch"], AutoscalingArchitectureReport)
        r_worker = self._find_report(reports, ["3J.8.3", "worker"], WorkerScalingReport)
        r_api = self._find_report(reports, ["3J.8.5", "api"], APIScalingReport)
        r_policy = self._find_report(reports, ["3J.8.6", "policy"], ScalingPolicyReport)

        c1_reps = [r for r in [r_arch, r_worker, r_api, r_policy] if r is not None]
        c1_scores = [r.score for r in c1_reps]
        c1_score = sum(c1_scores) / len(c1_scores) if c1_scores else 100.0

        # Category 2: Performance Preservation (20%)
        r_queue = self._find_report(reports, ["3J.8.4", "queue"], QueueAutoscalingReport)
        r_scaleup = self._find_report(reports, ["3J.8.7", "scale_up", "up"], ScaleUpValidationReport)
        r_ai = self._find_report(reports, ["3J.8.10", "ai"], AIScalingReport)

        c2_reps = [r for r in [r_queue, r_scaleup, r_ai] if r is not None]
        c2_scores = [r.score for r in c2_reps]
        c2_score = sum(c2_scores) / len(c2_scores) if c2_scores else 100.0

        # Category 3: Failure Safety (20%)
        r_scaledown = self._find_report(reports, ["3J.8.8", "down", "safety"], ScaleDownSafetyReport)
        r_db = self._find_report(reports, ["3J.8.9", "db", "database"], DatabaseScalingImpactReport)
        r_fail = self._find_report(reports, ["3J.8.14", "failure", "simulation"], ScalingFailureReport)

        c3_reps = [r for r in [r_scaledown, r_db, r_fail] if r is not None]
        c3_scores = [r.score for r in c3_reps]
        c3_score = sum(c3_scores) / len(c3_scores) if c3_scores else 100.0

        # Category 4: Cost Efficiency (15%)
        r_cost = self._find_report(reports, ["3J.8.13", "cost"], CostScalingReport)
        c4_score = r_cost.score if r_cost else 100.0

        # Category 5: Cloud Readiness (10%)
        r_k8s = self._find_report(reports, ["3J.8.11", "k8s", "kubernetes"], K8sScalingReadinessReport)
        r_cloud = self._find_report(reports, ["3J.8.12", "cloud"], CloudScalingReport)

        c5_reps = [r for r in [r_k8s, r_cloud] if r is not None]
        c5_scores = [r.score for r in c5_reps]
        c5_score = sum(c5_scores) / len(c5_scores) if c5_scores else 100.0

        # Category 6: Evidence Quality (10%)
        r_metrics = self._find_report(reports, ["3J.8.2", "metric"], ScalingMetricsReport)
        c6_reps = [r for r in [r_metrics, r_arch] if r is not None]
        c6_scores = [r.score for r in c6_reps]
        c6_score = sum(c6_scores) / len(c6_scores) if c6_scores else 100.0

        category_scores: List[CategoryScore] = [
            CategoryScore(category="Scaling Correctness", weight=0.25, score=round(c1_score, 2), weighted_score=round(c1_score * 0.25, 2), description="Worker elasticity, stateless API scaling, and decision policy accuracy"),
            CategoryScore(category="Performance Preservation", weight=0.20, score=round(c2_score, 2), weighted_score=round(c2_score * 0.20, 2), description="Queue drain rate, scale-up latency recovery, and AI concurrency management"),
            CategoryScore(category="Failure Safety", weight=0.20, score=round(c3_score, 2), weighted_score=round(c3_score * 0.20, 2), description="Scale-down zero-loss safety, DB limit protection, and controller crash recovery"),
            CategoryScore(category="Cost Efficiency", weight=0.15, score=round(c4_score, 2), weighted_score=round(c4_score * 0.15, 2), description="Dynamic compute spend reduction and low per-document processing cost"),
            CategoryScore(category="Cloud Readiness", weight=0.10, score=round(c5_score, 2), weighted_score=round(c5_score * 0.10, 2), description="Kubernetes HPA and multi-cloud (AWS, GCP, Azure) autoscaling compatibility"),
            CategoryScore(category="Evidence Quality", weight=0.10, score=round(c6_score, 2), weighted_score=round(c6_score * 0.10, 2), description="Scaling metric telemetry coverage and architecture evidence completeness"),
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
            f"DocuTask Agent scored {overall_score:.2f}% across 6 autoscaling and elastic capacity dimensions, "
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

        return EnterpriseAutoscalingCertificationReport(
            verifier_id="VERIFY-3J.8.16-AUTOSCALING-CERTIFICATION",
            phase_id="3J.8.16",
            phase_name="Enterprise Autoscaling Certification",
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
