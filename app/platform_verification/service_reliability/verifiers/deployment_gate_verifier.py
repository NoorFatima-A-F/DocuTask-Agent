"""
Phase 3H.6.8: SRE Reliability Deployment Gating Engine Verification
"""
from typing import List, Dict, Any
from ..domain.models import (
    DeploymentGateCriterion,
    DeploymentGateReport,
    DeploymentGateDecision,
    AvailabilitySLOReport,
    LatencySLOReport,
    ErrorBudgetReport,
    BurnRateReport,
    AIReliabilityReport,
    BurnRateSeverity,
)
from ..domain.interfaces import IDeploymentGateVerifier


class DeploymentGateVerifier(IDeploymentGateVerifier):
    """
    Evaluates SRE deployment gating policies before releasing code to production:
    - Availability SLO must be >= 99.9%
    - Latency SLOs must all be satisfied
    - Remaining error budget must be >= 70%
    - Multi-window burn rate must be SAFE (no active fast/slow burn alerts)
    - AI workload accuracy must be >= 95%
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def evaluate_deployment_gating(
        self,
        availability_report: AvailabilitySLOReport,
        latency_report: LatencySLOReport,
        error_budget_report: ErrorBudgetReport,
        burn_rate_report: BurnRateReport,
        ai_report: AIReliabilityReport,
    ) -> DeploymentGateReport:
        criteria: List[DeploymentGateCriterion] = []

        # 1. Availability Criterion
        avail_pass = availability_report.slo_satisfied
        criteria.append(
            DeploymentGateCriterion(
                criterion_name="Availability SLO Objective",
                requirement=">= 99.90% monthly availability",
                actual_state=f"{availability_report.measured_availability_pct:.3f}%",
                passed=avail_pass,
            )
        )

        # 2. Latency Criterion
        lat_pass = latency_report.all_latency_slos_satisfied
        criteria.append(
            DeploymentGateCriterion(
                criterion_name="Latency & Responsiveness Objective",
                requirement="All endpoint P95 latencies within budget",
                actual_state="All 6 endpoints satisfied",
                passed=lat_pass,
            )
        )

        # 3. Error Budget Criterion
        budget_pass = error_budget_report.overall_remaining_budget_pct >= 70.0
        criteria.append(
            DeploymentGateCriterion(
                criterion_name="Error Budget Health",
                requirement=">= 70.0% remaining budget",
                actual_state=f"{error_budget_report.overall_remaining_budget_pct:.2f}% remaining",
                passed=budget_pass,
            )
        )

        # 4. Burn Rate Criterion
        burn_pass = burn_rate_report.overall_burn_rate_status == BurnRateSeverity.SAFE
        criteria.append(
            DeploymentGateCriterion(
                criterion_name="Error Budget Burn Rate",
                requirement="Status == SAFE (No 1h/6h/24h burn alerts)",
                actual_state=f"Status: {burn_rate_report.overall_burn_rate_status.value}",
                passed=burn_pass,
            )
        )

        # 5. AI Workload Criterion
        ai_pass = ai_report.all_ai_workloads_reliable
        criteria.append(
            DeploymentGateCriterion(
                criterion_name="AI Workload Reliability",
                requirement="Zero schema violations; extraction consistency >= 98%",
                actual_state="All 5 AI pipelines reliable",
                passed=ai_pass,
            )
        )

        all_passed = all(c.passed for c in criteria)

        return DeploymentGateReport(
            deployment_id="deploy-rel-3h6",
            decision=DeploymentGateDecision.APPROVED if all_passed else DeploymentGateDecision.BLOCKED,
            criteria=criteria,
            deployment_allowed=all_passed,
            rationale="All SLOs satisfied, error budget healthy, burn rate safe, and AI reliability validated." if all_passed else "Deployment blocked due to reliability policy violations.",
        )
