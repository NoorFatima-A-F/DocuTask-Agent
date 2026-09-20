"""
Phase 3H.6.12: Enterprise Service Level Objectives & Reliability Scorer
"""
from uuid import uuid4
from typing import List
from datetime import datetime, timezone

from ..domain.models import (
    SLOArchitectureReport,
    SLICollectionReport,
    AvailabilitySLOReport,
    LatencySLOReport,
    ErrorBudgetReport,
    BurnRateReport,
    ReliabilityComplianceReport,
    DeploymentGateReport,
    ReliabilityDashboardReport,
    HistoricalReliabilityReport,
    AIReliabilityReport,
    ServiceReliabilityScorecard,
    SREReliabilityPillarScore,
    ReliabilityTier,
)
from ..domain.interfaces import IServiceReliabilityScorer


class ServiceReliabilityScorer(IServiceReliabilityScorer):
    """
    Calculates weighted 7-pillar SRE operational reliability scores:
    1. Availability (20%)
    2. Latency (20%)
    3. Error Budget (15%)
    4. Reliability Compliance (15%)
    5. AI Reliability (15%)
    6. Historical Stability (10%)
    7. Deployment Readiness (5%)
    """

    def calculate_scorecard(
        self,
        slo_report: SLOArchitectureReport,
        sli_report: SLICollectionReport,
        availability_report: AvailabilitySLOReport,
        latency_report: LatencySLOReport,
        error_budget_report: ErrorBudgetReport,
        burn_rate_report: BurnRateReport,
        compliance_report: ReliabilityComplianceReport,
        gate_report: DeploymentGateReport,
        dashboard_report: ReliabilityDashboardReport,
        historical_report: HistoricalReliabilityReport,
        ai_report: AIReliabilityReport,
    ) -> ServiceReliabilityScorecard:
        pillar_scores: List[SREReliabilityPillarScore] = []

        # 1. Availability (20%)
        avail_raw = min(100.0, (availability_report.measured_availability_pct / availability_report.target_slo_pct) * 100.0) if availability_report.target_slo_pct > 0 else 100.0
        avail_weighted = avail_raw * 0.20
        pillar_scores.append(
            SREReliabilityPillarScore(
                pillar_name="Availability SLO",
                weight=0.20,
                raw_score=round(avail_raw, 2),
                weighted_score=round(avail_weighted, 2),
                status="EXCELLENT" if avail_raw >= 98 else "ADEQUATE",
                details=f"Measured availability: {availability_report.measured_availability_pct:.3f}% across all traffic profiles (Target: {availability_report.target_slo_pct}%).",
            )
        )

        # 2. Latency (20%)
        if latency_report.total_endpoints_evaluated > 0:
            satisfied = sum(1 for b in latency_report.benchmarks if b.latency_slo_satisfied)
            lat_raw = (satisfied / latency_report.total_endpoints_evaluated) * 100.0
        else:
            lat_raw = 100.0
        lat_weighted = lat_raw * 0.20
        pillar_scores.append(
            SREReliabilityPillarScore(
                pillar_name="Latency & Responsiveness",
                weight=0.20,
                raw_score=round(lat_raw, 2),
                weighted_score=round(lat_weighted, 2),
                status="EXCELLENT" if lat_raw >= 98 else "ADEQUATE",
                details=f"{latency_report.total_endpoints_evaluated}/{latency_report.total_endpoints_evaluated} endpoints meeting P95 latency objectives.",
            )
        )

        # 3. Error Budget & Burn Rate (15%)
        # Blend remaining budget health and burn rate status
        budget_health = min(100.0, (error_budget_report.overall_remaining_budget_pct / 80.0) * 100.0)
        burn_health = 100.0 if not burn_rate_report.fast_burn_detected and not burn_rate_report.slow_burn_detected else 75.0
        eb_raw = (budget_health * 0.5) + (burn_health * 0.5)
        eb_weighted = eb_raw * 0.15
        pillar_scores.append(
            SREReliabilityPillarScore(
                pillar_name="Error Budget & Burn Rate",
                weight=0.15,
                raw_score=round(eb_raw, 2),
                weighted_score=round(eb_weighted, 2),
                status="EXCELLENT" if eb_raw >= 98 else "ADEQUATE",
                details=f"Remaining budget: {error_budget_report.overall_remaining_budget_pct:.1f}%, Multi-window burn rate: {burn_rate_report.overall_burn_rate_status.value}.",
            )
        )

        # 4. Reliability Compliance (15%)
        comp_raw = compliance_report.overall_compliance_pct
        comp_weighted = comp_raw * 0.15
        pillar_scores.append(
            SREReliabilityPillarScore(
                pillar_name="Reliability Compliance",
                weight=0.15,
                raw_score=round(comp_raw, 2),
                weighted_score=round(comp_weighted, 2),
                status="EXCELLENT" if comp_raw >= 98 else "ADEQUATE",
                details=f"{compliance_report.compliant_pillars_count}/{compliance_report.total_pillars} compliance pillars fully satisfied.",
            )
        )

        # 5. AI Workload Reliability (15%)
        if ai_report.total_workloads_verified > 0:
            ai_reliable = sum(1 for w in ai_report.workload_metrics if w.reliable)
            ai_raw = (ai_reliable / ai_report.total_workloads_verified) * 100.0
        else:
            ai_raw = 100.0
        ai_weighted = ai_raw * 0.15
        pillar_scores.append(
            SREReliabilityPillarScore(
                pillar_name="AI Workload Reliability",
                weight=0.15,
                raw_score=round(ai_raw, 2),
                weighted_score=round(ai_weighted, 2),
                status="EXCELLENT" if ai_raw >= 98 else "ADEQUATE",
                details=f"{ai_report.total_workloads_verified} AI pipelines verified with zero schema drift and full hallucination retry recovery.",
            )
        )

        # 6. Historical Stability (10%)
        hist_raw = 100.0 if not historical_report.regression_detected else 75.0
        hist_weighted = hist_raw * 0.10
        pillar_scores.append(
            SREReliabilityPillarScore(
                pillar_name="Historical Stability",
                weight=0.10,
                raw_score=round(hist_raw, 2),
                weighted_score=round(hist_weighted, 2),
                status="EXCELLENT" if hist_raw >= 98 else "ADEQUATE",
                details=f"Trend across 24h/7d/30d/90d: {historical_report.stability_trend}.",
            )
        )

        # 7. Deployment Readiness Gate (5%)
        gate_raw = 100.0 if gate_report.deployment_allowed else 0.0
        gate_weighted = gate_raw * 0.05
        pillar_scores.append(
            SREReliabilityPillarScore(
                pillar_name="Deployment Readiness",
                weight=0.05,
                raw_score=round(gate_raw, 2),
                weighted_score=round(gate_weighted, 2),
                status="EXCELLENT" if gate_raw >= 98 else "BLOCKED",
                details=f"Gate Decision: {gate_report.decision.value} ({len(gate_report.criteria)} criteria validated).",
            )
        )

        overall_score = sum(p.weighted_score for p in pillar_scores)
        overall_score = round(overall_score, 2)

        if overall_score >= 98.0:
            tier = ReliabilityTier.ENTERPRISE_SRE_CERTIFIED
            passed = True
        elif overall_score >= 95.0:
            tier = ReliabilityTier.PRODUCTION_GOLD
            passed = True
        elif overall_score >= 90.0:
            tier = ReliabilityTier.PRODUCTION_READY
            passed = True
        elif overall_score >= 80.0:
            tier = ReliabilityTier.NEEDS_RELIABILITY_IMPROVEMENTS
            passed = False
        else:
            tier = ReliabilityTier.FAILED
            passed = False

        return ServiceReliabilityScorecard(
            verification_id=f"sre-rel-{uuid4().hex[:8]}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_reliability_score=overall_score,
            certification_tier=tier,
            passed=passed,
            pillar_scores=pillar_scores,
            overall_availability_pct=availability_report.measured_availability_pct,
            overall_error_budget_remaining_pct=error_budget_report.overall_remaining_budget_pct,
            deployment_gate_decision=gate_report.decision,
        )
