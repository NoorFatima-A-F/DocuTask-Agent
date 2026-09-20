"""Abstract interfaces for Autonomous Health Remediation sub-engines."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
    RemediationPolicyReport,
    FailureContext,
    RemediationDecision,
    SafetyCheckResult,
    ActionExecutionReport,
    ExecutionLogEntry,
    RecoveryValidationReport,
    RollbackReport,
    SelfHealingTestReport,
    RemediationMetricsReport,
    RemediationSecurityReport,
    AutonomousRemediationScorecard,
)


class IRemediationPolicyEngine(ABC):
    """Interface for evaluating and registering remediation policies (3H.4.3.2)."""

    @abstractmethod
    def get_policy_report(self) -> RemediationPolicyReport:
        pass


class IActionClassifier(ABC):
    """Interface for classifying recovery actions into Levels 0 - 3 (3H.4.3.3)."""

    @abstractmethod
    def classify_action(self, action_name: str) -> Dict[str, Any]:
        pass


class IRecoveryDecisionEngine(ABC):
    """Interface for planning automated recovery decisions (3H.4.3.4)."""

    @abstractmethod
    def make_decision(self, context: FailureContext) -> RemediationDecision:
        pass


class ISafetyGuard(ABC):
    """Interface for safety guard and blast radius validation (3H.4.3.5)."""

    @abstractmethod
    def validate_safety(self, decision: RemediationDecision) -> SafetyCheckResult:
        pass


class IRemediationExecutor(ABC):
    """Interface for executing approved remediation operations (3H.4.3.6)."""

    @abstractmethod
    def execute_remediation(self, decision: RemediationDecision) -> ExecutionLogEntry:
        pass

    @abstractmethod
    def get_execution_report(self) -> ActionExecutionReport:
        pass


class IRecoveryValidator(ABC):
    """Interface for verifying post-remediation health restoration (3H.4.3.7)."""

    @abstractmethod
    def validate_recovery(self, execution_entry: ExecutionLogEntry) -> RecoveryValidationReport:
        pass


class IRollbackManager(ABC):
    """Interface for managing failure rollbacks and audit logs (3H.4.3.8)."""

    @abstractmethod
    def trigger_rollback(self, execution_entry: ExecutionLogEntry) -> RollbackReport:
        pass


class ISelfHealingScenariosVerifier(ABC):
    """Interface for verifying 5 real-world self-healing chaos scenarios (3H.4.3.9)."""

    @abstractmethod
    def verify_scenarios(self) -> SelfHealingTestReport:
        pass


class IRemediationMetricsCollector(ABC):
    """Interface for tracking MTTR, MTTD, and automation success rate (3H.4.3.10)."""

    @abstractmethod
    def collect_metrics(self) -> RemediationMetricsReport:
        pass


class IRemediationSecurityAuditor(ABC):
    """Interface for security, RBAC, and command whitelisting audit (3H.4.3.11)."""

    @abstractmethod
    def audit_security(self) -> RemediationSecurityReport:
        pass


class IAutonomousRemediationScorer(ABC):
    """Interface for calculating 6-dimension weighted self-healing scorecard (3H.4.3.14)."""

    @abstractmethod
    def score_remediation(
        self,
        policy_rep: RemediationPolicyReport,
        exec_rep: ActionExecutionReport,
        val_rep: RecoveryValidationReport,
        roll_rep: RollbackReport,
        scen_rep: SelfHealingTestReport,
        metrics_rep: RemediationMetricsReport,
        sec_rep: RemediationSecurityReport,
    ) -> AutonomousRemediationScorecard:
        pass


class IRemediationEvidenceExporter(ABC):
    """Interface for exporting structured audit manifests (3H.4.3.13)."""

    @abstractmethod
    def export_all(
        self,
        policy_rep: RemediationPolicyReport,
        exec_rep: ActionExecutionReport,
        val_rep: RecoveryValidationReport,
        roll_rep: RollbackReport,
        scen_rep: SelfHealingTestReport,
        metrics_rep: RemediationMetricsReport,
        sec_rep: RemediationSecurityReport,
        scorecard: AutonomousRemediationScorecard,
    ) -> Dict[str, str]:
        pass
