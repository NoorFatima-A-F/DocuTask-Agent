"""
Phase 3I.6: Observability Governance, SLO Engineering & Reliability Certification — Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import (
    ReliabilityGovernanceReport,
    SLIReport,
    SLOReport,
    ErrorBudgetReport,
    ReliabilityDashboardReport,
    ReliabilityTrendReport,
    ProductionGateReport,
    ReliabilityRegressionReport,
    TelemetryQualityReport,
    ReliabilityAutomationReport,
    ReliabilityCertificationReport,
)


class IGovernanceArchitectureVerifier(ABC):
    @abstractmethod
    def verify_governance_architecture(self) -> ReliabilityGovernanceReport:
        pass


class ISLIDefinitionVerifier(ABC):
    @abstractmethod
    def verify_slis(self) -> SLIReport:
        pass


class ISLOEngineeringVerifier(ABC):
    @abstractmethod
    def verify_slos(self) -> SLOReport:
        pass


class IErrorBudgetVerifier(ABC):
    @abstractmethod
    def verify_error_budgets(self) -> ErrorBudgetReport:
        pass


class IReliabilityDashboardVerifier(ABC):
    @abstractmethod
    def verify_reliability_dashboards(self) -> ReliabilityDashboardReport:
        pass


class IReliabilityTrendVerifier(ABC):
    @abstractmethod
    def verify_reliability_trends(self) -> ReliabilityTrendReport:
        pass


class IProductionReadinessGateVerifier(ABC):
    @abstractmethod
    def verify_production_gates(self) -> ProductionGateReport:
        pass


class IReliabilityRegressionVerifier(ABC):
    @abstractmethod
    def verify_reliability_regression(self) -> ReliabilityRegressionReport:
        pass


class ITelemetryQualityVerifier(ABC):
    @abstractmethod
    def verify_telemetry_quality(self) -> TelemetryQualityReport:
        pass


class IReliabilityAutomationVerifier(ABC):
    @abstractmethod
    def verify_reliability_automation(self) -> ReliabilityAutomationReport:
        pass


class IReliabilityQualityScorer(ABC):
    @abstractmethod
    def calculate_certification_score(
        self,
        gov_report: ReliabilityGovernanceReport,
        sli_report: SLIReport,
        slo_report: SLOReport,
        budget_report: ErrorBudgetReport,
        dash_report: ReliabilityDashboardReport,
        trend_report: ReliabilityTrendReport,
        gate_report: ProductionGateReport,
        reg_report: ReliabilityRegressionReport,
        qual_report: TelemetryQualityReport,
        auto_report: ReliabilityAutomationReport,
    ) -> ReliabilityCertificationReport:
        pass


class IReliabilityEvidenceExporter(ABC):
    @abstractmethod
    def export_all_reports(
        self,
        output_dir: str,
        gov_report: ReliabilityGovernanceReport,
        sli_report: SLIReport,
        slo_report: SLOReport,
        budget_report: ErrorBudgetReport,
        dash_report: ReliabilityDashboardReport,
        trend_report: ReliabilityTrendReport,
        gate_report: ProductionGateReport,
        reg_report: ReliabilityRegressionReport,
        qual_report: TelemetryQualityReport,
        auto_report: ReliabilityAutomationReport,
        certification_report: ReliabilityCertificationReport,
    ) -> Dict[str, Any]:
        pass
