"""
Phase 3H.6: Enterprise Service Level Objectives & Reliability Runtime Orchestrator
"""
from typing import Dict, Any, Optional

from ..verifiers import (
    SLOArchitectureVerifier,
    SLICollectorVerifier,
    AvailabilitySLOVerifier,
    LatencySLOVerifier,
    ErrorBudgetVerifier,
    BurnRateVerifier,
    ReliabilityComplianceVerifier,
    DeploymentGateVerifier,
    ExecutiveDashboardVerifier,
    HistoricalTrendVerifier,
    AIWorkloadReliabilityVerifier,
)
from ..scoring import ServiceReliabilityScorer
from ..exporter import ServiceReliabilityExporter
from ..domain.models import ServiceReliabilityScorecard


class ServiceReliabilityRuntime:
    """
    Main runtime orchestrator for executing Phase 3H.6:
    - Verifies formal SLO architecture across 8 subsystems
    - Collects multi-subsystem SLI metrics
    - Verifies 99.9% availability across normal, peak, and degraded traffic
    - Measures endpoint latency percentiles (P50, P90, P95, P99)
    - Manages 30-day error budgets and multi-window burn rates (1h, 6h, 24h, 3d)
    - Verifies end-to-end reliability compliance
    - Evaluates automated SRE deployment gate policies
    - Generates multi-persona executive reliability dashboards
    - Tracks historical stability trends across 24h/7d/30d/90d
    - Verifies AI workload reliability (OCR, LLM, schemas, hallucination recovery)
    - Computes master 7-pillar SRE certification scorecard
    - Exports 13 standardized JSON evidence artifacts with SHA-256 signatures
    """

    def __init__(
        self,
        output_dir: str = "service_reliability_verification",
        slo_verifier: Optional[SLOArchitectureVerifier] = None,
        sli_verifier: Optional[SLICollectorVerifier] = None,
        availability_verifier: Optional[AvailabilitySLOVerifier] = None,
        latency_verifier: Optional[LatencySLOVerifier] = None,
        error_budget_verifier: Optional[ErrorBudgetVerifier] = None,
        burn_rate_verifier: Optional[BurnRateVerifier] = None,
        compliance_verifier: Optional[ReliabilityComplianceVerifier] = None,
        gate_verifier: Optional[DeploymentGateVerifier] = None,
        dashboard_verifier: Optional[ExecutiveDashboardVerifier] = None,
        historical_verifier: Optional[HistoricalTrendVerifier] = None,
        ai_verifier: Optional[AIWorkloadReliabilityVerifier] = None,
        scorer: Optional[ServiceReliabilityScorer] = None,
        exporter: Optional[ServiceReliabilityExporter] = None,
    ):
        self.output_dir = output_dir
        self.slo_verifier = slo_verifier or SLOArchitectureVerifier()
        self.sli_verifier = sli_verifier or SLICollectorVerifier()
        self.availability_verifier = availability_verifier or AvailabilitySLOVerifier()
        self.latency_verifier = latency_verifier or LatencySLOVerifier()
        self.error_budget_verifier = error_budget_verifier or ErrorBudgetVerifier()
        self.burn_rate_verifier = burn_rate_verifier or BurnRateVerifier()
        self.compliance_verifier = compliance_verifier or ReliabilityComplianceVerifier()
        self.gate_verifier = gate_verifier or DeploymentGateVerifier()
        self.dashboard_verifier = dashboard_verifier or ExecutiveDashboardVerifier()
        self.historical_verifier = historical_verifier or HistoricalTrendVerifier()
        self.ai_verifier = ai_verifier or AIWorkloadReliabilityVerifier()
        self.scorer = scorer or ServiceReliabilityScorer()
        self.exporter = exporter or ServiceReliabilityExporter(output_dir=self.output_dir)

    def run_full_reliability_verification(self) -> Dict[str, Any]:
        # Step 1: Execute all verifications
        slo_report = self.slo_verifier.verify_slo_architecture()
        sli_report = self.sli_verifier.collect_subsystem_slis()
        availability_report = self.availability_verifier.verify_availability_slo()
        latency_report = self.latency_verifier.verify_latency_slos()
        error_budget_report = self.error_budget_verifier.verify_error_budgets()
        burn_rate_report = self.burn_rate_verifier.analyze_burn_rates()
        compliance_report = self.compliance_verifier.verify_reliability_compliance()
        dashboard_report = self.dashboard_verifier.generate_executive_dashboards()
        historical_report = self.historical_verifier.analyze_historical_trends()
        ai_report = self.ai_verifier.verify_ai_workload_reliability()

        # Step 2: Evaluate deployment gate based on verified SLOs and budgets
        gate_report = self.gate_verifier.evaluate_deployment_gating(
            availability_report=availability_report,
            latency_report=latency_report,
            error_budget_report=error_budget_report,
            burn_rate_report=burn_rate_report,
            ai_report=ai_report,
        )

        # Step 3: Compute Master SRE Reliability Scorecard
        scorecard: ServiceReliabilityScorecard = self.scorer.calculate_scorecard(
            slo_report=slo_report,
            sli_report=sli_report,
            availability_report=availability_report,
            latency_report=latency_report,
            error_budget_report=error_budget_report,
            burn_rate_report=burn_rate_report,
            compliance_report=compliance_report,
            gate_report=gate_report,
            dashboard_report=dashboard_report,
            historical_report=historical_report,
            ai_report=ai_report,
        )

        # Step 4: Export evidence artifacts and SHA-256 metadata manifest
        exported_files = self.exporter.export_all(
            slo_report=slo_report,
            sli_report=sli_report,
            availability_report=availability_report,
            latency_report=latency_report,
            error_budget_report=error_budget_report,
            burn_rate_report=burn_rate_report,
            compliance_report=compliance_report,
            gate_report=gate_report,
            dashboard_report=dashboard_report,
            historical_report=historical_report,
            ai_report=ai_report,
            scorecard=scorecard,
        )

        return {
            "scorecard": scorecard,
            "slo_report": slo_report,
            "sli_report": sli_report,
            "availability_report": availability_report,
            "latency_report": latency_report,
            "error_budget_report": error_budget_report,
            "burn_rate_report": burn_rate_report,
            "compliance_report": compliance_report,
            "gate_report": gate_report,
            "dashboard_report": dashboard_report,
            "historical_report": historical_report,
            "ai_report": ai_report,
            "exported_files": exported_files,
        }
