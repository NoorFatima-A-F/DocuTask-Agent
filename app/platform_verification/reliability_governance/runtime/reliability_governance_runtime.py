"""
Phase 3I.6: Observability Governance, SLO Engineering & Reliability Certification Runtime
Orchestrates all verifiers, scoring engine, and evidence exporter.
"""
import logging
from typing import Dict, Any

from ..verifiers.governance_architecture_verifier import GovernanceArchitectureVerifier
from ..verifiers.sli_definition_verifier import SLIDefinitionVerifier
from ..verifiers.slo_engineering_verifier import SLOEngineeringVerifier
from ..verifiers.error_budget_verifier import ErrorBudgetVerifier
from ..verifiers.reliability_dashboard_verifier import ReliabilityDashboardVerifier
from ..verifiers.reliability_trend_verifier import ReliabilityTrendVerifier
from ..verifiers.production_readiness_gate_verifier import ProductionReadinessGateVerifier
from ..verifiers.reliability_regression_verifier import ReliabilityRegressionVerifier
from ..verifiers.telemetry_quality_verifier import TelemetryQualityVerifier
from ..verifiers.reliability_automation_verifier import ReliabilityAutomationVerifier
from ..scoring.reliability_quality_scorer import ReliabilityQualityScorer
from ..exporter.reliability_evidence_exporter import ReliabilityEvidenceExporter

logger = logging.getLogger(__name__)


class ReliabilityGovernanceRuntime:
    def __init__(
        self,
        output_dir: str = "observability_verification/reliability",
    ):
        self.output_dir = output_dir
        self.gov_verifier = GovernanceArchitectureVerifier()
        self.sli_verifier = SLIDefinitionVerifier()
        self.slo_verifier = SLOEngineeringVerifier()
        self.budget_verifier = ErrorBudgetVerifier()
        self.dash_verifier = ReliabilityDashboardVerifier()
        self.trend_verifier = ReliabilityTrendVerifier()
        self.gate_verifier = ProductionReadinessGateVerifier()
        self.reg_verifier = ReliabilityRegressionVerifier()
        self.qual_verifier = TelemetryQualityVerifier()
        self.auto_verifier = ReliabilityAutomationVerifier()
        self.scorer = ReliabilityQualityScorer()
        self.exporter = ReliabilityEvidenceExporter()

    def run_full_verification(self) -> Dict[str, Any]:
        logger.info("Starting Phase 3I.6 Observability Governance & Reliability Certification...")

        # 1. Execute all verification steps
        gov_report = self.gov_verifier.verify_governance_architecture()
        sli_report = self.sli_verifier.verify_slis()
        slo_report = self.slo_verifier.verify_slos()
        budget_report = self.budget_verifier.verify_error_budgets()
        dash_report = self.dash_verifier.verify_reliability_dashboards()
        trend_report = self.trend_verifier.verify_reliability_trends()
        gate_report = self.gate_verifier.verify_production_gates()
        reg_report = self.reg_verifier.verify_reliability_regression()
        qual_report = self.qual_verifier.verify_telemetry_quality()
        auto_report = self.auto_verifier.verify_reliability_automation()

        # 2. Score and certify
        cert_report = self.scorer.calculate_certification_score(
            gov_report=gov_report,
            sli_report=sli_report,
            slo_report=slo_report,
            budget_report=budget_report,
            dash_report=dash_report,
            trend_report=trend_report,
            gate_report=gate_report,
            reg_report=reg_report,
            qual_report=qual_report,
            auto_report=auto_report,
        )

        # 3. Export evidence files and metadata
        metadata = self.exporter.export_all_reports(
            output_dir=self.output_dir,
            gov_report=gov_report,
            sli_report=sli_report,
            slo_report=slo_report,
            budget_report=budget_report,
            dash_report=dash_report,
            trend_report=trend_report,
            gate_report=gate_report,
            reg_report=reg_report,
            qual_report=qual_report,
            auto_report=auto_report,
            certification_report=cert_report,
        )

        return {
            "status": "SUCCESS" if cert_report.certification_granted else "FAILED",
            "certification_tier": cert_report.certification_tier.value,
            "overall_score_pct": cert_report.overall_score_pct,
            "certification_granted": cert_report.certification_granted,
            "governance_report": gov_report.model_dump(mode="json"),
            "sli_report": sli_report.model_dump(mode="json"),
            "slo_report": slo_report.model_dump(mode="json"),
            "error_budget_report": budget_report.model_dump(mode="json"),
            "dashboard_report": dash_report.model_dump(mode="json"),
            "trend_report": trend_report.model_dump(mode="json"),
            "gate_report": gate_report.model_dump(mode="json"),
            "regression_report": reg_report.model_dump(mode="json"),
            "quality_report": qual_report.model_dump(mode="json"),
            "automation_report": auto_report.model_dump(mode="json"),
            "certification_report": cert_report.model_dump(mode="json"),
            "metadata": metadata,
        }
