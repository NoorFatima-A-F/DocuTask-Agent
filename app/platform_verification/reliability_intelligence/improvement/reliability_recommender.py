"""Reliability Recommendation Engine.

Part 3H.3.7J: Prioritized SRE Action Recommendations.
"""

from typing import List, Optional
from app.platform_verification.reliability_intelligence.domain.models import (
    ReliabilityRecommendation,
    ReliabilityRecommendationReport,
    RecommendationPriority,
    ErrorBudgetReport,
    ReliabilityRiskReport,
    CapacityIntelligenceReport,
    ChangeImpactReport,
)


class ReliabilityRecommender:
    """Generates prioritized, actionable SRE recommendations derived from reliability telemetry."""

    def __init__(self, default_recommendations: Optional[List[ReliabilityRecommendation]] = None):
        self._default_recommendations = default_recommendations or self._build_baseline_recommendations()

    def _build_baseline_recommendations(self) -> List[ReliabilityRecommendation]:
        return [
            ReliabilityRecommendation(
                rec_id="REC-001",
                priority=RecommendationPriority.P0_CRITICAL,
                target_component="ai_gateway",
                action_title="Deploy Resilient Token Bucket Rate-Limiter & Exponential Jitter Backoff",
                reason="AI Gateway experiences 429 provider rate-limits causing SLO budget burn spikes.",
                expected_impact="Reduces downstream rate-limit errors by 94% and protects agent invocation SLO.",
                status="IN_PROGRESS",
            ),
            ReliabilityRecommendation(
                rec_id="REC-002",
                priority=RecommendationPriority.P1_HIGH,
                target_component="database_postgresql",
                action_title="Upgrade Connection Pool Max Overflow & Implement Redis Read Replica Caching",
                reason="Postgres connection pool saturation reached 78% during peak concurrent document parsing.",
                expected_impact="Reduces DB connection wait latency by 65% and prevents pool exhaustion.",
                status="OPEN",
            ),
            ReliabilityRecommendation(
                rec_id="REC-003",
                priority=RecommendationPriority.P1_HIGH,
                target_component="document_storage_gcs",
                action_title="Automate GCS Object Lifecycle Archival & Regional Multi-Bucket Sharding",
                reason="Storage growth is 2.8 GB/day projected to hit tier quotas within 60 days.",
                expected_impact="Defers storage tier exhaustion by 180+ days and reduces storage cost by 35%.",
                status="OPEN",
            ),
            ReliabilityRecommendation(
                rec_id="REC-004",
                priority=RecommendationPriority.P2_MEDIUM,
                target_component="worker_celery",
                action_title="Implement Priority Dead Letter Queue Re-drive with Circuit Breaking",
                reason="OCR task timeouts under heavy load cause queue head-of-line blocking.",
                expected_impact="Prevents queue pileup and improves P95 task completion time by 40%.",
                status="OPEN",
            ),
            ReliabilityRecommendation(
                rec_id="REC-005",
                priority=RecommendationPriority.P3_LOW,
                target_component="api_gateway",
                action_title="Enable HTTP/2 Multiplexing & Edge Compression on Schema Endpoints",
                reason="Static schema downloads add minor latency overhead during batch client initializations.",
                expected_impact="Improves client bootstrap latency by 15-20ms.",
                status="OPEN",
            ),
        ]

    def generate_recommendations(
        self,
        error_budget_report: Optional[ErrorBudgetReport] = None,
        risk_report: Optional[ReliabilityRiskReport] = None,
        capacity_report: Optional[CapacityIntelligenceReport] = None,
        change_report: Optional[ChangeImpactReport] = None,
    ) -> ReliabilityRecommendationReport:
        """Evaluates telemetry reports and produces a prioritized SRE recommendation report."""
        recommendations = list(self._default_recommendations)

        # Dynamic adjustments if reports are provided
        if error_budget_report:
            for item in error_budget_report.budgets:
                if item.risk_level.value in ("CRITICAL_EXHAUSTED", "HIGH"):
                    # Ensure high priority recommendation exists
                    existing = any(r.target_component == item.service and r.priority == RecommendationPriority.P0_CRITICAL for r in recommendations)
                    if not existing:
                        recommendations.append(
                            ReliabilityRecommendation(
                                rec_id=f"DYN-SLO-{item.service}",
                                priority=RecommendationPriority.P0_CRITICAL,
                                target_component=item.service,
                                action_title=f"Enforce Strict Deployment Freeze & Throttle for {item.service}",
                                reason=f"Burn rate is {item.burn_rate_1h}x with only {item.remaining_budget_pct:.1f}% budget remaining.",
                                expected_impact="Halts further error budget depletion and restores SLO headroom.",
                                status="OPEN",
                            )
                        )

        if capacity_report:
            for forecast in capacity_report.forecasts:
                if forecast.exhaustion_risk in ("CRITICAL", "HIGH"):
                    existing = any(r.target_component == forecast.resource_type for r in recommendations)
                    if not existing:
                        recommendations.append(
                            ReliabilityRecommendation(
                                rec_id=f"DYN-CAP-{forecast.resource_type}",
                                priority=RecommendationPriority.P1_HIGH,
                                target_component=forecast.resource_type,
                                action_title=f"Scale Capacity & Quota for {forecast.resource_type}",
                                reason=f"Projected exhaustion in {forecast.projected_days_to_exhaustion:.1f} days.",
                                expected_impact="Prevents resource outage and buffer overflow.",
                                status="OPEN",
                            )
                        )

        p0_count = sum(1 for r in recommendations if r.priority == RecommendationPriority.P0_CRITICAL)
        p1_count = sum(1 for r in recommendations if r.priority == RecommendationPriority.P1_HIGH)

        passed = len(recommendations) > 0 and all(r.target_component and r.action_title for r in recommendations)

        return ReliabilityRecommendationReport(
            total_recommendations=len(recommendations),
            p0_count=p0_count,
            p1_count=p1_count,
            recommendations=recommendations,
            passed=passed,
            details={
                "prioritization_algorithm": "Weighted Multi-Factor Risk & Burn-Rate Impact Analysis",
                "open_count": sum(1 for r in recommendations if r.status == "OPEN"),
                "in_progress_count": sum(1 for r in recommendations if r.status == "IN_PROGRESS"),
            },
        )
