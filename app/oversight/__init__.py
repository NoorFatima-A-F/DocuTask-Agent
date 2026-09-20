"""Enterprise Human Oversight, Approval & AI Decision Intervention Platform (EHOC).

This package provides a centralized AI autonomy control plane, multi-level approval chains,
evidence packages, reviewer authority management, hierarchical escalations, and controlled human overrides.
"""

from .core.context import OversightContext
from .core.decisions import HumanDecision, DecisionOutcome, FeedbackAssessment
from .core.exceptions import (
    OversightException,
    UnauthorizedReviewerError,
    InvalidOverrideError,
    EscalationTimeoutError,
    ApprovalPolicyViolationError,
)
from .core.engine import HumanOversightEngine

from .approvals.models import (
    ApprovalPolicyType,
    StepExecutionStatus,
    ApprovalStep,
    ApprovalStrategy,
    ApprovalChain,
)
from .approvals.lifecycle import ApprovalLifecycleState
from .approvals.policies import (
    ApprovalPolicyCondition,
    ApprovalPolicy,
    ApprovalPolicyEngine,
)
from .approvals.service import ApprovalService

from .reviews.requests import ReviewRequest, ReviewPriority
from .reviews.evidence import ReviewEvidencePackage, SourceCitation
from .reviews.comments import ReviewComment
from .reviews.assignments import (
    Reviewer,
    ReviewerAuthority,
    ReviewerAssignmentEngine,
)

from .workflows.state_machine import ApprovalStateMachine, StateTransitionEvent
from .workflows.approval_flow import ApprovalWorkflowEngine

from .escalation.rules import EscalationLevel, EscalationRule
from .escalation.handlers import EscalationHandler, EscalationEvent
from .escalation.engine import EscalationEngine

from .overrides.policies import OverridePolicy
from .overrides.validation import OverrideValidator
from .overrides.service import OverrideService, HumanOverrideRecord

from .notifications.channels import NotificationChannel, NotificationEventType
from .notifications.dispatcher import NotificationMessage, NotificationDispatcher

from .analytics.metrics import OversightMetricsCollector, OversightAnalyticsSummary

from .sdk.client import OversightSDK
from .sdk.decorators import require_oversight

from .api.routes import router as oversight_router

__all__ = [
    # Core
    "OversightContext",
    "HumanDecision",
    "DecisionOutcome",
    "FeedbackAssessment",
    "OversightException",
    "UnauthorizedReviewerError",
    "InvalidOverrideError",
    "EscalationTimeoutError",
    "ApprovalPolicyViolationError",
    "HumanOversightEngine",
    # Approvals
    "ApprovalPolicyType",
    "StepExecutionStatus",
    "ApprovalStep",
    "ApprovalStrategy",
    "ApprovalChain",
    "ApprovalLifecycleState",
    "ApprovalPolicyCondition",
    "ApprovalPolicy",
    "ApprovalPolicyEngine",
    "ApprovalService",
    # Reviews
    "ReviewRequest",
    "ReviewPriority",
    "ReviewEvidencePackage",
    "SourceCitation",
    "ReviewComment",
    "Reviewer",
    "ReviewerAuthority",
    "ReviewerAssignmentEngine",
    # Workflows
    "ApprovalStateMachine",
    "StateTransitionEvent",
    "ApprovalWorkflowEngine",
    # Escalation
    "EscalationLevel",
    "EscalationRule",
    "EscalationHandler",
    "EscalationEvent",
    "EscalationEngine",
    # Overrides
    "OverridePolicy",
    "OverrideValidator",
    "OverrideService",
    "HumanOverrideRecord",
    # Notifications
    "NotificationChannel",
    "NotificationEventType",
    "NotificationMessage",
    "NotificationDispatcher",
    # Analytics
    "OversightMetricsCollector",
    "OversightAnalyticsSummary",
    # SDK
    "OversightSDK",
    "require_oversight",
    # API
    "oversight_router",
]
