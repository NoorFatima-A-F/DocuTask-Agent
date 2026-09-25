"""Enterprise Autonomous Health Remediation & Recovery Action Framework.

Part 3H.4.3 for DocuTask Agent.
"""

from .runtime.autonomous_remediation_runtime import AutonomousRemediationRuntime
from .domain.models import (
    ActionLevel,
    RemediationRisk,
    ExecutionApproval,
    RemediationStatus,
    SelfHealingTier,
    RemediationPolicyItem,
    RemediationPolicyReport,
    FailureContext,
    RemediationDecision,
    SafetyCheckResult,
    ExecutionLogEntry,
    ActionExecutionReport,
    RecoveryValidationResult,
    RecoveryValidationReport,
    RollbackRecord,
    RollbackReport,
    SelfHealingScenarioResult,
    SelfHealingTestReport,
    RemediationMetricsReport,
    RemediationSecurityCheck,
    RemediationSecurityReport,
    AutonomousRemediationScorecard,
)

__all__ = [
    "AutonomousRemediationRuntime",
    "ActionLevel",
    "RemediationRisk",
    "ExecutionApproval",
    "RemediationStatus",
    "SelfHealingTier",
    "RemediationPolicyItem",
    "RemediationPolicyReport",
    "FailureContext",
    "RemediationDecision",
    "SafetyCheckResult",
    "ExecutionLogEntry",
    "ActionExecutionReport",
    "RecoveryValidationResult",
    "RecoveryValidationReport",
    "RollbackRecord",
    "RollbackReport",
    "SelfHealingScenarioResult",
    "SelfHealingTestReport",
    "RemediationMetricsReport",
    "RemediationSecurityCheck",
    "RemediationSecurityReport",
    "AutonomousRemediationScorecard",
]
