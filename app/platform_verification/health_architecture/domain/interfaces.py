"""
Abstract Interfaces for Health Check Architecture Framework (Part 3H.1).
"""
from abc import ABC, abstractmethod
from app.platform_verification.health_architecture.domain.models import (
    HealthStateModelReport,
    HealthContractReport,
    DependencyGraphReport,
    FailurePolicyReport,
    SecurityAuditReport,
    AutomationIntegrationReport,
    HealthScorecard,
)


class IHealthStateMachine(ABC):
    @abstractmethod
    def verify_state_model(self) -> HealthStateModelReport:
        pass


class IHealthContractManager(ABC):
    @abstractmethod
    def validate_contracts(self) -> HealthContractReport:
        pass


class IDependencyGraphManager(ABC):
    @abstractmethod
    def generate_dependency_graph(self) -> DependencyGraphReport:
        pass


class IFailurePolicyManager(ABC):
    @abstractmethod
    def verify_failure_policies(self) -> FailurePolicyReport:
        pass


class ISecurityAuditor(ABC):
    @abstractmethod
    def audit_security(self) -> SecurityAuditReport:
        pass


class IAutomationIntegrationVerifier(ABC):
    @abstractmethod
    def verify_automation_integration(self) -> AutomationIntegrationReport:
        pass


class IHealthScoreEngine(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        model: HealthStateModelReport,
        contract: HealthContractReport,
        deps: DependencyGraphReport,
        policy: FailurePolicyReport,
        sec: SecurityAuditReport,
        auto: AutomationIntegrationReport,
    ) -> HealthScorecard:
        pass
