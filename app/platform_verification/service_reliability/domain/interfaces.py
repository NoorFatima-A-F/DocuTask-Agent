"""
Phase 3H.6: Domain Interfaces for Service Level Objectives & Reliability Verification
"""
from abc import ABC, abstractmethod
from .models import (
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
)


class ISLOArchitectureVerifier(ABC):
    @abstractmethod
    def verify_slo_architecture(self) -> SLOArchitectureReport:
        pass


class ISLICollectorVerifier(ABC):
    @abstractmethod
    def collect_subsystem_slis(self) -> SLICollectionReport:
        pass


class IAvailabilitySLOVerifier(ABC):
    @abstractmethod
    def verify_availability_slo(self) -> AvailabilitySLOReport:
        pass


class ILatencySLOVerifier(ABC):
    @abstractmethod
    def verify_latency_slos(self) -> LatencySLOReport:
        pass


class IErrorBudgetVerifier(ABC):
    @abstractmethod
    def verify_error_budgets(self) -> ErrorBudgetReport:
        pass


class IBurnRateVerifier(ABC):
    @abstractmethod
    def analyze_burn_rates(self) -> BurnRateReport:
        pass


class IReliabilityComplianceVerifier(ABC):
    @abstractmethod
    def verify_reliability_compliance(self) -> ReliabilityComplianceReport:
        pass


class IDeploymentGateVerifier(ABC):
    @abstractmethod
    def evaluate_deployment_gating(
        self,
        availability_report: AvailabilitySLOReport,
        latency_report: LatencySLOReport,
        error_budget_report: ErrorBudgetReport,
        burn_rate_report: BurnRateReport,
        ai_report: AIReliabilityReport,
    ) -> DeploymentGateReport:
        pass


class IExecutiveDashboardVerifier(ABC):
    @abstractmethod
    def generate_executive_dashboards(self) -> ReliabilityDashboardReport:
        pass


class IHistoricalTrendVerifier(ABC):
    @abstractmethod
    def analyze_historical_trends(self) -> HistoricalReliabilityReport:
        pass


class IAIReliabilityVerifier(ABC):
    @abstractmethod
    def verify_ai_workload_reliability(self) -> AIReliabilityReport:
        pass


class IServiceReliabilityScorer(ABC):
    @abstractmethod
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
        pass
