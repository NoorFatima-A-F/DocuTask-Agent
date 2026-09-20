"""
Phase 3I.10: Observability Intelligence Governance, Reliability Automation Maturity & Enterprise Operations Certification — Domain Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

from app.platform_verification.observability_operations_governance.domain.models import (
    GovernanceArchitectureReport,
    ObservabilityPolicyReport,
    ReliabilityMaturityReport,
    SREManagementReport,
    RunbookAutomationReport,
    AutomationSafetyGovernanceReport,
    ChangeManagementReport,
    IncidentGovernanceReport,
    ContinuousImprovementReport,
    OperationsDashboardReport,
    EnterpriseOperationsCertificationReport,
)


class IGovernanceArchitectureVerifier(ABC):
    @abstractmethod
    def verify(self) -> GovernanceArchitectureReport:
        """Verify governance architecture, policy engine, audit system, and review engine."""
        pass


class IObservabilityPolicyVerifier(ABC):
    @abstractmethod
    def verify(self) -> ObservabilityPolicyReport:
        """Verify alert policies, automation permissions, and escalation policies."""
        pass


class IReliabilityMaturityVerifier(ABC):
    @abstractmethod
    def verify(self) -> ReliabilityMaturityReport:
        """Evaluate platform reliability maturity across all dimensions up to Level 5 Autonomous."""
        pass


class ISREManagementVerifier(ABC):
    @abstractmethod
    def verify(self) -> SREManagementReport:
        """Verify SLO tracking, 30-day rolling error budgets, and burn rate management."""
        pass


class IRunbookAutomationVerifier(ABC):
    @abstractmethod
    def verify(self) -> RunbookAutomationReport:
        """Verify executable automated runbooks for service, DB, queue, and AI fallback recovery."""
        pass


class IAutomationSafetyVerifier(ABC):
    @abstractmethod
    def verify(self) -> AutomationSafetyGovernanceReport:
        """Verify action risk tiering, human approval gates, and rollback capabilities."""
        pass


class IChangeManagementVerifier(ABC):
    @abstractmethod
    def verify(self) -> ChangeManagementReport:
        """Verify pre/post deployment checks, canary rollouts, and blast radius controls."""
        pass


class IIncidentGovernanceVerifier(ABC):
    @abstractmethod
    def verify(self) -> IncidentGovernanceReport:
        """Verify end-to-end incident lifecycle, MTTR/MTTD, and automated postmortems."""
        pass


class IContinuousImprovementVerifier(ABC):
    @abstractmethod
    def verify(self) -> ContinuousImprovementReport:
        """Verify postmortem action tracking, zero recurrence SLA, and reliability trends."""
        pass


class IOperationsDashboardVerifier(ABC):
    @abstractmethod
    def verify(self) -> OperationsDashboardReport:
        """Verify Executive, Engineering, and AI Operations dashboard tiers."""
        pass


class IOperationsCertificationScorer(ABC):
    @abstractmethod
    def compute_certification(self, verification_results: Dict[str, Any]) -> EnterpriseOperationsCertificationReport:
        """Compute the 6-pillar weighted score and generate the enterprise certification report."""
        pass


class IObservabilityGovernanceExporter(ABC):
    @abstractmethod
    def export(self, verification_results: Dict[str, Any], certification_report: EnterpriseOperationsCertificationReport) -> Dict[str, str]:
        """Export all verification manifests and signed metadata.json."""
        pass
