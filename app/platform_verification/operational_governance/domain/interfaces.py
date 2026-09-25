"""
Phase 3H.8: Domain Interfaces for Operational Governance Verification
"""
from abc import ABC, abstractmethod
from .models import (
    ChangeGovernanceReport,
    ConfigurationChangeReport,
    DeploymentSafetyReport,
    DatabaseChangeReport,
    AIModelChangeReport,
    ApprovalWorkflowReport,
    RollbackVerificationReport,
    AuditTrailReport,
    ContinuousVerificationReport,
    GovernanceDashboardReport,
    OperationalGovernanceScorecard,
)


class IChangeGovernanceVerifier(ABC):
    @abstractmethod
    def verify_change_governance(self) -> ChangeGovernanceReport:
        pass


class IConfigurationChangeVerifier(ABC):
    @abstractmethod
    def verify_configuration_changes(self) -> ConfigurationChangeReport:
        pass


class IDeploymentSafetyVerifier(ABC):
    @abstractmethod
    def verify_deployment_safety(self) -> DeploymentSafetyReport:
        pass


class IDatabaseChangeVerifier(ABC):
    @abstractmethod
    def verify_database_changes(self) -> DatabaseChangeReport:
        pass


class IAIModelChangeVerifier(ABC):
    @abstractmethod
    def verify_ai_model_changes(self) -> AIModelChangeReport:
        pass


class IApprovalWorkflowVerifier(ABC):
    @abstractmethod
    def verify_approval_workflows(self) -> ApprovalWorkflowReport:
        pass


class IRollbackVerificationVerifier(ABC):
    @abstractmethod
    def verify_automated_rollbacks(self) -> RollbackVerificationReport:
        pass


class IAuditTrailVerifier(ABC):
    @abstractmethod
    def verify_audit_trails(self) -> AuditTrailReport:
        pass


class IContinuousVerificationVerifier(ABC):
    @abstractmethod
    def verify_continuous_operations(self) -> ContinuousVerificationReport:
        pass


class IGovernanceDashboardVerifier(ABC):
    @abstractmethod
    def generate_governance_dashboard(self) -> GovernanceDashboardReport:
        pass


class IOperationalGovernanceScorer(ABC):
    @abstractmethod
    def calculate_scorecard(
        self,
        change_report: ChangeGovernanceReport,
        config_report: ConfigurationChangeReport,
        deploy_report: DeploymentSafetyReport,
        db_report: DatabaseChangeReport,
        ai_report: AIModelChangeReport,
        approval_report: ApprovalWorkflowReport,
        rollback_report: RollbackVerificationReport,
        audit_report: AuditTrailReport,
        continuous_report: ContinuousVerificationReport,
        dashboard_report: GovernanceDashboardReport,
    ) -> OperationalGovernanceScorecard:
        pass
