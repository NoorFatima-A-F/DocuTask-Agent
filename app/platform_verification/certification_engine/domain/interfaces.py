"""
Abstract interfaces for Enterprise Verification Quality Gate & Certification Engine.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.platform_verification.certification_engine.domain.models import (
    ApprovalReview,
    CertificationDashboardView,
    CertificationLevel,
    CertificationRecord,
    ChangeImpactReport,
    ChangeType,
    ExceptionRequest,
    GateEvaluationResult,
    PolicyDefinition,
    QualityGateDecision,
    QualityGateDefinition,
    RiskAssessment,
)


class IPolicyEngine(ABC):
    """Evaluates declarative policies with boolean expressions and condition matching."""

    @abstractmethod
    def register_policy(self, policy: PolicyDefinition) -> None:
        """Registers a policy definition."""
        pass

    @abstractmethod
    def evaluate_policy(self, policy_id: str, metrics: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Evaluates a policy against metrics, returning (passed, failure_reasons)."""
        pass


class IRiskEngine(ABC):
    """Calculates risk scores and determines governance actions based on probability, impact, and exposure."""

    @abstractmethod
    def assess_risk(
        self,
        system_id: str,
        failed_gates: List[GateEvaluationResult],
        metrics: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> RiskAssessment:
        """Assesses total risk for an evaluation run."""
        pass


class IQualityGateEngine(ABC):
    """Executes configurable quality gates against execution metrics."""

    @abstractmethod
    def register_gate(self, gate: QualityGateDefinition) -> None:
        """Registers a quality gate."""
        pass

    @abstractmethod
    def evaluate_gates(
        self,
        gate_ids: List[str],
        metrics: Dict[str, Any],
        active_exceptions: Optional[List[ExceptionRequest]] = None,
    ) -> List[GateEvaluationResult]:
        """Evaluates a set of quality gates against metrics."""
        pass


class IDecisionEngine(ABC):
    """Coordinates policy, gates, risk, and exceptions to produce an explainable release decision."""

    @abstractmethod
    def make_release_decision(
        self,
        system_id: str,
        system_version: str,
        model_version: str,
        target_level: CertificationLevel,
        metrics: Dict[str, Any],
        gate_ids: List[str],
        policy_ids: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> QualityGateDecision:
        """Generates release decision with complete reasoning trace."""
        pass


class ICertificationEngine(ABC):
    """Manages formal certification lifecycle and cryptographic verification."""

    @abstractmethod
    def issue_certification(
        self,
        decision: QualityGateDecision,
        evidence_package_id: str,
        approved_by: str,
        validity_days: int = 90,
    ) -> CertificationRecord:
        """Issues a new certification record upon approved decision."""
        pass

    @abstractmethod
    def get_certification(self, certification_id: str) -> Optional[CertificationRecord]:
        """Retrieves certification record by ID."""
        pass

    @abstractmethod
    def verify_certification_validity(self, certification_id: str) -> bool:
        """Verifies integrity, status, and expiration of a certification."""
        pass

    @abstractmethod
    def revoke_certification(self, certification_id: str, reason: str, revoked_by: str) -> CertificationRecord:
        """Revokes an active certification."""
        pass


class IApprovalWorkflowManager(ABC):
    """Manages multi-role review and approval workflows."""

    @abstractmethod
    def submit_review(self, review: ApprovalReview) -> bool:
        """Submits a human approval or rejection review."""
        pass

    @abstractmethod
    def get_reviews_for_certification(self, certification_id: str) -> List[ApprovalReview]:
        """Returns all reviews submitted for a certification."""
        pass


class IExceptionManager(ABC):
    """Manages quality gate exceptions and temporary risk acceptances."""

    @abstractmethod
    def request_exception(self, request: ExceptionRequest) -> ExceptionRequest:
        """Submits an exception request."""
        pass

    @abstractmethod
    def approve_exception(self, exception_id: str, approver: str) -> ExceptionRequest:
        """Approves an exception request."""
        pass

    @abstractmethod
    def get_active_exceptions_for_system(self, system_id: str) -> List[ExceptionRequest]:
        """Retrieves non-expired approved exceptions for a system."""
        pass


class IChangeImpactAnalyzer(ABC):
    """Analyzes system/code/prompt/dataset changes and triggers targeted invalidations."""

    @abstractmethod
    def analyze_change(
        self,
        change_type: ChangeType,
        changed_entity: str,
        version_before: str,
        version_after: str,
        system_id: str,
    ) -> ChangeImpactReport:
        """Analyzes impact of a change and invalidates affected certifications."""
        pass


class ICertificationDashboardEngine(ABC):
    """Provides consolidated governance dashboard views."""

    @abstractmethod
    def build_dashboard_view(self) -> CertificationDashboardView:
        """Builds current certification and gate health dashboard."""
        pass
