"""
Phase 3R: Abstract Interfaces and Protocols for Enterprise Operations Governance.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .models import (
    AIOpsReport,
    AlertReport,
    AuditTrailReport,
    ChangeManagementReport,
    ErrorBudgetReport,
    FinOpsReport,
    IncidentReport,
    OperationalMaturityScore,
    OperationsManifest,
    ProductionHealthReport,
    RootCauseAnalysisReport,
    RunbookReport,
    SelfHealingReport,
    SLODefinitionReport,
)


class ISLOManager(ABC):
    @abstractmethod
    def evaluate_slos(self) -> SLODefinitionReport:
        pass


class IErrorBudgetManager(ABC):
    @abstractmethod
    def calculate_error_budget(self) -> ErrorBudgetReport:
        pass


class IHealthIntelligenceEngine(ABC):
    @abstractmethod
    def assess_production_health(self) -> ProductionHealthReport:
        pass


class IIncidentManager(ABC):
    @abstractmethod
    def get_incident_summary(self) -> IncidentReport:
        pass


class IAlertingEngine(ABC):
    @abstractmethod
    def evaluate_alert_rules(self) -> AlertReport:
        pass


class IRunbookEngine(ABC):
    @abstractmethod
    def validate_runbooks(self) -> RunbookReport:
        pass


class ISelfHealingEngine(ABC):
    @abstractmethod
    def execute_self_healing_verification(self) -> SelfHealingReport:
        pass


class IRootCauseAnalyzer(ABC):
    @abstractmethod
    def analyze_incident(self, incident_id: str = "INC-2026-001") -> RootCauseAnalysisReport:
        pass


class IChangeManager(ABC):
    @abstractmethod
    def audit_changes(self) -> ChangeManagementReport:
        pass


class IAuditTrailEngine(ABC):
    @abstractmethod
    def verify_audit_trail(self) -> AuditTrailReport:
        pass


class IAIOpsMonitor(ABC):
    @abstractmethod
    def monitor_ai_operations(self) -> AIOpsReport:
        pass


class IFinOpsMonitor(ABC):
    @abstractmethod
    def calculate_unit_economics(self) -> FinOpsReport:
        pass


class IOperationalMaturityScorer(ABC):
    @abstractmethod
    def score_maturity(self, operational_reports: Dict[str, Any]) -> OperationalMaturityScore:
        pass
